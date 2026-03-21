# 목적: Markdown 리포트 → HTML 변환 + 대시보드 생성
# 입력: outputs/reports/*.md + outputs/charts/*.png
# 출력: outputs/html/index.html + 개별 리포트 HTML
# 의존: markdown, jinja2

import os
import re
import shutil
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

REPORT_DIR = Path("outputs/reports")
CHART_DIR = Path("outputs/charts")
HTML_DIR = Path("outputs/html")
TEMPLATE_DIR = Path("templates")

_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=False)
_md = markdown.Markdown(extensions=["tables", "toc", "fenced_code"])

# 리포트 메타데이터 (3단계 분류 + 설명)
REPORT_META = {
    "danal_business_position": {
        "stage": 1, "type": "Business Position",
        "desc": "IR + financials analysis. PG defense vs blockchain investment structure.",
    },
    "master_research_report": {
        "stage": 2, "type": "Master Research",
        "desc": "Macro regime, sector screening, company analysis with 27 sources.",
    },
    "circle_s1_analysis": {
        "stage": 2, "type": "S-1 Analysis",
        "desc": "Circle SEC S-1 filing deep dive. Revenue structure, risk factors.",
    },
    "deep_stablecoin": {
        "stage": 2, "type": "Deep Analysis",
        "desc": "Market structure + regulation + 4-axis risk scoring + stress test.",
    },
    "brief": {
        "stage": 2, "type": "Weekly Brief",
        "desc": "Macro snapshot + stablecoin market + investment implications.",
    },
    "decision_memo_Circle": {
        "stage": 3, "type": "Decision Memo",
        "desc": "1-page investment decision. Partnership over equity investment.",
    },
    "shortlist_priority_memo": {
        "stage": 3, "type": "Priority Memo",
        "desc": "Shortlisted companies ranked by strategic fit.",
    },
    "im_Circle": {"stage": 0, "type": "IM", "desc": "Circle investment memo."},
    "im_Ripple": {"stage": 0, "type": "IM", "desc": "Ripple investment memo."},
    "screen_stablecoin": {"stage": 0, "type": "Screening", "desc": "Sector screening."},
    "regime_report": {"stage": 0, "type": "Regime", "desc": "Regime analysis."},
}

# 최신 차트만 (dashboard 표시용)
HERO_CHARTS = [
    ("macro_dashboard", "Macro Dashboard"),
    ("regime_gauge", "Regime Gauge"),
    ("stablecoin_pie", "Stablecoin Market Share"),
    ("macro_timeseries", "Macro 12-Month Trend"),
    ("danal_financial", "Danal Financial Trend"),
]


def _extract_title(md_text: str) -> str:
    m = re.match(r"^#\s+(.+)", md_text)
    return m.group(1) if m else "Untitled"


def _extract_date(filename: str) -> str:
    m = re.search(r"(\d{8})", filename)
    if m:
        d = m.group(1)
        return f"{d[:4]}-{d[4:6]}-{d[6:]}"
    return ""


def _classify(filename: str) -> dict:
    stem = Path(filename).stem
    for prefix, meta in REPORT_META.items():
        if stem.startswith(prefix):
            return meta
    return {"stage": 0, "type": "Report", "desc": ""}


def _fix_img_paths(html: str) -> str:
    return html.replace("../charts/", "charts/")


def convert_report(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    title = _extract_title(text)
    date = _extract_date(md_path.name)
    meta = _classify(md_path.name)
    _md.reset()
    body = _fix_img_paths(_md.convert(text))
    tmpl = _env.get_template("report.html")
    html = tmpl.render(title=title, date=date, body=body, report_type=meta["type"])
    out = HTML_DIR / md_path.with_suffix(".html").name
    out.write_text(html, encoding="utf-8")
    return str(out)


def _latest_chart(prefix: str) -> Path | None:
    matches = sorted(CHART_DIR.glob(f"{prefix}_*.png"), reverse=True)
    return matches[0] if matches else None


def build_dashboard() -> str:
    reports = sorted(REPORT_DIR.glob("*.md"), reverse=True)
    seen_prefixes: set[str] = set()
    stage1, stage2, stage3, supporting = [], [], [], []

    for r in reports:
        meta = _classify(r.name)
        # 같은 타입은 최신 1개만
        prefix = re.sub(r"_\d{8}\.md$", "", r.name)
        if prefix in seen_prefixes:
            continue
        seen_prefixes.add(prefix)

        entry = {
            "filename": r.with_suffix(".html").name,
            "title": _extract_title(r.read_text(encoding="utf-8")),
            "type": meta["type"],
            "desc": meta["desc"],
        }
        if meta["stage"] == 1:
            stage1.append(entry)
        elif meta["stage"] == 2:
            stage2.append(entry)
        elif meta["stage"] == 3:
            stage3.append(entry)
        else:
            supporting.append(entry)

    charts = []
    for prefix, alt in HERO_CHARTS:
        p = _latest_chart(prefix)
        if p:
            charts.append({"path": f"charts/{p.name}", "alt": alt})

    tmpl = _env.get_template("dashboard.html")
    html = tmpl.render(stage1=stage1, stage2=stage2, stage3=stage3,
                       supporting=supporting, charts=charts)
    out = HTML_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    return str(out)


def build_all() -> list[str]:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    # 차트 복사
    dst = HTML_DIR / "charts"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(CHART_DIR, dst)

    paths = []
    for md in sorted(REPORT_DIR.glob("*.md")):
        paths.append(convert_report(md))

    paths.append(build_dashboard())
    print(f"  HTML {len(paths)}건 생성: {HTML_DIR}/")
    return paths
