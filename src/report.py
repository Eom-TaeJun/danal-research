# 목적: 수집된 데이터 → Markdown 리포트 생성
# 입력: --type [brief|im|screen] --company [optional]
# 출력: outputs/reports/[type]_YYYYMMDD.md
# 실패 시: 데이터 없으면 "데이터 없음" 섹션으로 대체
# 제외: PDF 변환, 이메일 발송, 시각화 (별도)

import json
import os
import argparse
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = "outputs/reports"
CONTEXT_DIR = "outputs/context"


def load_latest(pattern: str) -> dict:
    """outputs/context/에서 가장 최신 파일 로드"""
    files = sorted(Path(CONTEXT_DIR).glob(pattern), reverse=True)
    if not files:
        return {}
    with open(files[0], encoding="utf-8") as f:
        return json.load(f)


def fmt_pct(val) -> str:
    if val is None:
        return "N/A"
    return f"{val:+.1f}%"


def fmt_num(val, unit="B") -> str:
    if val is None:
        return "N/A"
    if unit == "B":
        return f"${val/1e9:.1f}B"
    return str(val)


def build_brief(data: dict) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    macro = data.get("macro", {})
    stable = data.get("stablecoins", {})
    crypto = data.get("crypto", {})

    fed = macro.get("FEDFUNDS", {}).get("value", "N/A")
    dgs10 = macro.get("DGS10", {}).get("value", "N/A")
    krw = macro.get("DEXKOUS", {}).get("value", "N/A")

    usdt = stable.get("USDT", {})
    usdc = stable.get("USDC", {})
    total_mcap = sum(
        v.get("market_cap", 0) or 0 for v in stable.values()
    )

    btc = crypto.get("BTC", {})

    lines = [
        f"# 핀테크/디지털자산 주간 브리핑 — {date}",
        "",
        "## 1. 거시경제 스냅샷",
        f"| 지표 | 값 |",
        f"|------|-----|",
        f"| Fed Funds Rate | {fed}% |",
        f"| 미국 10Y 국채 | {dgs10}% |",
        f"| USD/KRW | {krw} |",
        "",
        "## 2. 디지털자산 시장",
        f"| 항목 | 값 | 7일 변화 |",
        f"|------|-----|---------|",
        f"| 스테이블코인 전체 시총 | {fmt_num(total_mcap)} | — |",
        f"| USDT | {fmt_num(usdt.get('market_cap'))} | {fmt_pct(usdt.get('price_change_7d'))} |",
        f"| USDC | {fmt_num(usdc.get('market_cap'))} | {fmt_pct(usdc.get('price_change_7d'))} |",
        f"| BTC | ${btc.get('price', 'N/A'):,} | {fmt_pct(btc.get('change_24h'))} (24h) |",
        "",
        "## 3. 이번 주 핵심 동향",
        "> 최신 뉴스는 `/brief` 커맨드 실행 시 Perplexity가 자동 보완합니다.",
        "",
        "## 4. 투자 시사점",
        "> 데이터 기반 시사점을 여기에 작성하세요.",
        "",
        f"---",
        f"*Generated: {datetime.now().isoformat()} | Source: FRED, CoinGecko*",
    ]
    return "\n".join(lines)


def build_im(research_data: dict, company: str) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    summary = research_data.get("summary", "수집된 정보 없음")
    biz_model = research_data.get("business_model", "—")
    competitors = research_data.get("competitors", [])
    risks = research_data.get("risks", [])
    news = research_data.get("recent_news", [])

    comp_str = "\n".join(f"- {c}" for c in competitors) if competitors else "- 조사 필요"
    risk_str = "\n".join(f"- {r}" for r in risks) if risks else "- 조사 필요"
    news_str = "\n".join(f"- {n}" for n in news) if news else "- 조사 필요"

    return f"""# Investment Memorandum — {company}
> 작성일: {date} | 초안 (Draft)

---

## 1. Executive Summary
{summary}

**투자 의견:** ☐ 관심  ☐ 검토  ☐ 보류

---

## 2. Company Overview
**사업 모델:** {biz_model}

**핵심 제품/서비스:**
- (조사 필요)

---

## 3. Market Opportunity
| 구분 | 규모 | 출처 |
|------|------|------|
| TAM | — | |
| SAM | — | |
| SOM | — | |

**시장 성장 드라이버:**
- (조사 필요)

**경쟁사:**
{comp_str}

---

## 4. Investment Thesis
**Bull Case:**
- (작성 필요)

**Bear Case:**
- (작성 필요)

---

## 5. Key Risks & Mitigants
{risk_str}

---

## 6. 최근 동향
{news_str}

---

## 7. 다음 단계
- [ ] 추가 확인 필요 항목
- [ ] 미팅 요청 여부

---
*Generated: {datetime.now().isoformat()} | Source: Perplexity*
"""


def report(report_type: str = "brief", company: str = "") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")

    if report_type == "brief":
        data = load_latest("snapshot_*.json")
        content = build_brief(data)
        path = f"{OUTPUT_DIR}/brief_{date_str}.md"

    elif report_type == "im":
        safe = company.replace(" ", "_").replace("/", "-")
        data = load_latest(f"research_{safe}_*.json")
        content = build_im(data, company)
        path = f"{OUTPUT_DIR}/im_{safe}_{date_str}.md"

    else:
        content = f"# Screen Report\n> {date_str}\n\n(작성 필요)"
        path = f"{OUTPUT_DIR}/screen_{date_str}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ 리포트 저장: {path}")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", default="brief",
                        choices=["brief", "im", "screen"])
    parser.add_argument("--company", default="")
    args = parser.parse_args()
    report(report_type=args.type, company=args.company)
