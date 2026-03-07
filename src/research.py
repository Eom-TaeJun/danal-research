# 목적: Perplexity로 기업/섹터 정보 수집 → IM 초안용 컨텍스트 생성
# 입력: --company "[기업명]" 또는 --query "[검색어]"
# 출력: outputs/context/research_[기업명]_YYYYMMDD.json
# 실패 시: PERPLEXITY_API_KEY 없으면 빈 컨텍스트 반환
# 제외: 유료 데이터 벤더 API, 로그인 필요 소스

import json
import os
import argparse
import httpx
from datetime import datetime

OUTPUT_DIR = "outputs/context"
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

_RESEARCH_FALLBACK = {
    "summary": "", "business_model": "", "key_products": [],
    "market_size": "", "competitors": [], "bull_case": [],
    "bear_case": [], "recent_news": [], "risks": [],
    "financials_history": [], "valuation_metrics": {}, "management_team": [],
}


def research(company: str = "", query: str = "") -> dict:
    target = company or query
    if not target:
        return {"error": "company 또는 query 필요"}

    if not PERPLEXITY_API_KEY:
        print("  [research] PERPLEXITY_API_KEY 없음 — 빈 컨텍스트 반환")
        return {"company": company, "summary": "", "sources": []}

    prompt = (
        f"Provide a structured research summary for investment analysis of: {target}\n\n"
        "Format as JSON with exactly these keys:\n"
        "- summary: 2-3 sentence company overview\n"
        "- business_model: how they make money\n"
        "- key_products: list of 3-5 main products/services\n"
        "- market_size: TAM description and size estimate\n"
        "- competitors: list of top 3-5 competitors\n"
        "- bull_case: list of 3 reasons to invest\n"
        "- bear_case: list of 3 risks or reasons not to invest\n"
        "- recent_news: list of 3 most recent developments (last 6 months)\n"
        "- risks: list of top 3-5 key risks\n"
        "- financials_history: last 3 fiscal years with ACTUAL numbers (not null). "
        "List of {year (int), revenue_usd_millions (float e.g. 2750.0 for $2.75B), "
        "net_income_usd_millions (float, negative if loss), gross_margin_pct (float 0-100)}. "
        "Use reported figures; omit a field only if truly unverifiable.\n"
        "- valuation_metrics: {market_cap_usd_millions (float, latest known), "
        "ev_revenue_multiple (float), pe_ratio (float or null if loss-making), "
        "peer_avg_ev_revenue_multiple (float)}. "
        "For public companies use current market data; for private use last funding round.\n"
        "- management_team: list of top 3 executives {name, title, background_one_line}\n"
        "Return only valid JSON, no markdown."
    )

    print(f"  → Perplexity 리서치 중: {target}")
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {PERPLEXITY_API_KEY}"},
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": prompt}],
                }
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]

        # JSON 파싱 시도
        import re
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                print("  [research] JSON 파싱 실패 — fallback 구조 사용")
                parsed = {**_RESEARCH_FALLBACK, "raw": content}
        else:
            print("  [research] JSON 없음 — fallback 구조 사용")
            parsed = {**_RESEARCH_FALLBACK, "raw": content}
    except Exception as e:
        print(f"  [research] 실패: {e}")
        parsed = {"error": str(e)}

    result = {"company": company, "query": query,
              "collected_at": datetime.now().isoformat(), **parsed}

    # 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_name = company.replace(" ", "_").replace("/", "-") if company else "query"
    date_str = datetime.now().strftime("%Y%m%d")
    path = f"{OUTPUT_DIR}/research_{safe_name}_{date_str}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 저장: {path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", default="")
    parser.add_argument("--query", default="")
    args = parser.parse_args()
    research(company=args.company, query=args.query)
