# 목적: 거시경제 + 스테이블코인 핵심 지표 수집
# 입력: --mode [brief|stablecoin|screen] --sector [optional]
# 출력: outputs/context/snapshot_YYYYMMDD.json
# 실패 시: 소스별 독립 실패 — 일부 실패해도 수집 계속
# 제외: 실시간 스트리밍, WebSocket, DB 저장

import json
import os
import re
import argparse
import requests
from datetime import datetime, timedelta

OUTPUT_DIR = "outputs/context"


def fetch_fred(series_ids: list[str]) -> dict:
    """FRED 거시경제 지표 수집"""
    api_key = os.getenv("FRED_API_KEY", "")
    result = {}
    for sid in series_ids:
        try:
            r = requests.get(
                "https://api.stlouisfed.org/fred/series/observations",
                params={"series_id": sid, "api_key": api_key,
                        "file_type": "json", "sort_order": "desc", "limit": 2},
                timeout=10
            )
            r.raise_for_status()
            obs = r.json().get("observations", [])
            if obs:
                result[sid] = {"value": obs[0]["value"], "date": obs[0]["date"]}
        except Exception as e:
            print(f"  [FRED] {sid} 실패: {e}")
    return result


def fetch_coingecko_stablecoins() -> dict:
    """CoinGecko 스테이블코인 시총·거래량 수집"""
    coins = ["tether", "usd-coin", "dai", "first-digital-usd"]
    result = {}
    try:
        ids = ",".join(coins)
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={"vs_currency": "usd", "ids": ids,
                    "price_change_percentage": "7d"},
            timeout=10
        )
        r.raise_for_status()
        for coin in r.json():
            result[coin["symbol"].upper()] = {
                "market_cap": coin.get("market_cap"),
                "volume_24h": coin.get("total_volume"),
                "price_change_7d": coin.get("price_change_percentage_7d_in_currency"),
            }
    except Exception as e:
        print(f"  [CoinGecko] 실패: {e}")
    return result


def fetch_crypto_prices() -> dict:
    """BTC, ETH 가격 수집"""
    result = {}
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin,ethereum",
                    "vs_currencies": "usd",
                    "include_24hr_change": "true"},
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        result["BTC"] = {"price": data["bitcoin"]["usd"],
                         "change_24h": data["bitcoin"].get("usd_24h_change")}
        result["ETH"] = {"price": data["ethereum"]["usd"],
                         "change_24h": data["ethereum"].get("usd_24h_change")}
    except Exception as e:
        print(f"  [CoinGecko prices] 실패: {e}")
    return result


def fetch_fintech_news() -> dict:
    """Perplexity로 핀테크·디지털자산 주간 뉴스 + 투자 시사점 수집"""
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    if not api_key:
        return {}
    prompt = (
        "Summarize the top 3 fintech and digital asset news from the past 7 days. "
        "Return JSON only: {\"items\": [{\"title\": \"...\", \"summary\": \"one sentence\"}], "
        "\"implications\": [\"ko: 투자 시사점 1\", \"ko: 시사점 2\", \"ko: 시사점 3\"]}. "
        "Focus on: stablecoins, crypto regulation, global payments, central bank policy. "
        "Write implications in Korean. Return only valid JSON, no markdown."
    )
    try:
        import httpx
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": "sonar", "messages": [{"role": "user", "content": prompt}]},
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            return {}
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print("  [뉴스] JSON 파싱 실패")
            return {}
    except Exception as e:
        print(f"  [뉴스] 수집 실패: {e}")
        return {}


def fetch_fred_history(series_ids: list[str], months: int = 12) -> dict:
    """FRED 시계열 데이터 수집 (최근 N개월) — 차트용"""
    api_key = os.getenv("FRED_API_KEY", "")
    start = (datetime.now() - timedelta(days=months * 31)).strftime("%Y-%m-%d")
    result = {}
    for sid in series_ids:
        try:
            r = requests.get(
                "https://api.stlouisfed.org/fred/series/observations",
                params={"series_id": sid, "api_key": api_key,
                        "file_type": "json", "observation_start": start,
                        "sort_order": "asc"},
                timeout=15,
            )
            r.raise_for_status()
            obs = r.json().get("observations", [])
            result[sid] = [
                {"date": o["date"], "value": o["value"]}
                for o in obs if o["value"] != "."
            ]
        except Exception as e:
            print(f"  [FRED history] {sid} 실패: {e}")
    return result


def fetch_btc_history(days: int = 90) -> list[dict]:
    """CoinGecko BTC 일별 가격 히스토리 (vol ratio 계산용)"""
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
            params={"vs_currency": "usd", "days": days, "interval": "daily"},
            timeout=15,
        )
        r.raise_for_status()
        prices = r.json().get("prices", [])
        return [
            {"date": datetime.fromtimestamp(p[0] / 1000).strftime("%Y-%m-%d"),
             "price": p[1]}
            for p in prices
        ]
    except Exception as e:
        print(f"  [CoinGecko history] BTC 실패: {e}")
        return []


def collect_danal_financials() -> dict:
    """다날 공식 재무정보 (공시 기반 하드코딩 — API 없음)"""
    return {
        "source": "다날 공식 재무정보 (danal.co.kr/invest/financial)",
        "unit": "억원 (연결)",
        "annual": [
            {"year": 2021, "revenue": 2648, "operating_income": 257, "pretax_income": 52},
            {"year": 2022, "revenue": 2553, "operating_income": 245, "pretax_income": -58},
            {"year": 2023, "revenue": 2468, "operating_income": 209, "pretax_income": -210},
            {"year": 2024, "revenue": 2118, "operating_income": 136, "pretax_income": -355},
            {"year": 2025, "revenue": 1945, "operating_income": 150, "pretax_income": -611},
        ],
        "note": "영업이익은 PG 본업 효율화로 반등, 세전순이익 적자는 블록체인 투자 영업외손실 누적",
    }


def collect(mode: str = "brief", sector: str = "stablecoin") -> dict:
    print(f"[collect] mode={mode} sector={sector}")
    snapshot = {"collected_at": datetime.now().isoformat(), "mode": mode}

    # 거시경제 (공통)
    print("  → FRED 수집 중...")
    snapshot["macro"] = fetch_fred(["FEDFUNDS", "DGS2", "DGS10", "DEXKOUS", "CPIAUCSL"])

    # 디지털자산 (brief, stablecoin, screen)
    print("  → CoinGecko 수집 중...")
    snapshot["stablecoins"] = fetch_coingecko_stablecoins()
    snapshot["crypto"] = fetch_crypto_prices()

    # 핀테크 뉴스 (brief 모드)
    if mode == "brief":
        print("  → 핀테크 뉴스 수집 중...")
        snapshot["news"] = fetch_fintech_news()

    # 시계열 + 다날 재무 (deep 모드)
    if mode == "deep":
        print("  → FRED 시계열 수집 중 (12개월)...")
        snapshot["fred_history"] = fetch_fred_history(
            ["FEDFUNDS", "DGS10", "DEXKOUS"], months=12
        )
        print("  → BTC 가격 히스토리 수집 중 (90일)...")
        snapshot["btc_history"] = fetch_btc_history(days=90)
        print("  → 다날 재무정보 로드 중...")
        snapshot["danal_financials"] = collect_danal_financials()

    # 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = f"{OUTPUT_DIR}/snapshot_{date_str}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 저장: {path}")
    return snapshot


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="brief",
                        choices=["brief", "stablecoin", "screen", "deep"])
    parser.add_argument("--sector", default="stablecoin")
    args = parser.parse_args()
    collect(mode=args.mode, sector=args.sector)
