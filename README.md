# danal-research

> 다날 금융·투자 분석 인턴의 실제 업무를 재현하는 리서치 워크플로

다날의 사업 구조와 전략 방향을 먼저 파악하고,
거기서 출발해 외부 기업·시장·규제를 조사하고,
결과를 다날 관점의 판단 문서로 정리합니다.

---

## 판단 흐름과 산출물

이 프로젝트의 산출물은 아래 순서로 읽힙니다.

**1단계 — 다날의 현재 위치 파악**

| 문서 | 내용 |
|------|------|
| **[다날 사업 구조 메모](outputs/reports/danal_business_position_20260321.md)** | IR 북·재무정보 기반. 본업 PG 방어 vs 신사업 적자 구조, SC 발행→유통→정산 전략, 그래서 무엇을 조사해야 하는가 |

**2단계 — 외부 리서치 실행**

| 문서 | 내용 |
|------|------|
| **[마스터 리서치 리포트](outputs/reports/master_research_report_20260308.md)** | 거시 레짐 → 섹터 → 기업 스크리닝 → IM → 권고. 9개 거시지표, 영문 출처 27건, 3국 규제 비교 |
| **[Circle S-1 영문 분석](outputs/reports/circle_s1_analysis_20260308.md)** | SEC S-1 + FY2025 실적 영문 직독. 수익 구조 분해, Risk Factors 원문 인용 4건 |
| **[주간 브리핑](outputs/reports/brief_20260306.md)** | 거시경제 스냅샷 + 디지털자산 시장 + 핀테크 동향 + 투자 시사점 |
| **[스테이블코인 심화 분석](outputs/reports/deep_stablecoin_20260321.md)** | 시장 구조 + 3국 규제 비교 + 다날 재무 + KRW SaaS 시나리오 + 스크리닝 스코어카드 |

**3단계 — 다날 관점으로 압축**

| 문서 | 내용 |
|------|------|
| **[Circle Decision Memo](outputs/reports/decision_memo_Circle_20260321.md)** | 1페이지 판단 메모. "투자보다 파트너십 검토" 결론 → 핵심 숫자 → 리스크 → watch point |

> 전체 산출물: [reports/](outputs/reports/) · [charts/](outputs/charts/) · [csv/](outputs/csv/) · [excel/](outputs/excel/)

---

## 워크플로

```
다날 사업 구조·IR·재무 파악
    ↓
"무엇을 조사해야 하는가" 결정
    ↓
데이터 수집 (FRED · CoinGecko · Perplexity)
    ↓
거시 레짐 판단 + 기업/섹터 리서치
    ↓
판단 문서 생성 (Brief · IM · Decision Memo)
```

---

## 데이터 소스

| 소스 | 수집 항목 | 비용 |
|------|----------|------|
| 다날 공식 (IR 북·재무정보·보도자료) | 사업 전략, 재무, SC 전략 | 공개 |
| [FRED](https://fred.stlouisfed.org/) | Fed Funds Rate, 10Y 국채, USD/KRW, CPI | 무료 |
| [CoinGecko](https://www.coingecko.com/) | 스테이블코인 시총·도미넌스, BTC/ETH | 무료 |
| [Perplexity](https://www.perplexity.ai/) | 기업 재무·경영진·경쟁사, 핀테크 뉴스 | 유료 |

---

## 실행

```bash
pip install -r requirements.txt
cp .env.example .env   # FRED_API_KEY, PERPLEXITY_API_KEY

python main.py --brief              # 주간 브리핑
python main.py --im "Circle"        # IM 초안
python main.py --screen stablecoin  # 섹터 스크리닝
python main.py --deep stablecoin    # 스테이블코인 심화 분석
python main.py --analyze            # 레짐 판단
```

---

## 아키텍처

```
src/
├── collect.py      데이터 수집 (FRED + CoinGecko + Perplexity)
├── research.py     기업 심층 리서치
├── analyze.py      레짐 판단 + 다날 함의 도출
├── report.py       리포트 생성 (Brief / IM / Screen)
└── chart.py        시각화

outputs/
├── reports/        리포트 (.md)
├── charts/         차트 (.png)
├── csv/            시나리오·스코어카드 (.csv)
├── excel/          통합 분석 (.xlsx)
└── context/        수집 원본 (.json)
```

---

## 작업 환경

데이터 수집과 초안 생성에 [Claude Code](https://claude.ai/code)를 활용했습니다.
판단·검증·구조 설계는 직접 수행했습니다.

CoinGecko는 Public API (무료, 키 불필요).

```
python >= 3.11
requests, httpx, matplotlib
```
