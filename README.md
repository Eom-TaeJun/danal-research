# danal-research

> US 스테이블코인 시장 중심의 핀테크 투자 리서치 워크플로

다날의 사업 구조를 먼저 파악하고, 거시경제·규제·시장 데이터를 수집해
레짐을 판단하고, 투자 대상 기업을 스크리닝해 판단 문서로 정리합니다.

**[HTML Dashboard](outputs/html/index.html)** | [Reports](outputs/reports/) | [Charts](outputs/charts/)

---

## 판단 흐름

**Stage 1 — 사업 구조 파악**

| 문서 | 내용 |
|------|------|
| **[다날 사업 구조 메모](outputs/reports/danal_business_position_20260321.md)** | IR·재무 기반. PG 본업 방어 vs 블록체인 신사업, SC 정산 전략 |

**Stage 2 — 외부 리서치**

| 문서 | 내용 |
|------|------|
| **[마스터 리서치 리포트](outputs/reports/master_research_report_20260308.md)** | 거시 레짐 → 섹터 → 기업 스크리닝 → IM. 영문 출처 27건, 규제 비교 |
| **[Circle S-1 분석](outputs/reports/circle_s1_analysis_20260308.md)** | SEC S-1 원문 직독. 수익 구조 분해, Risk Factors 인용 |
| **[스테이블코인 심화](outputs/reports/deep_stablecoin_20260321.md)** | 시장 구조 + US/EU 규제 + 4축 리스크 스코어링 + 스트레스 테스트 |
| **[주간 브리핑](outputs/reports/brief_20260321.md)** | 거시 스냅샷 + 스테이블코인 시장 + 투자 시사점 |

**Stage 3 — 투자 판단**

| 문서 | 내용 |
|------|------|
| **[Circle Decision Memo](outputs/reports/decision_memo_Circle_20260321.md)** | 1페이지 판단 메모 — "투자보다 파트너십 검토" 결론 |
| **[Shortlist Priority](outputs/reports/shortlist_priority_memo_20260321.md)** | 전략적합성 기반 기업 우선순위 |

---

## 핵심 기능

| 모듈 | 역할 |
|------|------|
| `collect.py` | FRED + CoinGecko + Perplexity 데이터 수집 |
| `analyze.py` | 8개 신호 가중 합산 → 거시 레짐 판단 (Goldilocks / Overheating / Late-Cycle / Stagflation / Recession) |
| `risk.py` | 스테이블코인 4축 리스크 스코어링 (신용·유동성·규제·기술) + 스트레스 테스트 |
| `calibrate.py` | 과거 분석 결과 기반 Spearman 상관 → 신호 가중치 자동 보정 |
| `report.py` | Markdown 리포트 생성 (Brief / IM / Screen / Deep) |
| `html.py` | MD → HTML 변환 + 대시보드 생성 |
| `chart.py` | matplotlib 시각화 (레짐 게이지, 파이차트, 시계열) |

---

## 실행

```bash
pip install -r requirements.txt
cp .env.example .env   # FRED_API_KEY, PERPLEXITY_API_KEY

python main.py --brief              # 주간 브리핑
python main.py --im "Circle"        # IM 초안
python main.py --screen stablecoin  # 섹터 스크리닝
python main.py --deep stablecoin    # 심화 분석
python main.py --analyze            # 레짐 판단
python main.py --calibrate          # 가중치 자동 보정
python main.py --html               # HTML 대시보드 생성
```

---

## 아키텍처

```
src/
├── collect.py      데이터 수집 (FRED + CoinGecko + Perplexity)
├── analyze.py      레짐 판단 + 8개 가중 신호 + 비즈니스 함의
├── risk.py         4축 리스크 스코어링 + 스트레스 테스트
├── calibrate.py    Spearman 상관 기반 가중치 자동 보정
├── research.py     기업 심층 리서치
├── report.py       Markdown 리포트 생성
├── html.py         MD → HTML 변환 + 대시보드
├── chart.py        시각화 (matplotlib)
├── excel.py        Excel 변환
└── io.py           파일 I/O 유틸

tests/
└── test_smoke.py   risk, calibrate, analyze 스모크 테스트 (9건)

outputs/
├── html/           HTML 대시보드 + 리포트
├── reports/        Markdown 리포트
├── charts/         차트 (PNG)
├── csv/            스코어카드
├── excel/          통합 분석 (XLSX)
└── context/        수집 원본 (JSON, .gitignore)
```

---

## 데이터 소스

| 소스 | 수집 항목 | 비용 |
|------|----------|------|
| [FRED](https://fred.stlouisfed.org/) | Fed Funds Rate, 10Y 국채, USD/KRW, CPI | 무료 |
| [CoinGecko](https://www.coingecko.com/) | 스테이블코인 시총·도미넌스, BTC/ETH | 무료 |
| [Perplexity](https://www.perplexity.ai/) | 기업 재무·경영진·경쟁사, 핀테크 뉴스 | 유료 |
| 다날 공식 (IR 북·재무정보) | 사업 전략, 재무 | 공개 |

---

## 작업 환경

데이터 수집과 초안 생성에 [Claude Code](https://claude.ai/code)를 활용했습니다.
판단·검증·구조 설계는 직접 수행했습니다.

```
python >= 3.11
requests, httpx, matplotlib, markdown, jinja2
```
