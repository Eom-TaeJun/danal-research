# 목적: 수집된 데이터 → Markdown 리포트 생성
# 입력: --type [brief|im|screen] --company [optional]
# 출력: outputs/reports/[type]_YYYYMMDD.md
# 실패 시: 데이터 없으면 "데이터 없음" 섹션으로 대체
# 제외: PDF 변환, 이메일 발송 (시각화는 chart.py 연동)

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


def build_brief(data: dict, chart_paths: dict = None) -> str:
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
    ]
    if chart_paths and "stablecoin_pie" in chart_paths:
        # 리포트 경로 기준 상대 경로: outputs/reports/ → outputs/charts/
        pie_rel = "../charts/" + Path(chart_paths["stablecoin_pie"]).name
        lines += [
            f"![Stablecoin Market Share]({pie_rel})",
            "",
        ]
    lines += [
        "## 3. 이번 주 핵심 동향",
        "> 최신 뉴스는 `/brief` 커맨드 실행 시 Perplexity가 자동 보완합니다.",
        "",
        "## 4. 투자 시사점",
        "> 데이터 기반 시사점을 여기에 작성하세요.",
        "",
        "---",
        f"*Generated: {datetime.now().isoformat()} | Source: FRED, CoinGecko*",
    ]
    return "\n".join(lines)


def _fmt_list(items, fallback="- 조사 필요") -> str:
    return "\n".join(f"- {i}" for i in items) if items else fallback


def _fmt_table(headers: list, rows: list) -> str:
    head = " | ".join(headers)
    sep = "|".join("---" for _ in headers)
    lines = [f"| {head} |", f"|{sep}|"]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def _fmt_mgmt(team: list) -> str:
    if not team:
        return "_데이터 없음_"
    rows = [[m.get("name", "?"), m.get("title", "?"), m.get("background_one_line", "—")] for m in team]
    return _fmt_table(["이름", "직책", "주요 이력"], rows)


def _fmt_financials(history: list) -> str:
    if not history:
        return "_데이터 없음_"
    rows = [
        [h.get("year", "?"), h.get("revenue_usd_millions", "N/A"),
         h.get("net_income_usd_millions", "N/A"), f"{h.get('gross_margin_pct', 'N/A')}%"]
        for h in history
    ]
    return _fmt_table(["연도", "매출(백만$)", "순이익(백만$)", "매출총이익률"], rows)


def _fmt_valuation(metrics: dict) -> str:
    if not metrics:
        return "_데이터 없음_"
    rows = [
        ["시가총액(백만$)", metrics.get("market_cap_usd_millions", "N/A"), "—"],
        ["EV/Revenue", metrics.get("ev_revenue_multiple", "N/A"), metrics.get("peer_avg_ev_revenue_multiple", "N/A")],
        ["P/E", metrics.get("pe_ratio", "N/A"), "—"],
    ]
    return _fmt_table(["지표", "회사", "동종업계 평균"], rows)


def build_im(research_data: dict, company: str, chart_paths: dict = None) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    summary    = research_data.get("summary", "수집된 정보 없음")
    biz_model  = research_data.get("business_model", "—")
    products   = research_data.get("key_products", [])
    market_sz  = research_data.get("market_size", "—")
    competitors= research_data.get("competitors", [])
    bull       = research_data.get("bull_case", [])
    bear       = research_data.get("bear_case", [])
    risks      = research_data.get("risks", [])
    news       = research_data.get("recent_news", [])
    fin_hist   = research_data.get("financials_history", [])
    val_met    = research_data.get("valuation_metrics", {})
    mgmt_team  = research_data.get("management_team", [])

    chart_block = ""
    if chart_paths and "revenue_trend" in chart_paths:
        rel = "../charts/" + Path(chart_paths["revenue_trend"]).name
        chart_block = f"\n![Revenue Trend]({rel})\n"

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
{_fmt_list(products)}

---

## 3. 경영진
{_fmt_mgmt(mgmt_team)}

---

## 4. Market Opportunity
**시장 규모:** {market_sz}

**경쟁사:**
{_fmt_list(competitors)}

---

## 5. 재무 실적
{_fmt_financials(fin_hist)}{chart_block}
---

## 6. Investment Thesis

**Bull Case:**
{_fmt_list(bull)}

**Bear Case:**
{_fmt_list(bear)}

---

## 7. 밸류에이션
{_fmt_valuation(val_met)}

---

## 8. Key Risks
{_fmt_list(risks)}

---

## 9. 최근 동향
{_fmt_list(news)}

---

## 10. 다음 단계
- [ ] TAM/SAM/SOM 수치 확인
- [ ] 재무 지표 추가 (Revenue, EBITDA)
- [ ] 미팅 요청 여부

---
*Generated: {datetime.now().isoformat()} | Source: Perplexity*
"""


def report(report_type: str = "brief", company: str = "") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")

    if report_type == "brief":
        data = load_latest("snapshot_*.json")
        try:
            from src.chart import build_charts
            charts = build_charts(date_str)
        except Exception:
            charts = {}
        content = build_brief(data, chart_paths=charts)
        path = f"{OUTPUT_DIR}/brief_{date_str}.md"

    elif report_type == "im":
        safe = company.replace(" ", "_").replace("/", "-")
        data = load_latest(f"research_{safe}_*.json")
        try:
            from src.chart import build_im_charts
            im_charts = build_im_charts(data, date_str)
        except Exception:
            im_charts = {}
        content = build_im(data, company, im_charts)
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
