# 목적: 거시경제 + 스테이블코인 핵심 지표 수집
# 입력: --mode [brief|stablecoin|screen] --sector [optional]
# 출력: outputs/context/snapshot_YYYYMMDD.json
# 실패 시: 소스별 독립 실패 — 일부 실패해도 수집 계속
# 제외: 실시간 스트리밍, WebSocket, DB 저장

import json
import os
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


def collect(mode: str = "brief", sector: str = "stablecoin") -> dict:
    print(f"[collect] mode={mode} sector={sector}")
    snapshot = {"collected_at": datetime.now().isoformat(), "mode": mode}

    # 거시경제 (공통)
    print("  → FRED 수집 중...")
    snapshot["macro"] = fetch_fred(["FEDFUNDS", "DGS10", "DEXKOUS", "CPIAUCSL"])

    # 디지털자산 (brief, stablecoin, screen)
    print("  → CoinGecko 수집 중...")
    snapshot["stablecoins"] = fetch_coingecko_stablecoins()
    snapshot["crypto"] = fetch_crypto_prices()

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
                        choices=["brief", "stablecoin", "screen"])
    parser.add_argument("--sector", default="stablecoin")
    args = parser.parse_args()
    collect(mode=args.mode, sector=args.sector)
