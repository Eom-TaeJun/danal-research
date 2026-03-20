# danal-research

## 이 포트폴리오가 증명하는 것

> **다날 금융·투자 분석 인턴 JD가 요구한 일을 다날의 현재 사업 시그널에 맞춰 미리 구현했습니다.**

공식 공고의 3가지 업무를 1:1로 대응했습니다:
- **투자 리포트 및 IM 초안 지원**: Circle·Ripple·슈퍼블록·토스 IM 4종 + 마스터 리서치 리포트
- **금융 및 거시경제 데이터 분석**: FRED·CoinGecko·Perplexity 멀티소스 → 거시/규제/기업 분석 → 판단 자료화
- **전략 보고 및 시각화**: 차트 4종 + CSV 3종 + Excel 1종으로 의사결정 자료 정리

차별점은 도구가 아닙니다. **다날이 공식적으로 반복하는 `결제 캐시카우 -> 통합 결제 플랫폼 -> 글로벌/디지털자산 확장` 시그널을 리서치 workflow로 번역했다는 점**입니다. 그래서 모든 분석은 `시장 동향 요약 -> IM 초안 -> 차트/시나리오 -> 다날 사업 연결` 순서로 설계했고, `확신도`, `반증 신호`, `watch point`, `시니어 검토 전제`를 함께 남기도록 구성했습니다.

핵심 산출물: [마스터 리서치 리포트](outputs/reports/master_research_report_20260308.md) · [Circle S-1 영문 직독](outputs/reports/circle_s1_analysis_20260308.md)  
포지셔닝 원페이지: [PORTFOLIO_POSITIONING_ONE_PAGER.md](PORTFOLIO_POSITIONING_ONE_PAGER.md)  
정렬 메모: [JOB_SIGNAL_ALIGNMENT.md](JOB_SIGNAL_ALIGNMENT.md)  
공식 시그널 메모: [OFFICIAL_SIGNALS_20260320.md](OFFICIAL_SIGNALS_20260320.md)  
운영 원칙 메모: [WORKFLOW_PRINCIPLES.md](WORKFLOW_PRINCIPLES.md)

---

다날용 금융·투자 분석 지원 워크플로

FRED(거시경제) + CoinGecko(디지털자산) + Perplexity(뉴스·기업 리서치)를 수집해
주간 브리핑, 투자 검토 보고서(IM), 섹터 스크리닝 초안을 구조화합니다.
핵심 계산과 규칙은 정형화하고, 최종 서술은 사람이 읽는 내부 문서 형식으로 정리합니다.
즉, 범용 투자 자동화 데모가 아니라 다날 금융·투자 분석 인턴 JD에 맞춘 `workflow-first` 포트폴리오입니다.

---

## 다날 공식 시그널과 1:1 매핑

| 다날 공식 시그널 | 공식 근거 | 이 프로젝트에서 보여준 것 |
|---|---|---|
| `투자 리포트`, `IM`, `거시/금융 데이터`, `차트 시각화` | 금융·투자 분석 인턴 공고 | brief, IM 4종, master report, charts, CSV, Excel |
| `통합 결제 플랫폼` | 회사 소개 페이지 | 결제 본업과 신사업 확장을 함께 읽는 master report 구조 |
| `가맹점 중심`, `간단한 연동`, `유지관리` | 2025-03-20 D1 공식 보도자료 | 기술 설명보다 사업 적용성과 실행 가능성을 앞세운 리포트 구조 |
| `글로벌/외국인 결제`, `디지털자산 확장` | 2025-02-28 공식 보도자료, 회사 서비스 페이지 | Circle·Ripple·스테이블코인·크로스보더 결제 리서치 |
| `시장·정책 동향`, `수익 모델`, `실행 로드맵` | 2025-12-07 사업기획 공고 | 규제 비교, 시나리오 모델, scorecard, action-oriented 메모 |

이 프로젝트를 지원서나 면접에서 설명할 때의 핵심 번역은 [JOB_SIGNAL_ALIGNMENT.md](JOB_SIGNAL_ALIGNMENT.md)에 따로 정리했습니다.

---

## 이 포트폴리오의 분석 운영 원칙

- `workflow first`: 기능 데모보다 brief, IM, screen, chart처럼 실제 내부 문서 흐름을 우선합니다.
- `deterministic core first`: 데이터 수집, 지표 계산, 레짐 판단, 시나리오 표는 규칙 기반으로 고정하고 자연어는 보고서화에 집중합니다.
- `confidence + falsification`: 결론만 적지 않고 확신도, 반론, 반증 가능 신호, 다음 모니터링 포인트를 함께 남깁니다.
- `human-in-the-loop`: 인턴의 역할은 초안 작성과 자료 정리이며 최종 투자 판단은 시니어가 한다는 전제를 유지합니다.
- `action-oriented handoff`: 모든 출력은 다날의 결제 본업, 가맹점 가치, 글로벌/외국인 결제, 디지털자산 확장 중 어디에 닿는지로 닫습니다.
- `harness retained`: 역할 분리 하니스와 품질 게이트는 유지하되, 외부 설명에서는 메인 스토리가 아니라 안정적인 반복 생산을 돕는 보조 레이어로 둡니다.

이 운영 원칙은 구조적으로는 넓은 범용 자동화보다 좁고 검증 가능한 리서치 시스템에 더 가깝고, 그 요약은 [WORKFLOW_PRINCIPLES.md](WORKFLOW_PRINCIPLES.md)에 정리했습니다.

---

## 빠른 시작

```bash
git clone https://github.com/Eom-TaeJun/danal-research
cd danal-research
pip install -r requirements.txt
cp .env.example .env        # FRED_API_KEY, PERPLEXITY_API_KEY 입력

python main.py --brief              # 주간 핀테크/디지털자산 브리핑
python main.py --im "Circle"        # 투자 검토 보고서(IM) 초안
python main.py --screen stablecoin  # 섹터 스크리닝 + 레짐 분석
python main.py --analyze            # 거시 레짐 단독 분석
```

---

## 분석 파이프라인

```
사용자 요청
    │
    ├── --brief ─────────────────────────────────────────────────────┐
    │     collect.py: FRED(금리·환율) + CoinGecko(스테이블코인·BTC)    │
    │     + Perplexity(핀테크 뉴스)                                   │
    │     → outputs/reports/brief_YYYYMMDD.md                        │
    │                                                                 │
    ├── --im "[기업명]" ──────────────────────────────────────────────┤
    │     research.py: Perplexity(기업개요·재무·경영진·경쟁사)          │
    │     → outputs/reports/im_[기업명]_YYYYMMDD.md                  │
    │       (10섹션: Executive Summary ~ 다음 단계)                   │
    │                                                                 │
    ├── --screen [sector] ────────────────────────────────────────────┤
    │     collect.py → analyze.py → chart.py → report.py            │
    │     레짐 판단: 수익률 곡선 + Fed 스탠스 → 4가지 국면              │
    │     → outputs/reports/screen_[sector]_YYYYMMDD.md              │
    │       + outputs/charts/macro_dashboard_YYYYMMDD.png            │
    │       + outputs/charts/regime_gauge_YYYYMMDD.png               │
    │                                                                 │
    └── --analyze ────────────────────────────────────────────────────┘
          analyze.py: 스냅샷 → 레짐 + 스테이블코인 시그널 + 다날 함의
          → outputs/context/analysis_YYYYMMDD.json
```

---

## 레짐 분석 프레임워크

수익률 곡선(DGS10 - FEDFUNDS)과 Fed 스탠스를 교차해 경기 국면을 판단합니다.

```
              인플레이션 高 (Fed ≥ 4%)   인플레이션 低 (Fed < 3%)
성장 ↑  →      Overheating               Goldilocks  ← 현재
성장 ↓  →      Stagflation               Recession
```

레짐별로 다날의 결제 플랫폼 확장과 글로벌/디지털자산 사업에
대한 투자 함의와 주목 이벤트를 자동으로 도출합니다.

---

## 샘플 출력

### 주간 브리핑
- [brief_20260306.md](outputs/reports/brief_20260306.md) — **최신 (개선판)**
  - Executive 결론 1줄 + 레짐 명시 | 거시경제 스냅샷 | 디지털자산 시장 | 핵심 동향 3건
  - 다날 핵심 확장축 시사점 (통합결제·글로벌 결제·디지털자산 연결)
- [brief_20260302.md](outputs/reports/brief_20260302.md) — 초기 버전

### 마스터 리서치 리포트 ★ (2026-03-08 신규)
- [master_research_report_20260308.md](outputs/reports/master_research_report_20260308.md) — **핵심 포트폴리오 문서**
  - 거시→섹터→스크리닝→IM→권고 완전 연결 (6-Part 구조)
  - 레짐: "Goldilocks with sticky inflation" | 9개 지표 | 영문 원문 출처 27개
  - GENIUS Act 시행 완료·MiCA 집행·한국법 미확정 3단계 규제 비교
  - B2B 스테이블코인 $36B/년 실증 데이터 | 롱리스트 8개 → 숏리스트 3개 스크리닝
  - 반론 4개 + 반증 가능 신호 4개 명시 (분석 신뢰도 표시)

### Circle S-1 영문 원문 분석 ★ (2026-03-08 신규)
- [circle_s1_analysis_20260308.md](outputs/reports/circle_s1_analysis_20260308.md) — **영어 공시 직독 분석**
  - SEC S-1(2025-06-04) + FY2025 실적(2026-02-25) + GENIUS Act 원문 직접 분석
  - 수익 구조 분해: 준비금 이자 ~90% 취약성 | CPN $5.7B | USDC $11.9T
  - S-1 Risk Factors 영문 인용 4개 (금리 의존·법적 지위·Tether 경쟁·Coinbase 집중)
  - CCTP 기반 다날 KRW→USDC 정산 흐름 다이어그램 | 협력 타당성 최종 판단

### 투자 검토 보고서 (IM)
- [im_Circle_20260306.md](outputs/reports/im_Circle_20260306.md) — 투자의견 ☑ 검토 | 밸류에이션 피어 | 다날-Circle 협력 시나리오
- [im_Ripple_20260306.md](outputs/reports/im_Ripple_20260306.md) — 투자의견 ☑ 관심 | XRPL KSC 인프라 | RLUSD-KSC 공존 시나리오
- [im_슈퍼블록_20260308.md](outputs/reports/im_%EC%8A%88%ED%8D%BC%EB%B8%94%EB%A1%9D_20260308.md) — 기투자 사후검증 | $OVER FDV $3.8M | 경영진 보완 (Dan Park CTO)
- [im_토스_20260306.md](outputs/reports/im_%ED%86%A0%EC%8A%A4_20260306.md) — 투자의견 ☑ 보류 | 경쟁사 분석 | 다날 차별화 역도출

### 섹터 스크리닝
- [screen_stablecoin_20260306.md](outputs/reports/screen_stablecoin_20260306.md) — 규제 현황표 | 경쟁사 6개 비교 | 다날 포지셔닝

### 지원용 보강 문서 ★ (2026-03-21 신규)
- [decision_memo_Circle_20260321.md](outputs/reports/decision_memo_Circle_20260321.md) — 1페이지 투자 판단 메모 | 한 줄 결론 | 핵심 숫자 | 리스크 | watch point
- [shortlist_priority_memo_20260321.md](outputs/reports/shortlist_priority_memo_20260321.md) — 후보군 우선순위 메모 | Circle·Ripple·토스·슈퍼블록 정렬 기준
- [merchant_foreigner_payment_summary_20260321.md](outputs/reports/merchant_foreigner_payment_summary_20260321.md) — 가맹점·외국인 결제 공식 시그널 요약 | 포트폴리오 해석 기준

### 데이터 (CSV) ★ (2026-03-08 신규)
- [kwrw_stablecoin_scenario_20260308.csv](outputs/csv/kwrw_stablecoin_scenario_20260308.csv) — KRW SaaS 수익 시나리오 27개 (3규제×3전환율×3take rate)
- [screening_scorecard_20260308.csv](outputs/csv/screening_scorecard_20260308.csv) — 기업 스크리닝 스코어카드 (7개사, 100점 척도)
- [macro_snapshot_20260308.csv](outputs/csv/macro_snapshot_20260308.csv) — 거시지표 스냅샷 9개 (BLS·BEA·ISM·Fed·FRED 출처)

---

## 아키텍처

```
.
├── src/
│   ├── collect.py      FRED + CoinGecko + Perplexity 데이터 수집
│   ├── research.py     Perplexity 기업 심층 리서치
│   ├── analyze.py      레짐 판단 + 스테이블코인 시그널 + 다날 함의 도출
│   ├── report.py       Markdown 리포트 생성 (Brief / IM / Screen)
│   └── chart.py        시각화 (파이차트 / 매출추이 / 레짐게이지 / 대시보드)
│
├── .claude/
│   ├── agents/         Claude Code 서브에이전트 정의
│   │   ├── danal-lead.md       조율·품질 검토
│   │   ├── research-agent.md   IM 리서치 + None 보완
│   │   ├── collect-agent.md    데이터 수집 (경량)
│   │   ├── macro-analyst.md    거시 레짐 + 다날 함의
│   │   └── sanity-checker.md   품질 게이트 (None값·출처·다날함의 4-Gate)
│   ├── skills/         도메인 지식 자동 주입
│   │   ├── weekly-brief/       브리핑 구조·원칙
│   │   ├── im-draft/           IM 섹션 구조·작성 기준
│   │   ├── stablecoin-market/  스테이블코인 시장 도메인 지식
│   │   └── danal-context/      다날 전략 맥락 (자동 활성화)
│   └── settings.json   Hooks (API 키 확인, 경로 검증, 완성도 검증)
│
├── agents/contracts.json   에이전트 역할·계약 선언
├── INTENT.md               프로젝트 의도 + 불변 원칙 + 어휘 레지스터
├── outputs/
│   ├── reports/        생성된 리포트 (.md)
│   ├── charts/         시각화 차트 (.png)
│   └── context/        중간 데이터 (.json)
└── main.py
```

---

## 데이터 소스

| 소스 | 수집 데이터 | API |
|------|-----------|-----|
| [FRED](https://fred.stlouisfed.org/) | Fed Funds Rate, 10Y 국채, USD/KRW, CPI | 무료 |
| [CoinGecko](https://www.coingecko.com/) | 스테이블코인 시총·도미넌스·거래량, BTC/ETH | 무료 |
| [Perplexity](https://www.perplexity.ai/) | 핀테크 뉴스, 기업 재무·경영진·경쟁사 리서치 | 유료 |

---

## Claude Code 통합

이 프로젝트는 [Claude Code](https://claude.ai/code)의 에이전트 인프라를 활용합니다.

| 컴포넌트 | 역할 |
|---------|------|
| **Agents** (`.claude/agents/`) | 역할 분리 서브에이전트 — 조율·리서치·수집·분석 |
| **Skills** (`.claude/skills/`) | 도메인 지식 자동 주입 — 스테이블코인·IM·다날 컨텍스트 |
| **Hooks** (`.claude/settings.json`) | 가드레일 — API 키 확인, 경로 검증, 완성도 검증 |
| **INTENT.md** | 프로젝트 불변 원칙 + 어휘 레지스터 |

Claude Code에서 자연어로 작업 지시:
```
"Circle IM 만들어줘"                 → research-agent 자동 위임
"이번 주 스테이블코인 시장 브리핑"    → collect-agent + weekly-brief skill
"현재 매크로 레짐이 다날에 어떤 의미?" → macro-analyst + danal-context skill
```

---

## 환경 변수

```bash
FRED_API_KEY=...          # https://fred.stlouisfed.org/docs/api/api_key.html
PERPLEXITY_API_KEY=...    # https://www.perplexity.ai/settings/api
```

CoinGecko는 Public API (무료, 키 불필요).

---

## 이 프로젝트가 JD에 대해 증명하는 것

| JD 업무 | 이 프로젝트의 대응 산출물 |
|---------|-------------------------|
| 투자 리포트 작성 및 리서치 지원 | `brief_20260306.md`, `master_research_report_20260308.md` |
| 투자 검토 보고서(IM) 초안 작성 보조 | `im_Circle_20260306.md`, `im_Ripple_20260306.md`, `im_슈퍼블록_20260308.md`, `im_토스_20260306.md` |
| 금융 및 거시경제 데이터 분석 | `macro_snapshot_20260308.csv`, `master_research_report_20260308.md`, `regime_report_20260306.md` |
| 글로벌 핀테크 및 디지털자산 시장 조사 | Circle, Ripple, 스테이블코인, 규제 비교 리서치 |
| 전략 보고 및 시각화 | 차트 4종, `screening_scorecard_20260308.csv`, `danal_research_20260309.xlsx` |

---

## 요구 사항

```
python >= 3.11
requests, httpx, matplotlib
```

```bash
pip install -r requirements.txt
```
