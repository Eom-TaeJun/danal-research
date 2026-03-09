# INTENT — danal-research

> 세션 시작 시 **이 파일을 먼저 읽는다.** CLAUDE.md보다 우선.
> 여기 정의된 용어·원칙·경로·임계값이 프로젝트 전체의 단일 진실(Source of Truth).
> 모든 에이전트·스킬·코드는 이 파일의 정의를 따른다.

---

## 1. 프로젝트 목적

다날 핀테크·디지털자산 투자팀의 **리서치 워크플로 자동화**.

- 거시경제 + 디지털자산 시장 데이터를 수집해 주간 브리핑 생성
- 기업 IM(Investment Memorandum) 초안을 자동으로 구성
- 모든 분석은 다날의 전략적 방향(KRW SaaS, x402, PCI)과 연결

---

## 2. 불변 원칙 (절대 변경 불가)

1. **출력 경로**: 모든 생성 파일은 `outputs/` 하위에만 저장
2. **수치 출처 명기**: 모든 재무·시장 수치에 출처와 날짜 포함 — `(CoinGecko, 2026-03)`
3. **None 값 금지**: None이 남은 IM은 완성 리포트가 아님 — 반드시 보완
4. **skills/ 읽기 전용**: 도메인 지식 파일은 수정하지 않음
5. **다날 함의 필수**: 모든 분석의 마지막은 다날 4축 연결로 마무리

---

## 3. 레짐 정의 (Canonical — 코드·문서·차트 모두 이 정의 따름)

| 레짐 | 성장 방향 | 인플레이션 | 핵심 신호 | 다날 KRW SaaS 함의 |
|------|:------:|:--------:|---------|-----------------|
| **Goldilocks** | positive | moderate/low | 수익률 곡선 정상화, Fed 온건 | 신규 계약 공략 최적 타이밍 |
| **Overheating** | positive | high | Fed ≥ 4.5%, 긴축 지속 | 준비금 이자 모델 경쟁 우위 주의 |
| **Stagflation** | negative | high | 성장↓ + 물가↑ | 도입 의사결정 지연, 기존 고객 유지 |
| **Recession** | negative | moderate/low | 수익률 곡선 역전, 실업↑ | 안전자산 수요 → KRW 헤지 니즈 확대 |
| **Late-Cycle** | neutral | moderate/low | 성장 둔화 진입 이행 국면 | 신규 보수적, 리텐션 우선 |

> **Late-Cycle**: Goldilocks → Recession 이행 국면. neutral 성장은 Goldilocks가 아님.
> `analyze.py`의 `collect_growth_signals()` 임계값: `growth_norm ≥ 0.2` → positive, `≤ -0.2` → negative, 그 외 → neutral → **Late-Cycle**.

---

## 4. 다날 4축 (Canonical 용어)

| 축 | 공식 명칭 | 코드·보고서 표기 |
|---|---------|--------------|
| **캐시카우** | 휴대폰결제 | `payment_cashcow` |
| **성장동력** | KRW 스테이블코인 SaaS (KSC) | `stablecoin_saas` |
| **글로벌** | K.ONDA (외국인 통합결제) | `global_expansion` |
| **미래** | x402 프로토콜 / 페이코인(PCI) | `x402_ai` |

---

## 5. 경보 임계값 (Canonical — 코드에 하드코딩)

| 지표 | 임계값 | 의미 | 즉시 행동 |
|-----|:-----:|-----|---------|
| USD/KRW | > 1,500 | BOK 개입 임계 | KRW SaaS 리스크 보고 |
| USD/KRW | > 1,440 | 원화 약세 경계 | K.ONDA 채산성 모니터링 |
| BTC 24h | < -10% | 플래시 크래시 | 안전자산 선호 전환 대응 |
| 스테이블코인 시총 | < $200B | 채택 역행 | 도입 둔화 위험 |
| 스테이블코인 시총 | > $300B | 포화 진입 | 점유율 경쟁 심화 |
| Fed Funds | ≥ 4.5% | 고금리 구간 | Circle 준비금 수익 모델 재평가 |
| Fed Funds | < 3.5% | 완화 구간 | KRW SaaS 신규 계약 타이밍 |

---

## 6. 출력 파일 명명 규칙 (Canonical)

```
outputs/
├── reports/
│   ├── brief_YYYYMMDD.md            # 주간 브리핑
│   ├── im_[기업명]_YYYYMMDD.md      # 투자 검토 보고서
│   ├── screen_[섹터]_YYYYMMDD.md    # 섹터 스크리닝
│   └── regime_report_YYYYMMDD.md    # 레짐 독립 분석
├── context/
│   ├── snapshot_YYYYMMDD.json       # FRED+CoinGecko 수집 원본
│   ├── analysis_YYYYMMDD.json       # 레짐 판단 결과
│   └── research_[기업명]_YYYYMMDD.json  # 기업 리서치 원본
├── charts/
│   ├── stablecoin_pie_YYYYMMDD.png
│   ├── revenue_trend_YYYYMMDD.png
│   ├── regime_gauge_YYYYMMDD.png
│   └── macro_dashboard_YYYYMMDD.png
├── csv/
│   └── [설명]_YYYYMMDD.csv
└── excel/
    └── danal_research_YYYYMMDD.xlsx
```

> 기업명 한글 허용 — `im_토스_20260306.md` 형식 유효.
> `outputs/` 외부 경로 저장 금지 (불변 원칙 1).

---

## 7. 출처 명기 표준 (Canonical)

```
올바른 예:
  스테이블코인 시총: $263B (CoinGecko, 2026-03-06)
  Fed Funds Rate: 4.33% (FRED FEDFUNDS, 2026-03)
  Circle 매출: $1,670M (Circle FY2025 Press Release, 2026-02-25)
  확인 불가 수치: "확인 필요" 또는 "—"

잘못된 예 (절대 금지):
  스테이블코인 시총: $263B          ← 날짜·출처 없음
  매출: $1,670M (블룸버그)          ← 날짜 없음
  투자 시사점: 좋아질 것             ← ko: 접두어 누락 (Brief 한정)
```

---

## 8. 도메인 어휘 레지스터

| 용어 | 정의 |
|-----|-----|
| **IM** | Investment Memorandum — 내부 투자 검토 보고서 (10섹션) |
| **Brief** | 주간 핀테크/디지털자산 시장 브리핑 |
| **Screen** | 섹터 스크리닝 — 시장 내 기회 탐색 |
| **KSC** | KRW Stablecoin — 다날의 원화 스테이블코인 브랜드명 |
| **x402** | AI 에이전트 자동 결제 프로토콜 (HTTP 402 기반) |
| **PCI** | 페이코인 — 편의점 4사 연동 블록체인 결제 |
| **K.ONDA** | 다날 외국인 통합결제 플랫폼 (바이낸스·Circle 협력) |
| **GENIUS Act** | 미국 달러 스테이블코인 연방 규제법 (2025-07-18 시행) |
| **MiCA** | EU 암호자산시장 규정 (2024-06 발효) |
| **EMT** | E-Money Token — MiCA 내 법정화폐 연동 스테이블코인 |
| **TAM/SAM/SOM** | 전체/유효/획득가능 시장 규모 |
| **ko:** | Brief 투자 시사점 접두어 — 생략 시 sanity-checker Gate 2 FAIL |
| **확인 필요** | 출처 불명 수치 대체 표기 — None·빈칸 금지 |
| **WoW / YoY** | Week-over-Week / Year-over-Year |

---

## 9. 파일 구조 및 AI 네비게이션 맵

```
danal/
│
├── 📋 루트 문서 (읽기 순서)
│   ├── INTENT.md          ← 지금 이 파일. 가장 먼저 읽기. 단일 진실 원천.
│   ├── CLAUDE.md          ← 빠른 실행 명령 참조
│   ├── AGENTS.md          ← 하니스 아키텍처·레이어 설계
│   └── spec.md            ← 워크플로 상세·보고서 포맷 원천
│
├── 🐍 Python 파이프라인 (src/)
│   ├── collect.py         수집: FRED + CoinGecko + Perplexity → snapshot JSON
│   ├── research.py        기업 리서치: Perplexity → research JSON
│   ├── analyze.py         레짐 판단: snapshot → analysis JSON + DanalResult
│   ├── report.py          리포트 생성: JSON → Markdown
│   ├── chart.py           시각화: JSON → PNG
│   ├── excel.py           Excel 변환: CSV → xlsx
│   └── io.py              공통 유틸: load_latest() 등
│
├── 🤖 Claude Code 하니스 (.claude/)
│   ├── agents/
│   │   ├── danal-lead.md        허브 에이전트 — 조율·품질 검토
│   │   ├── research-agent.md    IM 리서치 + None 보완
│   │   ├── collect-agent.md     데이터 수집 (경량, Haiku)
│   │   ├── macro-analyst.md     레짐 판단 + 다날 함의 (7단계 CoT)
│   │   └── sanity-checker.md    4-Gate 품질 검증 (Haiku)
│   ├── skills/
│   │   ├── danal-context/       다날 전략 맥락 (자동 주입, user-invocable: false)
│   │   ├── im-draft/            IM 10섹션 구조·작성 기준
│   │   ├── stablecoin-market/   스테이블코인 도메인 지식
│   │   └── weekly-brief/        브리핑 구조·원칙
│   └── commands/
│       ├── brief.md  /im.md  /screen.md   슬래시 진입점
│
├── 📄 에이전트 계약
│   └── agents/contracts.json    역할·입출력·위임 계약 (새 에이전트 추가 시 등록)
│
└── 📊 산출물 (outputs/)
    └── (위 §6 파일 명명 규칙 참조)
```

---

## 10. 에이전트 역할 분담

```
사용자 요청
    ↓
danal-lead (조율·품질 검토)
    ├→ research-agent   IM 리서치 + None 보완  (Sonnet)
    ├→ collect-agent    데이터 수집 Brief/Screen  (Haiku)
    ├→ macro-analyst    레짐 판단 7단계 CoT + 다날 함의  (Sonnet)
    └→ sanity-checker   4-Gate 품질 검증  (Haiku, 자동 활성)
```

**Gate 순서**: Gate1(None값) → Gate2(포맷) → Gate3(출처) → Gate4(다날 함의)
모두 PASS여야 배포 가능. FAIL 시 해당 에이전트로 재위임.

---

## 11. 참조 문서

| 파일 | 내용 | 언제 읽나 |
|-----|-----|---------|
| `AGENTS.md` | 하니스 레이어 아키텍처·스킬 활성화 맵 | 에이전트 구조 이해 시 |
| `spec.md` | 보고서 포맷·레짐 판단 기준·출처 표준 상세 | 리포트 생성·레짐 분석 시 |
| `agents/contracts.json` | 에이전트 역할·계약 상세 | 새 에이전트 추가·수정 시 |
| `.claude/skills/danal-context/SKILL.md` | 다날 전략 맥락·최신 파트너십 | 다날 함의 작성 시 |
| `.claude/skills/danal-context/references/danal-profile.md` | 다날 재무·경쟁 포지셔닝 상세 | IM 다날 섹션 작성 시 |
