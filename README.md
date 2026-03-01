# danal-research

핀테크 & 디지털자산 투자 리서치 자동화 에이전트

거시경제 지표(FRED) + 스테이블코인 시장(CoinGecko)을 수집해
투자 브리핑과 IM(Investment Memorandum) 초안을 Markdown으로 생성합니다.

---

## 빠른 시작

```bash
git clone https://github.com/[username]/danal-research
cd danal-research
pip install -r requirements.txt
cp .env.example .env  # API 키 입력

python main.py --brief              # 주간 핀테크 브리핑
python main.py --im "Circle"        # 투자 검토 보고서 초안
python main.py --screen stablecoin  # 시장 스크리닝
```

---

## 샘플 출력

- [주간 브리핑 샘플](outputs/reports/brief_20260301.md)

---

## 구조

```
.claude/skills/          Claude Code 인터페이스 (Anthropic plugin 구조)
  weekly-brief/          주간 브리핑 스킬
  im-draft/              IM 초안 스킬
  stablecoin-market/     스테이블코인 시장 분석 스킬
src/
  collect.py             FRED + CoinGecko 데이터 수집
  research.py            Perplexity 기업 리서치
  report.py              Markdown 리포트 생성
outputs/reports/         생성된 리포트
```

---

## 데이터 소스

| 소스 | 용도 |
|------|------|
| [FRED](https://fred.stlouisfed.org/) | 금리·환율·CPI (무료) |
| [CoinGecko](https://www.coingecko.com/) | 스테이블코인 시총·거래량 (무료) |
| [Perplexity](https://www.perplexity.ai/) | 기업 리서치·최신 뉴스 |

---

## 환경 변수

```
FRED_API_KEY          https://fred.stlouisfed.org/docs/api/api_key.html
PERPLEXITY_API_KEY    https://www.perplexity.ai/settings/api
```
