# 목적: 수집된 데이터 → Markdown 리포트 생성
# 입력: --type [brief|im|screen] --company [optional]
# 출력: outputs/reports/[type]_YYYYMMDD.md
# 실패 시: 데이터 없으면 "데이터 없음" 섹션으로 대체
# 제외: PDF 변환, 이메일 발송 (시각화는 chart.py 연동)

import os
import argparse
from datetime import datetime
from pathlib import Path
from src.io import load_latest

OUTPUT_DIR = "outputs/reports"


def fmt_pct(val) -> str:
    if val is None:
        return "N/A"
    return f"{val:+.1f}%"


def fmt_num(val, unit="B") -> str:
    if val is None:
        return "N/A"
    try:
        val = float(str(val).replace(",", ""))
    except (ValueError, TypeError):
        return str(val)
    if unit == "B":
        return f"${val/1e9:.1f}B"
    return str(val)


def _na(v, suffix="") -> str:
    return "[확인 필요]" if v is None else f"{v}{suffix}"


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
    _btc_price = btc.get("price")
    btc_price_str = f"${int(_btc_price):,}" if isinstance(_btc_price, (int, float)) else "N/A"

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
        f"| BTC | {btc_price_str} | {fmt_pct(btc.get('change_24h'))} (24h) |",
        "",
    ]
    if chart_paths and "stablecoin_pie" in chart_paths:
        # 리포트 경로 기준 상대 경로: outputs/reports/ → outputs/charts/
        pie_rel = "../charts/" + Path(chart_paths["stablecoin_pie"]).name
        lines += [
            f"![Stablecoin Market Share]({pie_rel})",
            "",
        ]
    # 섹션 3: 핵심 동향 (Perplexity 뉴스)
    news = data.get("news", {})
    news_items = news.get("items", [])
    implications = news.get("implications", [])

    lines += ["## 3. 이번 주 핵심 동향", ""]
    if news_items:
        for item in news_items:
            lines.append(f"**{item.get('title', '')}**")
            lines.append(item.get("summary", ""))
            lines.append("")
    else:
        lines += ["> 뉴스 데이터 없음 (PERPLEXITY_API_KEY 확인)", ""]

    # 섹션 4: 투자 시사점
    lines += ["## 4. 투자 시사점", ""]
    if implications:
        for imp in implications:
            clean = imp.replace("ko: ", "").replace("ko:", "").strip()
            lines.append(f"- {clean}")
        lines.append("")
    else:
        lines += ["> 시사점 데이터 없음", ""]

    lines += [
        "---",
        f"*Generated: {datetime.now().isoformat()} | Source: FRED, CoinGecko, Perplexity*",
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
        [h.get("year", "?"), _na(h.get("revenue_usd_millions")),
         _na(h.get("net_income_usd_millions")), _na(h.get("gross_margin_pct"), "%")]
        for h in history
    ]
    return _fmt_table(["연도", "매출(백만$)", "순이익(백만$)", "매출총이익률"], rows)


def _fmt_valuation(metrics: dict) -> str:
    if not metrics:
        return "_데이터 없음_"
    rows = [
        ["시가총액(백만$)", _na(metrics.get("market_cap_usd_millions")), "—"],
        ["EV/Revenue", _na(metrics.get("ev_revenue_multiple")), _na(metrics.get("peer_avg_ev_revenue_multiple"))],
        ["P/E", _na(metrics.get("pe_ratio")), "—"],
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


def build_screen(snapshot: dict, analysis: dict, chart_paths: dict = None) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    macro = snapshot.get("macro", {})
    stable = snapshot.get("stablecoins", {})

    regime = analysis.get("regime", {})
    sig = analysis.get("stablecoin_signal", {})
    danal = analysis.get("danal_implications", {})

    fed = macro.get("FEDFUNDS", {}).get("value", "N/A")
    dgs10 = macro.get("DGS10", {}).get("value", "N/A")
    krw = macro.get("DEXKOUS", {}).get("value", "N/A")

    total_b = sig.get("total_mcap_b", 0)
    usdt_dom = sig.get("usdt_dom_pct", 0)
    usdc_dom = sig.get("usdc_dom_pct", 0)
    stablecoin_signal = sig.get("signal", "—").upper()
    stablecoin_note = sig.get("note", "—")

    rationale_lines = "\n".join(f"  - {r}" for r in regime.get("rationale", []))

    lines = [
        f"# 스테이블코인 섹터 스크리닝 — {date}",
        "",
    ]
    if chart_paths and "macro_dashboard" in chart_paths:
        rel = "../charts/" + Path(chart_paths["macro_dashboard"]).name
        lines += [f"![Market Snapshot Dashboard]({rel})", ""]
    lines += [
        "---",
        "",
        "## 1. 거시 레짐",
        "",
        f"| 판단 | 확신 | 성장 방향 | 인플레이션 |",
        f"|------|------|---------|-----------|",
        f"| **{regime.get('regime', '—')}** | {regime.get('confidence', '—')} "
        f"| {regime.get('growth_dir', '—')} | {regime.get('inflation_dir', '—')} |",
        "",
        "**근거:**",
        rationale_lines,
        "",
    ]
    if chart_paths and "regime_gauge" in chart_paths:
        rel = "../charts/" + Path(chart_paths["regime_gauge"]).name
        lines += [f"![Regime Gauge]({rel})", ""]

    lines += [
        "## 2. 거시경제 스냅샷",
        "",
        f"| 지표 | 값 |",
        f"|------|-----|",
        f"| Fed Funds Rate | {fed}% |",
        f"| 미국 10Y 국채 | {dgs10}% |",
        f"| USD/KRW | {krw} |",
        "",
        "## 3. 스테이블코인 시장",
        "",
        f"**전체 시총: ${total_b}B** — 시그널: `{stablecoin_signal}`",
        f"> {stablecoin_note}",
        "",
        "| 코인 | 시총 | 도미넌스 | 7일 변화 |",
        "|------|------|---------|---------|",
    ]
    for sym, v in stable.items():
        mcap = fmt_num(v.get("market_cap"))
        dom = round((v.get("market_cap") or 0) / (total_b * 1e9) * 100, 1) if total_b else 0
        chg = fmt_pct(v.get("price_change_7d"))
        lines.append(f"| {sym} | {mcap} | {dom}% | {chg} |")

    if chart_paths and "stablecoin_pie" in chart_paths:
        rel = "../charts/" + Path(chart_paths["stablecoin_pie"]).name
        lines += ["", f"![Stablecoin Market Share]({rel})"]

    lines += [
        "",
        "## 4. 다날 비즈니스 함의",
        "",
        f"**레짐 {regime.get('regime', '—')} 기준:**",
        "",
        f"- **KRW 스테이블코인 SaaS**: {danal.get('stablecoin_saas', '—')}",
        f"- **휴대폰결제 캐시카우**: {danal.get('payment_cashcow', '—')}",
        f"- **글로벌 핀테크 확장**: {danal.get('global_expansion', '—')}",
        "",
        "**주목할 이벤트:**",
    ]
    for ev in danal.get("watch_events", []):
        lines.append(f"- {ev}")

    lines += [
        "",
        "## 5. 투자 기회 & 리스크 매트릭스",
        "",
        "| 구분 | 내용 |",
        "|------|------|",
        f"| ✅ 기회 1 | 스테이블코인 규제 명확화(GENIUS Act) → SaaS 신규 수요 |",
        f"| ✅ 기회 2 | {regime.get('regime', '')} 레짐 → {danal.get('stablecoin_saas', '')[:40]}... |",
        f"| ✅ 기회 3 | PCI 편의점 결제 확장 — 경기 방어적 포지션 |",
        f"| ⚠️ 리스크 1 | USDT 도미넌스 {usdt_dom}% 집중 → Circle 이탈 시 구조 변화 |",
        f"| ⚠️ 리스크 2 | USD/KRW {krw} — 환율 변동성 |",
        f"| ⚠️ 리스크 3 | 한국 디지털자산기본법 스테이블코인 정의 미확정 |",
        "",
        "---",
        f"*Generated: {datetime.now().isoformat()} | Source: FRED, CoinGecko, Perplexity*",
    ]
    return "\n".join(lines)


def report(report_type: str = "brief", company: str = "", sector: str = "stablecoin") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")

    if report_type == "brief":
        data = load_latest("snapshot_*.json")
        try:
            from src.chart import build_charts
            charts = build_charts(date_str)
        except Exception as e:
            print(f"[WARN] chart 생성 실패: {e}")
            charts = {}
        content = build_brief(data, chart_paths=charts)
        path = f"{OUTPUT_DIR}/brief_{date_str}.md"

    elif report_type == "im":
        safe = company.replace(" ", "_").replace("/", "-")
        data = load_latest(f"research_{safe}_*.json")
        try:
            from src.chart import build_im_charts
            im_charts = build_im_charts(data, date_str)
        except Exception as e:
            print(f"[WARN] chart 생성 실패: {e}")
            im_charts = {}
        content = build_im(data, company, im_charts)
        path = f"{OUTPUT_DIR}/im_{safe}_{date_str}.md"

    elif report_type == "screen":
        snapshot = load_latest("snapshot_*.json")
        analysis = load_latest("analysis_*.json")
        try:
            from src.chart import build_analysis_charts, build_charts
            screen_charts = {**build_charts(date_str),
                             **build_analysis_charts(analysis, date_str,
                                                     snapshot=snapshot)}
        except Exception as e:
            print(f"[WARN] chart 생성 실패: {e}")
            screen_charts = {}
        content = build_screen(snapshot, analysis, chart_paths=screen_charts)
        safe_sector = sector.replace(" ", "_").replace("/", "-") or "stablecoin"
        path = f"{OUTPUT_DIR}/screen_{safe_sector}_{date_str}.md"

    else:
        content = f"# Screen Report\n> {date_str}\n\n(sector 미지정)"
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
