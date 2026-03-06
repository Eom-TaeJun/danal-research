# danal — 프로그램 계획 / Todo / 차별점 전략

> 다날 핀테크·디지털자산 투자팀 인턴 지원 포트폴리오 종합 기획.

---

## Part 1. 프로그램 구현 계획

### 현재 파이프라인 구조

```
main.py
  --brief    → collect.py → report.py → brief_YYYYMMDD.md
  --im       → research.py → report.py → im_[기업명]_YYYYMMDD.md
  --screen   → collect.py → report.py → screen_[sector]_YYYYMMDD.md
  --analyze  → analyze.py → 레짐 판단
```

### 하니스 구조 설계 (참조 레포 패턴 적용)

> 아래 3개 레포의 2026 Best Practice를 적용한 설계 결정.

**참조 레포**:
- [`phuryn/pm-skills`](https://github.com/phuryn/pm-skills) — Skills·Commands·Plugins 3계층 분리, 스킬 자동 활성화
- [`shanraisshan/claude-code-best-practice`](https://github.com/shanraisshan/claude-code-best-practice) — `.claude/` 디렉토리 구조, Sub-Agent 정의 방식
- [`Eom-TaeJun/tech-digest`](https://github.com/Eom-TaeJun/tech-digest) — AGENTS.md·SKILL.md·spec.md 역할 분리, Hub-Spoke 에이전트 패턴

**적용된 설계 원칙**:

| 설계 원칙 | 출처 | 적용 위치 |
|---------|------|---------|
| Skills = 도메인 지식 빌딩블록, 자동 활성화 | pm-skills | `.claude/skills/*/SKILL.md` |
| Commands = 슬래시 진입점, Step+Gate 워크플로 | pm-skills·claude-code-best-practice | `.claude/commands/*.md` |
| Agents = Hub-Spoke 패턴 (lead + 전문가) | tech-digest | `.claude/agents/*.md` |
| SKILL.md ≤ 100줄, 상세는 `references/`로 분리 | tech-digest | `skills/im-draft/references/` |
| AGENTS.md = 하니스 레이어 아키텍처 문서 | tech-digest | `AGENTS.md` (루트) |
| spec.md = 방법론 원천, CLAUDE.md보다 우선 | pwc/spec.md 패턴 | `spec.md` (루트) |
| sanity-checker = 품질 게이트 에이전트 | pwc 패턴 | `.claude/agents/sanity-checker.md` |

**현재 `.claude/` 구조**:
```
.claude/
├── agents/
│   ├── danal-lead.md          조율·품질 검토 (Hub)
│   ├── research-agent.md      IM 리서치 + None 보완
│   ├── collect-agent.md       데이터 수집 (경량)
│   ├── macro-analyst.md       레짐 판단 + 다날 함의
│   └── sanity-checker.md      품질 게이트 (4-Gate)
├── commands/
│   ├── brief.md               Step 4단계 + Gate 2개
│   ├── im.md                  Step 5단계 + None 루프 + Gate 2개
│   └── screen.md              Step 4단계 + Gate 2개
├── skills/
│   ├── danal-context/SKILL.md
│   ├── im-draft/
│   │   ├── SKILL.md
│   │   └── references/im-structure.md
│   ├── stablecoin-market/SKILL.md
│   └── weekly-brief/SKILL.md
└── settings.json              Hooks (API 키 확인·경로 검증·완성도 검증)
```

**루트 문서 구조**:
```
AGENTS.md          하니스 레이어 아키텍처 표 + Skill Activation Map
spec.md            방법론 원천 (워크플로·레짐·출처 표준) — 최우선 참조
CLAUDE.md          빠른 참조 + 읽기 순서 명시
INTENT.md          프로젝트 불변 원칙 + 어휘 레지스터
portfolio-plan.md  프로그램 계획·Todo·차별점
agents/
└── contracts.json  에이전트 역할·계약 선언
```

**Python 파이프라인**:
```
src/
├── collect.py     FRED + CoinGecko + Perplexity 수집
├── research.py    Perplexity 기업 심층 리서치
├── analyze.py     레짐 판단 + 다날 함의
├── report.py      Markdown 리포트 생성
└── chart.py       시각화 (파이·매출추이·레짐게이지)
main.py            진입점
requirements.txt   의존성
```

---

### Phase 1: 기존 산출물 품질 개선 ✅

**목표**: 이미 있는 Circle IM + Brief를 "배포 가능" 수준으로 올리기

| 작업 | 파일 | 기준 |
|------|------|------|
| Circle IM 투자의견 확정 | `im_Circle_*.md` | `☑ 검토` or `☑ 관심` 확정 |
| 밸류에이션 피어 비교 추가 | 섹션 7 | Tether·Paxos·Coinbase 3개 피어 |
| 다날-Circle 협력 시나리오 | 섹션 10 | x402 결제 연동 시나리오 명시 |
| Brief Executive 결론 추가 | `brief_*.md` | 첫 줄에 "이번 주 핵심: [레짐] + [뉴스 1줄]" |
| Brief 레짐 명시 | 섹션 2 | "현재 레짐: Goldilocks (근거: ...)" |

### Phase 2: 신규 산출물 생성 ✅

**목표**: 역량 범위를 확장하는 추가 산출물 2-3개

| 산출물 | 명령 | 핵심 포인트 |
|--------|------|-----------|
| 토스 IM | `--im "토스"` | 경쟁사 분석 → 다날 차별화 역도출 |
| 레짐 분석 리포트 | `--analyze --report` | 통계 없이 투자팀 언어로 서술 |
| Screen 개선 | `--screen stablecoin` | 다날 포지셔닝 독립 섹션 |

### Phase 3: 통합 쇼케이스 마무리

| 작업 | 파일 | 내용 |
|------|------|------|
| preview.html 업데이트 | `preview.html` | 리포트 목록 + 역량 증명 맵핑 가시화 |
| README.md 작성 | `README.md` | 무엇을 증명하는가 한 단락 |

---


## Part 2. Todo 리스트

### Phase 1 ✅
- [x] Circle IM 투자의견 `☑ 검토` 확정
- [x] 섹션 7 밸류에이션 피어 비교표 추가
- [x] 섹션 10 다날 전략 연결 (바이낸스·Circle 협력 현실화)
- [x] Brief Executive 결론 + 레짐 명시

### Phase 2 ✅
- [x] 토스 IM 초안 + 다날 차별화 역도출
- [x] 레짐 분석 독립 리포트 (`regime_report_20260306.md`)
- [x] Screen 리포트 다날 포지셔닝 독립 섹션

### Phase 3 ✅
- [x] `preview.html` 전면 업데이트
- [x] `README.md` 역량 증명 섹션
- [x] `danal-context` 최신 파트너십 반영 (완료)

---

## Part 3. 3대 역량 전략

> AI는 도구입니다. 차별점은 **AI를 통해 표현되는 역량**에 있습니다.

---

### 역량 ① — 경제 분석력

> "수치를 읽는 것이 아니라, 수치가 의사결정에 주는 의미를 읽습니다."

| 증명 방법 | 산출물 | 핵심 포인트 |
|---------|-------|-----------|
| 거시 레짐 판단 | `regime_report_20260306.md` | Goldilocks/Overheating/Stagflation/Recession 4국면 + 3개 지표 수렴으로 판단 |
| 밸류에이션 해석 | `im_Circle_20260306.md` 섹션 7 | EV/Revenue 피어 비교 + 금리 하락 시나리오별 수익 추정 |
| 규제 영향 분석 | `screen_stablecoin_20260306.md` 섹션 4 | GENIUS Act·MiCA·디지털자산기본법 → 다날 사업 영향 연결 |
| 시나리오 분석 | `regime_report_20260306.md` 섹션 5 | Goldilocks 지속(70%)·Overheating(20%)·Recession(10%) 확률 |

**일반 지원자와의 차이**: 지표 나열이 아닌 **판단과 권고**로 표현.

---

### 역량 ② — 설득을 위한 데이터 분석 시각

> "데이터는 주장을 뒷받침하는 증거여야 합니다. 그래서 모든 수치에 출처가 있습니다."

| 증명 방법 | 산출물 | 핵심 포인트 |
|---------|-------|-----------|
| 구조적 논거 | 모든 IM 섹션 6 | Bull 3가지 + Bear 3가지 — 균형잡힌 투자 판단 |
| 데이터 시각화 | `outputs/charts/` 4종 | 파이차트·레짐게이지·매출트렌드·매크로대시보드 |
| 출처 의무화 | sanity-checker Gate 3 | "모든 재무 수치에 출처" — 주장이 아닌 근거 |
| 경쟁사 비교표 | `im_Circle_*.md` 섹션 4 | Tether·Circle·Paxos·MakerDAO 5행 구조화 비교 |
| 모니터링 지표 | `regime_report_20260306.md` 섹션 6 | 다음 주 상향/하향 신호 명시 — 반증 가능한 분석 |

**일반 지원자와의 차이**: "좋아 보인다"가 아닌 **"왜, 어떤 데이터로"**.

---

### 역량 ③ — 최신 AI 기술 학습·적용 도전력

> "AI를 쓴 것이 아니라, AI가 신뢰할 수 있게 작동하도록 시스템을 설계했습니다."

| 증명 방법 | 파일 | 핵심 포인트 |
|---------|------|-----------|
| Hub-Spoke 에이전트 | `.claude/agents/*.md` 5개 | 2026 Best Practice(tech-digest 패턴) 적용 |
| 품질 게이트 설계 | `sanity-checker.md` | None값·포맷·출처·다날함의 4-Gate — 신뢰성 확보 |
| 스킬 자동 주입 | `danal-context/SKILL.md` | `user-invocable: false` — 도메인 지식 자동화 |
| 방법론 문서화 | `AGENTS.md` + `spec.md` | 설계 결정의 이유를 문서로 설명 가능 |
| 참조 레포 적용 | `portfolio-plan.md` 섹션 1 | pm-skills·claude-code-best-practice·tech-digest 패턴 |

**일반 지원자와의 차이**: AI 사용이 아닌 **AI 시스템 설계**.

---

### 산출물 × 3대 역량 매핑

| 산출물 | 경제 분석력 | 데이터 시각 | AI 도전력 |
|-------|:---------:|:---------:|:--------:|
| `regime_report_20260306.md` | ★★★ | ★★ | ★ |
| `im_Circle_20260306.md` | ★★★ | ★★★ | ★★ |
| `im_토스_20260306.md` | ★★ | ★★ | ★★ |
| `screen_stablecoin_20260306.md` | ★★ | ★★★ | ★★ |
| `brief_20260306.md` | ★★ | ★★ | ★★★ |
| `.claude/` 아키텍처 | ★ | ★ | ★★★ |

---

*작성일: 2026-03-06 | 3대 역량: 경제 분석력 · 데이터 분석 시각 · AI 도전력*


