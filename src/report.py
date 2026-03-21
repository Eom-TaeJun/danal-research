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


def build_brief(data: dict, chart_paths: dict = None, analysis: dict = None) -> str:
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

    # Executive 결론 — 레짐 + 우선 행동 (analysis 있을 때)
    exec_line = ""
    if analysis:
        r = analysis.get("regime", {})
        danal = analysis.get("danal_implications", {})
        regime_name = r.get("regime", "")
        confidence = r.get("confidence", "")
        priority = danal.get("priority_action", "")
        if regime_name:
            exec_line = f"> **이번 주 핵심**: 레짐 **{regime_name}** ({confidence}) | {priority}"

    lines = [
        f"# 핀테크/디지털자산 주간 브리핑 — {date}",
        "",
    ]
    if exec_line:
        lines += [exec_line, ""]
    lines += [
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
        f"*작성: {datetime.now().strftime('%Y-%m-%d')} | Source: FRED, CoinGecko, 다날 공식(IR 북·보도자료·재무정보)*",
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
*작성: {datetime.now().strftime('%Y-%m-%d')} | Source: Perplexity, 다날 공식(IR 북·보도자료·재무정보)*
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
        f"- **스테이블코인 정산 SaaS**: {danal.get('stablecoin_saas', '—')}",
        f"- **결제 캐시카우**: {danal.get('payment_cashcow', '—')}",
        f"- **크로스보더 확장**: {danal.get('global_expansion', '—')}",
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
        f"| ⚠️ 리스크 2 | SEC 증권성 판단 — 이자 지급 SC 규제 불확실성 |",
        f"| ⚠️ 리스크 3 | Fed 금리 인하 시 준비금 이자 모델 수익성 압박 |",
        "",
        "---",
        f"*작성: {datetime.now().strftime('%Y-%m-%d')} | Source: FRED, CoinGecko, 다날 공식(IR 북·보도자료·재무정보)*",
    ]
    return "\n".join(lines)


def _inline_csv(csv_path: str, max_rows: int = 15) -> str:
    """CSV 파일을 마크다운 테이블로 변환"""
    import csv as csv_mod
    if not os.path.exists(csv_path):
        return "> CSV 파일 없음"
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv_mod.reader(f)
        headers = next(reader, [])
        rows = []
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            rows.append(row)
    if not headers:
        return "> 빈 CSV"
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for row in rows:
        cells = [str(c)[:30] for c in row]
        while len(cells) < len(headers):
            cells.append("")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)



def _scorecard_table(csv_path: str) -> str:
    """스크리닝 스코어카드 CSV → 마크다운 표"""
    import csv as csv_mod
    if not os.path.exists(csv_path):
        return "> 스코어카드 CSV 없음"
    with open(csv_path, encoding="utf-8-sig") as f:
        rows = list(csv_mod.DictReader(f))

    lines = [
        "| 기업 | 전략적합(40) | 기술보완(30) | 규제역량(20) | 협력가능(10) | **합계** | 판정 |",
        "|------|-----------|-----------|-----------|-----------|--------|------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['company']} "
            f"| {row['strategic_fit_score(40점)']} "
            f"| {row['tech_complement_score(30점)']} "
            f"| {row['regulatory_score(20점)']} "
            f"| {row['cooperation_score(10점)']} "
            f"| **{row['total_score(100점)']}** "
            f"| {row['recommendation']} |"
        )
    return "\n".join(lines)


def build_deep_stablecoin(snapshot: dict, analysis: dict,
                           chart_paths: dict = None) -> str:
    """스테이블코인 시장 심화 리포트"""
    date = datetime.now().strftime("%Y-%m-%d")
    macro = snapshot.get("macro", {})
    stable = snapshot.get("stablecoins", {})
    regime = analysis.get("regime", {})
    sig = analysis.get("stablecoin_signal", {})
    danal = analysis.get("danal_implications", {})
    danal_fin = snapshot.get("danal_financials", {})

    fed = macro.get("FEDFUNDS", {}).get("value", "N/A")
    dgs10 = macro.get("DGS10", {}).get("value", "N/A")
    krw = macro.get("DEXKOUS", {}).get("value", "N/A")
    total_b = sig.get("total_mcap_b", 0)

    # Chart refs
    def _chart_ref(key, alt=""):
        if chart_paths and key in chart_paths:
            rel = "../charts/" + Path(chart_paths[key]).name
            return f"\n![{alt}]({rel})\n"
        return ""

    # CSV 파일 경로 (최신)
    import glob
    scorecard_csvs = sorted(glob.glob("outputs/csv/screening_scorecard_*.csv"), reverse=True)

    lines = [
        f"# 스테이블코인 시장 심화 분석 — {date}",
        "",
        f"> 현재 레짐: **{regime.get('regime', '—')}** ({regime.get('confidence', '—')}) | "
        f"스테이블코인 시총: ${total_b}B",
        "",
        "---",
        "",
        "## 1. 거시지표 추이",
        "",
        f"| 지표 | 현재 | 레짐 신호 |",
        f"|------|------|---------|",
        f"| Fed Funds Rate | {fed}% | 금리 하락 기조 — SC 결제 볼륨 ↑, 이자 수익 ↓ |",
        f"| 10Y Treasury | {dgs10}% | 장기금리 안정 — 기업 투자 환경 양호 |",
        f"| USD/KRW | {krw} | 달러 강세 프록시 — 크립토·이머징 자금 흐름 참고 |",
        "",
    ]
    lines.append(_chart_ref("macro_timeseries", "거시지표 12개월 추이"))
    lines += [
        "---",
        "",
        "## 2. 스테이블코인 시장 구조",
        "",
        "| 코인 | 시총 | 도미넌스 | 수익 모델 | 규제 상태 |",
        "|------|------|---------|---------|---------|",
        f"| USDT | {fmt_num(stable.get('USDT', {}).get('market_cap'))} | ~70% | 이자 수익 (T-Bills) | 미규제 — GENIUS Act 적용 대상 |",
        f"| USDC | {fmt_num(stable.get('USDC', {}).get('market_cap'))} | ~29% | 이자 수익 + CPN 수수료 | SEC 등록, OCC 인가 추진 |",
        "| DAI | $4.2B | ~1.6% | 담보 이자 (DSR) | DeFi — MiCA 해당 없음 |",
        "| RLUSD | 출시 초기 | <0.1% | ODL 수수료 + 이자 | NYDFS 인가 |",
        "",
        "**구조적 특징:**",
        "- **이자 의존 모델의 한계**: USDT/USDC 모두 수익의 90%+ 가 준비금 이자. Fed 금리 1%p 인하 시 Circle 연 $4.4억 매출 감소 (S-1 기준)",
        "- **수수료 모델로의 전환**: Circle CPN ($5.7B 연간 볼륨), Ripple ODL — 거래 기반 수익 구조 시도",
        "- **수수료 기반 모델**: 이자가 아닌 **정산 수수료(take rate) 기반 SaaS** — 금리 변동에 구조적으로 중립",
        "",
    ]
    lines.append(_chart_ref("stablecoin_pie", "스테이블코인 시장점유율"))
    lines += [
        "---",
        "",
        "## 3. 규제 환경 비교",
        "",
        "| 관할 | 법안/규제 | 현황 | 다날 함의 |",
        "|------|---------|------|---------|",
        "| 미국 | GENIUS Act | 2025-07 통과 | USDC 정산 레일 안정성 ↑ — 규제 명확화로 기관 채택 가속 |",
        "| 미국 | SEC 가이던스 | 증권성 판단 기준 진화 중 | 이자 지급 SC(DAI 등)의 증권 분류 리스크 지속 |",
        "| EU | MiCA | 2024-06 시행, EBA 면제 종료 (2026-03-02) | 유럽 SC 발행 진입장벽 ↑ — USDC 유럽 시장 점유 기회 |",
        "",
        "---",
        "",
        "## 4. 다날 재무 현황",
        "",
    ]
    if danal_fin.get("annual"):
        lines += [
            "| 연도 | 매출 | 영업이익 | 세전순이익 | 해석 |",
            "|------|------|---------|----------|------|",
        ]
        for d in danal_fin["annual"]:
            note = ""
            if d["year"] == 2025:
                note = "영업이익 반등, 블록체인 투자 적자 확대"
            elif d["year"] == 2024:
                note = "매출 하락 가속, 효율화 시작"
            lines.append(
                f"| {d['year']} | {d['revenue']:,}억 | {d['operating_income']}억 "
                f"| {d['pretax_income']}억 | {note} |"
            )
        lines.append("")
    lines.append(_chart_ref("danal_financial", "다날 재무 추이"))
    lines += [
        "**핵심 긴장**: 본업 PG는 영업이익률 개선(6.4%→7.7%)으로 방어 중이나, "
        "블록체인 투자 영업외손실 누적으로 세전순이익 적자 3배 확대. "
        "신사업 수익화 시점이 투자 판단의 핵심.",
        "",
        "---",
        "",
        "## 5. 스테이블코인 리스크 평가",
        "",
    ]
    # 리스크 평가 삽입
    try:
        from src.risk import evaluate_stablecoins, STRESS_SCENARIOS
        risk_data = evaluate_stablecoins(snapshot)
        lines += [
            "| 코인 | 신용 | 유동성 | 규제 | 기술 | **종합** | 등급 |",
            "|------|------|--------|------|------|---------|------|",
        ]
        for a in risk_data["assessments"]:
            lines.append(
                f"| {a['ticker']} | {a['credit']:.0f} | {a['liquidity']:.0f} "
                f"| {a['regulatory']:.0f} | {a['technical']:.0f} "
                f"| **{a['total']:.0f}** | {a['grade']} |"
            )
        lines += [
            "",
            "**가중치**: 신용(30%) + 유동성(25%) + 규제(25%) + 기술(20%) — 0(안전)~100(위험)",
            "",
            "**스트레스 테스트 (Severe 시나리오 — 은행 위기급):**",
            "",
            "| 코인 | 디페그 확률 | 예상 손실 | 등급 |",
            "|------|-----------|----------|------|",
        ]
        for ticker, tests in risk_data["stress_tests"].items():
            severe = next((t for t in tests if "은행" in t["scenario"]), tests[-2] if len(tests) > 1 else tests[0])
            lines.append(
                f"| {ticker} | {severe['depeg_prob']:.1f}% "
                f"| {severe['expected_loss_pct']:.1f}% | {severe['rating']} |"
            )
        lines.append("")
    except Exception as e:
        lines.append(f"> 리스크 평가 생성 실패: {e}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 6. 리서치 대상 스크리닝",
        "",
    ]
    if scorecard_csvs:
        lines.append(_scorecard_table(scorecard_csvs[0]))
    lines += [
        "",
        "**기준**: 다날 전략적합성(40%) + 기술보완성(30%) + 규제역량(20%) + 협력가능성(10%)",
        "",
        "---",
        "",
        "## 7. 투자 시사점",
        "",
        f"- **레짐 {regime.get('regime', '—')}에서의 최적 행동**: {danal.get('stablecoin_saas', '—')}",
        f"- **본업 방어**: {danal.get('payment_cashcow', '—')}",
        f"- **글로벌 확장**: {danal.get('global_expansion', '—')}",
        "",
        "**watch point:**",
    ]
    for ev in danal.get("watch_events", []):
        lines.append(f"- {ev}")
    lines += [
        "",
        "---",
        f"*작성: {date} | Source: FRED, CoinGecko, SEC EDGAR, 다날 공식(IR 북·보도자료·재무정보)*",
    ]
    return "\n".join(lines)


def report(report_type: str = "brief", company: str = "", sector: str = "stablecoin") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")

    if report_type == "brief":
        data = load_latest("snapshot_*.json")
        analysis = load_latest("analysis_*.json") or {}
        try:
            from src.chart import build_charts
            charts = build_charts(date_str)
        except Exception as e:
            print(f"[WARN] chart 생성 실패: {e}")
            charts = {}
        content = build_brief(data, chart_paths=charts, analysis=analysis)
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

    elif report_type == "deep":
        snapshot = load_latest("snapshot_*.json")
        analysis = load_latest("analysis_*.json")
        try:
            from src.chart import build_deep_charts
            deep_charts = build_deep_charts(snapshot, date_str)
        except Exception as e:
            print(f"[WARN] chart 생성 실패: {e}")
            deep_charts = {}
        content = build_deep_stablecoin(snapshot, analysis, chart_paths=deep_charts)
        path = f"{OUTPUT_DIR}/deep_stablecoin_{date_str}.md"

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
