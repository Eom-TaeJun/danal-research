# danal-research

핀테크 & 디지털자산 투자 리서치 자동화 에이전트

FRED(거시경제) + CoinGecko(디지털자산) + Perplexity(뉴스·기업 리서치)를 수집해
주간 브리핑, 투자 검토 보고서(IM), 섹터 스크리닝을 Markdown으로 자동 생성합니다.
거시 레짐(Goldilocks/Overheating/Stagflation/Recession)을 판단하고
다날의 KRW 스테이블코인·핀테크 사업 맥락에서 투자 함의까지 도출합니다.

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

레짐별로 다날 3대 사업(KRW 스테이블코인 SaaS / 휴대폰결제 / 글로벌 핀테크)에
대한 투자 함의와 주목 이벤트를 자동으로 도출합니다.

---

## 샘플 출력

### 주간 브리핑
- [brief_20260306.md](outputs/reports/brief_20260306.md) — **최신 (개선판)**
  - Executive 결론 1줄 + 레짐 명시 | 거시경제 스냅샷 | 디지털자산 시장 | 핵심 동향 3건
  - 다날 3축 투자 시사점 (KRW SaaS·x402·PCI 연결)
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

## 이 프로젝트가 증명하는 역량

다날 투자팀 인턴 포트폴리오 — 수동 리서치 대비 차별화 포인트:

| 일반 인턴 | 이 시스템 |
|---------|--------|
| IM 수동 작성 (Excel + Word) | **IM 자동화** — Perplexity 리서치 → 10섹션 초안 |
| 수동 시장 모니터링 | **멀티소스 자동 수집** — FRED·CoinGecko·Perplexity |
| 분석과 비즈니스 연결 누락 | **모든 분석 → 다날 3축 연결 의무화** |
| 거시 지표 나열 | **레짐 판단 → 투자 권고** (Goldilocks 등) |

---

## 요구 사항

```
python >= 3.11
requests, httpx, matplotlib
```

```bash
pip install -r requirements.txt
```
