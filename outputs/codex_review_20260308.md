# Codex 교차검증 리포트 — danal (2026-03-08)

## 1. Gemini 아키텍처 분석 검증

### E. _IMPLICATIONS 하드코딩
부분 동의. `src/analyze.py:69-102`의 `_IMPLICATIONS`는 단순 상수라기보다 다날 사업 해석 로직 자체를 담고 있고, 이는 `AGENTS.md:28-35`의 "데이터는 Python, 지능은 Skills" 원칙과 충돌한다. 특히 `src/analyze.py:464-472`는 레짐 결과에 맞춰 이 문구를 그대로 주입해 리포트의 핵심 해석을 생성하므로, 운영 관점에서는 `.claude/skills/danal-context/SKILL.md:4-6, 37-58`에 있어야 할 전략 맥락이 코드에 중복 저장된 상태다.

다만 이 문제는 "즉시 오동작하는 버그"라기보다 유지보수/거버넌스 문제에 가깝다. 현재 구현은 네 개 레짐에 대한 다날 함의를 안정적으로 내보내므로 기능은 수행한다. 문제의 본질은 사업 문구를 바꾸려면 코드 배포가 필요하고, Skill과 코드가 쉽게 드리프트한다는 점이다.

### F. main.py ↔ 에이전트 충돌 위험
동의하되, 원인은 "절차형 main.py 자체"보다는 날짜 단위 파일명과 latest-load 패턴이다. `main.py:43-48`는 screen 실행 시 `collect()` → `analyze()` → `report()`를 순차 호출하고, 각 단계는 `src/collect.py:133-136`, `src/analyze.py:478-480`, `src/report.py:401-403`에서 날짜만 포함된 고정 파일명에 저장한다. 같은 날 두 번째 실행이 들어오면 같은 산출물을 덮어쓴다.

실제 overwrite 시나리오는 두 가지다.
- 같은 날 `python main.py --screen fintech` 후 `python main.py --screen stablecoin`을 실행하면 snapshot, analysis, 최종 report가 모두 같은 날짜 파일로 재저장된다. 게다가 `src/report.py:402-403`는 sector를 무시하고 항상 `screen_stablecoin_YYYYMMDD.md`로 저장하므로 첫 실행 산출물은 완전히 소실된다.
- 같은 날 screen 실행 뒤 brief를 다시 생성하면 `snapshot_YYYYMMDD.json`이 brief용 데이터로 덮인다. 이후 `src/report.py:17-23, 391-401`처럼 "가장 최신 snapshot + 가장 최신 analysis"를 조합해 screen 리포트를 다시 만들면, screen 분석 결과와 brief snapshot이 섞인 비일관 출력이 생길 수 있다.

즉 F는 이론적 우려가 아니라 현재 파일 네이밍/로딩 설계에서 이미 재현 가능한 위험이다.

## 2. Gemini가 놓친 것

### 새로 발견한 이슈
- `src/collect.py:119` vs `src/analyze.py:119-167`: `analyze.py`는 `DGS2`를 사용해 2Y-10Y 신호를 계산하지만, 수집기는 `FEDFUNDS`, `DGS10`, `DEXKOUS`, `CPIAUCSL`만 가져온다. 결과적으로 `yield_curve_2y_10y` 신호는 영구적으로 비활성 상태다.
- `src/collect.py:113-129`, `src/collect.py:141-147`, `main.py:43-48`, `src/report.py:391-403`: screen workflow가 sector-aware 하지 않다. `sector` 인자는 로깅 외에 사용되지 않고, report는 sector를 받지 않으며 결과 파일명도 항상 `screen_stablecoin_*.md`다. `fintech/defi/payments` 스크리닝은 현재 동일 데이터와 동일 파일로 덮어쓴다.
- `src/report.py:416-420` vs `.claude/commands/screen.md:29-31`: 문서는 `python src/report.py --type screen --sector "$ARGUMENTS"` 실행을 지시하지만, 실제 CLI는 `--sector`를 받지 않는다. 문서 기준 실행은 즉시 실패한다.
- `src/collect.py:106-107`: Perplexity 응답에서 JSON을 `re.search(r"\{.*\}")`로 다시 추출한다. Gemini가 `research.py`에서 지적했던 "regex 기반 JSON 추출" 취약점이 collect 쪽에는 그대로 남아 있다.
- `src/chart.py:255-265`: `macro_dashboard()`는 stablecoin 데이터가 비어 있으면 `max(pcts)`에서 `ValueError`가 난다. 실제로 빈 입력으로 재현되며, 파일 주석의 "데이터 없으면 None 반환" 계약과 맞지 않는다.
- `src/report.py:74-84`, `src/report.py:316-326`, `AGENTS.md:57-63`, `.claude/agents/sanity-checker.md:55-61`: 보고서가 숫자를 출력하면서도 각 수치에 `(출처, YYYY-MM)`를 붙이지 않는다. 이는 프로젝트 핵심 규칙 위반이고, 현재 산출물은 Gate 3를 구조적으로 통과할 수 없다.
- `src/report.py:110-113` vs `.claude/agents/sanity-checker.md:45-49`: brief 리포트는 `ko:` 접두어를 제거하지만, sanity-checker는 brief에서 `^- ko:` 3개 이상을 PASS 조건으로 본다. 생성기와 검증기의 규약이 서로 모순된다.
- `src/report.py:334-345` vs `src/analyze.py:57-64, 464-472` vs `.claude/skills/danal-context/SKILL.md:23-25, 45-48`: 분석 결과에는 `x402_ai`와 `priority_action`이 존재하지만 screen 리포트는 KRW SaaS/캐시카우/글로벌만 노출하고 x402 축과 우선 행동을 버린다. Danal context skill이 요구하는 3축 연결이 최종 산출물에서 일부 손실된다.
- `agents/contracts.json:41-46` vs `src/report.py:402-403`: 계약은 `outputs/reports/screen_[sector]_YYYYMMDD.md`를 약속하지만 구현은 항상 `screen_stablecoin_YYYYMMDD.md`를 만든다. 오케스트레이터가 계약 기반으로 산출물을 추적하면 실제 경로와 어긋난다.
- `agents/contracts.json:57-58` vs `src/analyze.py:477-480`: `macro-analyst` 계약은 텍스트 출력만 명시하지만 실제 구현은 `outputs/context/analysis_YYYYMMDD.json` 파일을 생성한다. 산출물 계약이 현실과 달라 자동화 파이프라인 확장 시 혼선을 만든다.

## 3. 신규 기능 제안 재평가

| 제안 | Gemini 판단 | Codex 판단 | 최종 권장 순위 |
|------|------------|------------|--------------|
| G (YFinance) | 신규 기능 제안 | ROI 높음. IM 품질을 직접 개선한다. 다만 `YFinance`만으로는 공시 신뢰성이 약하므로 우선순위는 "EDGAR 우선 + YFinance 보조"가 맞다. | 1 |
| H (Slack) | 신규 기능 제안 | 구현은 쉽지만 현재 산출물 품질/계약 문제가 남아 있어 배포 채널을 늘려도 핵심 가치가 커지지 않는다. 품질 게이트가 안정화된 뒤에 붙일 기능이다. | 3 |
| I (Feedback Loop) | 신규 기능 제안 | 장기적으로 유의미하지만, 예측 정의·관측 주기·정답 라벨링 체계가 먼저 필요하다. 지금 단계에서는 설계비용이 높고 즉시 효익이 제한적이다. | 2 |

### 더 나은 대안
- `run_id + manifest` 기반 아티팩트 버저닝. 현재 최우선 문제는 overwrite와 latest-load 혼선이다. `snapshot`, `analysis`, `report`를 동일 run_id로 묶으면 F의 실제 리스크를 바로 제거할 수 있다.
- 리포트 스키마/출처 validator 자동화. `AGENTS.md:62-64`의 규칙을 코드로 강제해, 각 숫자에 출처·날짜가 없으면 저장 자체를 막는 편이 Slack 연동보다 ROI가 높다.
- sector adapter 분리. `stablecoin` 중심 수집기를 `fintech/defi/payments`까지 동일 CLI로 노출하는 것이 현재 더 큰 문제다. sector별 데이터 수집 스키마와 리포트 템플릿을 먼저 분리해야 screen 기능이 실제 의미를 가진다.
