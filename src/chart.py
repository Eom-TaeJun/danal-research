# 목적: 수집된 snapshot 데이터 → 시각화 차트 PNG 생성
# 입력: outputs/context/snapshot_*.json
# 출력: outputs/charts/[name]_YYYYMMDD.png  (상대 경로 반환)
# 실패 시: matplotlib 없거나 데이터 없으면 None 반환
# 제외: 인터랙티브 차트, 웹 대시보드, 실시간 스트리밍

import json
import os
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = "outputs/charts"
CONTEXT_DIR = "outputs/context"


def load_latest(pattern: str) -> dict:
    files = sorted(Path(CONTEXT_DIR).glob(pattern), reverse=True)
    if not files:
        return {}
    with open(files[0], encoding="utf-8") as f:
        return json.load(f)


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


if __name__ == "__main__":
    result = build_charts()
    for k, v in result.items():
        print(f"  {k}: {v}")
