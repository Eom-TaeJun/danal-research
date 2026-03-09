# 목적: 수집된 snapshot 데이터 → 시각화 차트 PNG 생성
# 입력: outputs/context/snapshot_*.json
# 출력: outputs/charts/[name]_YYYYMMDD.png  (상대 경로 반환)
# 실패 시: matplotlib 없거나 데이터 없으면 None 반환
# 제외: 인터랙티브 차트, 웹 대시보드, 실시간 스트리밍

import os
from datetime import datetime
from src.io import load_latest

OUTPUT_DIR = "outputs/charts"


def stablecoin_pie(data: dict, date_str: str) -> str | None:
    """스테이블코인 시장점유율 파이차트 → PNG 경로 반환"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    stable = data.get("stablecoins", {})
    if not stable:
        return None

    labels = list(stable.keys())
    sizes = [stable[k].get("market_cap", 0) or 0 for k in labels]
    total = sum(sizes)
    if total == 0:
        return None

    # 1% 미만은 "기타"로 묶기
    threshold = total * 0.01
    main_labels, main_sizes, other = [], [], 0
    for lbl, sz in zip(labels, sizes):
        if sz >= threshold:
            main_labels.append(lbl)
            main_sizes.append(sz)
        else:
            other += sz
    if other > 0:
        main_labels.append("Others")
        main_sizes.append(other)

    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#607D8B"]
    explode = [0.05] + [0] * (len(main_labels) - 1)

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        main_sizes,
        labels=main_labels,
        autopct="%1.1f%%",
        colors=colors[: len(main_labels)],
        explode=explode,
        startangle=140,
    )
    for t in autotexts:
        t.set_fontsize(9)

    total_b = total / 1e9
    ax.set_title(
        f"Stablecoin Market Share  (Total: ${total_b:.1f}B)",
        fontsize=12,
        fontweight="bold",
        pad=14,
    )
    fig.tight_layout()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/stablecoin_pie_{date_str}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ 차트 저장: {path}")
    return path


def build_charts(date_str: str = None) -> dict:
    """snapshot 로드 후 모든 차트 생성, {name: path} 반환"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
    data = load_latest("snapshot_*.json")
    paths = {}
    pie = stablecoin_pie(data, date_str)
    if pie:
        paths["stablecoin_pie"] = pie
    return paths


def revenue_trend(research_data: dict, date_str: str) -> str | None:
    """재무 이력 → 매출 막대차트 PNG (숫자 없으면 None)"""
    history = research_data.get("financials_history", [])
    if not history:
        return None
    years, revenues = [], []
    for h in history:
        try:
            revenues.append(float(h["revenue_usd_millions"]))
            years.append(str(h.get("year", "?")))
        except (KeyError, TypeError, ValueError):
            return None  # 숫자 아니면 skip
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(years, revenues, color="#2196F3")
    ax.set_title("Revenue Trend (USD M)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Revenue (USD M)")
    fig.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/revenue_trend_{date_str}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ 차트 저장: {path}")
    return path


def build_im_charts(research_data: dict, date_str: str = None) -> dict:
    """IM용 차트 생성 → {name: path} 반환"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
    paths = {}
    trend = revenue_trend(research_data, date_str)
    if trend:
        paths["revenue_trend"] = trend
    return paths


def regime_gauge(analysis: dict, date_str: str) -> str | None:
    """레짐 2×2 매트릭스 시각화 → PNG (현재 위치 표시)"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        plt.rcParams["font.family"] = "NanumGothic"
        plt.rcParams["axes.unicode_minus"] = False
    except ImportError:
        return None

    regime_data = analysis.get("regime", {})
    regime = regime_data.get("regime", "Goldilocks")
    confidence = regime_data.get("confidence", "Medium")

    # 레짐 → 셀 위치 (col, row): 0-based, (0,0)=좌하단
    _pos = {
        "Recession":   (0, 0), "Goldilocks":  (1, 0),
        "Stagflation": (0, 1), "Overheating": (1, 1),
        "Late-Cycle":  (0, 0),
    }
    _colors = {
        "Recession": "#90CAF9", "Goldilocks": "#A5D6A7",
        "Stagflation": "#FFCC80", "Overheating": "#EF9A9A",
        "Late-Cycle": "#B0BEC5",
    }
    _base_regimes = ("Recession", "Goldilocks", "Stagflation", "Overheating")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(0, 2); ax.set_ylim(0, 2)
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2])
    ax.set_xticklabels(["", "성장↑", "성장↓"], fontsize=10)
    ax.set_yticklabels(["", "인플레↓", "인플레↑"], fontsize=10)
    ax.tick_params(length=0)
    ax.grid(True, color="white", linewidth=2)
    ax.set_facecolor("#F5F5F5")

    for name in _base_regimes:
        c, r = _pos[name]
        fc = _colors[name]
        rect = mpatches.FancyBboxPatch(
            (c + 0.05, r + 0.05), 0.9, 0.9,
            boxstyle="round,pad=0.05", linewidth=1.5,
            edgecolor="white", facecolor=fc, alpha=0.85,
        )
        ax.add_patch(rect)
        ax.text(c + 0.5, r + 0.5, name, ha="center", va="center",
                fontsize=11, fontweight="bold", color="#333333")
    if regime in _pos:
        c, r = _pos[regime]
        ax.text(c + 0.5, r + 0.5, "★", ha="center", va="center",
                fontsize=22, color="#1565C0", zorder=5,
                fontfamily="DejaVu Sans")

    ax.set_title(
        f"현재 레짐: {regime}  (확신: {confidence})",
        fontsize=12, fontweight="bold", pad=12, color="#1A237E"
    )
    if regime == "Late-Cycle":
        ax.text(
            0.5, -0.12, "⚠ Late-Cycle: 성장 둔화 진입 이행 국면",
            transform=ax.transAxes, ha="center", fontsize=9,
            color="#546E7A", style="italic"
        )
    fig.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/regime_gauge_{date_str}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ 차트 저장: {path}")
    return path


def macro_dashboard(snapshot: dict, analysis: dict, date_str: str) -> str | None:
    """거시·디지털자산 지표 3-패널 대시보드 → PNG"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
        plt.rcParams["font.family"] = "NanumGothic"
        plt.rcParams["axes.unicode_minus"] = False
    except ImportError:
        return None

    macro = snapshot.get("macro", {})
    stable = snapshot.get("stablecoins", {})
    crypto = snapshot.get("crypto", {})
    regime = analysis.get("regime", {}).get("regime", "—")

    fed = _safe_float(macro.get("FEDFUNDS", {}).get("value"))
    dgs10 = _safe_float(macro.get("DGS10", {}).get("value"))
    krw = _safe_float(macro.get("DEXKOUS", {}).get("value"))

    fig = plt.figure(figsize=(14, 4.5))
    fig.patch.set_facecolor("#FAFAFA")
    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

    # ── 패널 1: 금리 현황 ────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    labels = ["Fed Funds", "10Y Treasury"]
    vals = [fed or 0, dgs10 or 0]
    colors = ["#EF5350", "#42A5F5"]
    bars = ax1.bar(labels, vals, color=colors, width=0.5, edgecolor="white", linewidth=1.5)
    for bar, v in zip(bars, vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, v + 0.05,
                 f"{v:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    if fed and dgs10:
        spread = dgs10 - fed
        ax1.annotate(
            f"Spread: {spread:+.2f}%p",
            xy=(0.5, max(vals) * 0.5), xycoords="data",
            ha="center", fontsize=9, color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4", alpha=0.8),
        )
    ax1.set_ylim(0, max(vals) * 1.35)
    ax1.set_title("금리 현황", fontsize=11, fontweight="bold", pad=8)
    ax1.set_ylabel("금리 (%)", fontsize=9)
    ax1.set_facecolor("#F8F9FA")
    ax1.spines[["top", "right"]].set_visible(False)

    # ── 패널 2: 스테이블코인 시장 ────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    syms = list(stable.keys())
    mcaps = [stable[s].get("market_cap", 0) or 0 for s in syms]
    total = sum(mcaps)
    pcts = [m / total * 100 if total else 0 for m in mcaps]
    pal = ["#1565C0", "#2196F3", "#90CAF9", "#BBDEFB"]
    ax2.barh(syms, pcts, color=pal[:len(syms)], edgecolor="white", linewidth=1.2)
    for i, (p, m) in enumerate(zip(pcts, mcaps)):
        ax2.text(p + 0.5, i, f"{p:.1f}%  (${m/1e9:.0f}B)",
                 va="center", fontsize=9, color="#333")
    ax2.set_xlim(0, (max(pcts) if pcts else 100) * 1.4)
    ax2.set_title(f"스테이블코인 도미넌스\n총 ${total/1e9:.0f}B", fontsize=11, fontweight="bold", pad=8)
    ax2.set_xlabel("도미넌스 (%)", fontsize=9)
    ax2.set_facecolor("#F8F9FA")
    ax2.spines[["top", "right"]].set_visible(False)

    # ── 패널 3: 암호화폐 + KRW ───────────────────────────────────────────
    ax3 = fig.add_subplot(gs[2])
    btc = crypto.get("BTC", {})
    eth = crypto.get("ETH", {})
    assets = ["BTC", "ETH"]
    changes = [btc.get("change_24h") or 0, eth.get("change_24h") or 0]
    bar_colors = ["#4CAF50" if c >= 0 else "#EF5350" for c in changes]
    bars3 = ax3.bar(assets, changes, color=bar_colors, width=0.45,
                    edgecolor="white", linewidth=1.5)
    for bar, c in zip(bars3, changes):
        ypos = c + 0.05 if c >= 0 else c - 0.35
        ax3.text(bar.get_x() + bar.get_width() / 2, ypos,
                 f"{c:+.1f}%", ha="center", fontsize=10, fontweight="bold")
    ax3.axhline(0, color="#999", linewidth=0.8)
    btc_price = btc.get("price", 0)
    eth_price = eth.get("price", 0)
    ax3.set_title(
        f"암호화폐 24h 수익률\nBTC ${btc_price:,.0f}  ETH ${eth_price:,.0f}",
        fontsize=11, fontweight="bold", pad=8,
    )
    ax3.set_ylabel("24h 변화 (%)", fontsize=9)
    ax3.set_facecolor("#F8F9FA")
    ax3.spines[["top", "right"]].set_visible(False)

    # ── 타이틀 ────────────────────────────────────────────────────────────
    krw_str = f"USD/KRW {krw:,.0f}" if krw else ""
    fig.suptitle(
        f"시장 스냅샷 ({date_str[:4]}-{date_str[4:6]}-{date_str[6:]})  |  레짐: {regime}  |  {krw_str}",
        fontsize=13, fontweight="bold", y=1.02, color="#1A237E",
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/macro_dashboard_{date_str}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓ 차트 저장: {path}")
    return path


def _safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def build_analysis_charts(analysis: dict, date_str: str = None,
                          snapshot: dict = None) -> dict:
    """분석 결과 → 레짐 게이지 + 매크로 대시보드 차트 생성"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y%m%d")
    paths = {}
    gauge = regime_gauge(analysis, date_str)
    if gauge:
        paths["regime_gauge"] = gauge
    if snapshot:
        dash = macro_dashboard(snapshot, analysis, date_str)
        if dash:
            paths["macro_dashboard"] = dash
    return paths


if __name__ == "__main__":
    result = build_charts()
    for k, v in result.items():
        print(f"  {k}: {v}")
