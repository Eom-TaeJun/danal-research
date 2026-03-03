# 목적: 거시경제 + 디지털자산 지표 → 레짐 판단 + 스테이블코인 시그널 + 다날 함의
# 입력: outputs/context/snapshot_*.json
# 출력: outputs/context/analysis_YYYYMMDD.json
# 레짐: Goldilocks / Overheating / Stagflation / Recession
# 제외: 기업 개별 분석, 포트폴리오 최적화

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = "outputs/context"
CONTEXT_DIR = "outputs/context"


# ── 스키마 ─────────────────────────────────────────────────────────────────

@dataclass
class RegimeResult:
    regime: str          # Goldilocks | Overheating | Stagflation | Recession
    confidence: str      # High | Medium | Low
    growth_dir: str      # positive | neutral | negative
    inflation_dir: str   # high | moderate | low
    rationale: list


@dataclass
class StablecoinResult:
    total_mcap_b: float
    usdt_dom_pct: float
    usdc_dom_pct: float
    btc_24h_pct: float
    flight_to_safety: bool
    signal: str          # bullish | neutral | bearish
    note: str


@dataclass
class DanalResult:
    stablecoin_saas: str
    payment_cashcow: str
    global_expansion: str
    watch_events: list


# ── 레짐 판단 ──────────────────────────────────────────────────────────────
# 성장 시그널: DGS10 - FEDFUNDS 스프레드 (수익률 곡선)
# 인플레이션 시그널: FEDFUNDS 레벨 (Fed 긴축 강도 프록시)
#
#              인플레↑(Fed≥4%)    인플레↓(Fed<3%)
# 성장+(spread≥+0.3)  Overheating     Goldilocks
# 성장-(spread≤-0.2)  Stagflation     Recession

_IMPLICATIONS = {
    "Goldilocks": {
        "stablecoin_saas": "성장 환경 최적 — 기업의 스테이블코인 결제 도입 수요 증가. SaaS 신규 계약 공략 타이밍.",
        "payment_cashcow": "소비 확장 국면 → 휴대폰결제 거래량 증가 예상. 캐시카우 수익 안정적.",
        "global_expansion": "위험자산 선호 → 글로벌 핀테크 투자 활성화. 해외 파트너십 협상 유리.",
        "watch_events": ["Fed 금리 동결/인하 확인", "스테이블코인 신규 발행 동향", "MiCA 집행 현황"],
    },
    "Overheating": {
        "stablecoin_saas": "고금리 → 준비금 이자 수익 최대화(Circle 모델). 다날 SaaS 수수료 모델은 금리 중립, 경쟁사 수익↑ 주의.",
        "payment_cashcow": "인플레이션 → 실질 구매력 감소, 고가 결제 거래 위축 가능.",
        "global_expansion": "긴축 환경 → 핀테크 밸류에이션 압박. 유기적 성장 전략이 인수합병보다 유리.",
        "watch_events": ["FOMC 성명 + 점도표", "CPI 발표일", "GENIUS Act 입법 동향"],
    },
    "Stagflation": {
        "stablecoin_saas": "불확실성 증가 → 스테이블코인 결제 도입 의사결정 지연 가능. 기존 고객 유지 집중.",
        "payment_cashcow": "경기 둔화 + 물가 상승 이중 압박 → 결제 수수료 수익 감소 위험.",
        "global_expansion": "EM 환율 변동성 확대 → KRW 약세 시 해외 결제 비용 증가. 환헤지 전략 필요.",
        "watch_events": ["USD/KRW 1,450 돌파 여부", "BOK 기준금리 결정", "국내 소비지출 지표"],
    },
    "Recession": {
        "stablecoin_saas": "안전자산 선호 → 스테이블코인 수요 증가. KRW 스테이블코인 헤지 니즈 확대.",
        "payment_cashcow": "소비 급감 → 거래량 감소. PCI 편의점 결제가 방어적 역할.",
        "global_expansion": "리스크오프 → 신규 투자 중단. 기존 인프라 효율화 및 비용 절감 집중.",
        "watch_events": ["실업률 발표", "소매판매 지표", "BOK 긴급 금리인하 가능성"],
    },
}


def _f(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def detect_regime(macro: dict) -> RegimeResult:
    fed = _f(macro.get("FEDFUNDS", {}).get("value"))
    dgs10 = _f(macro.get("DGS10", {}).get("value"))
    krw = _f(macro.get("DEXKOUS", {}).get("value"))
    rationale, growth_dir, inflation_dir = [], "neutral", "moderate"
    confidence = "Medium"

    if fed is not None and dgs10 is not None:
        spread = round(dgs10 - fed, 2)
        if spread >= 0.3:
            growth_dir = "positive"
            rationale.append(f"수익률 곡선 정상화 (10Y-FF spread: +{spread}%p) → 성장 기대")
        elif spread <= -0.2:
            growth_dir = "negative"
            rationale.append(f"수익률 곡선 역전 (spread: {spread}%p) → 경기 둔화 신호")
        else:
            rationale.append(f"수익률 곡선 평탄 (spread: {spread:+}%p) → 성장 불확실")

    if fed is not None:
        if fed >= 4.0:
            inflation_dir = "high"
            confidence = "High"
            rationale.append(f"Fed Funds {fed}% — 고금리 유지, 긴축 국면")
        elif fed < 3.0:
            inflation_dir = "low"
            confidence = "High"
            rationale.append(f"Fed Funds {fed}% — 완화 전환, 물가 안정")
        else:
            rationale.append(f"Fed Funds {fed}% — 완만한 긴축 (인플레이션 moderate)")

    if krw is not None and krw > 1450:
        rationale.append(f"⚠️ USD/KRW {krw:.0f} — BOK 개입 임계(1,500) 주시 필요")

    regime_map = {
        ("positive", "high"): "Overheating",
        ("positive", "moderate"): "Goldilocks",
        ("positive", "low"): "Goldilocks",
        ("neutral", "high"): "Overheating",
        ("neutral", "moderate"): "Goldilocks",
        ("neutral", "low"): "Goldilocks",
        ("negative", "high"): "Stagflation",
        ("negative", "moderate"): "Recession",
        ("negative", "low"): "Recession",
    }
    regime = regime_map.get((growth_dir, inflation_dir), "Goldilocks")
    if not rationale:
        rationale.append("데이터 부족 — 추가 수집 필요")
        confidence = "Low"

    return RegimeResult(regime=regime, confidence=confidence,
                        growth_dir=growth_dir, inflation_dir=inflation_dir,
                        rationale=rationale)


def analyze_stablecoins(stable: dict, crypto: dict) -> StablecoinResult:
    total = sum(v.get("market_cap", 0) or 0 for v in stable.values())
    total_b = round(total / 1e9, 1)
    usdt = stable.get("USDT", {}).get("market_cap", 0) or 0
    usdc = stable.get("USDC", {}).get("market_cap", 0) or 0
    usdt_dom = round(usdt / total * 100, 1) if total else 0
    usdc_dom = round(usdc / total * 100, 1) if total else 0
    btc_24h = round(crypto.get("BTC", {}).get("change_24h") or 0, 2)
    stab_7d = stable.get("USDT", {}).get("price_change_7d") or 0
    flight = stab_7d > 0.5 and btc_24h < -3.0

    if total_b >= 270:
        signal, note = "bullish", f"시총 ${total_b}B — 성장세 지속"
    elif total_b <= 200:
        signal, note = "bearish", f"시총 ${total_b}B — 수요 감소"
    else:
        signal, note = "neutral", f"시총 ${total_b}B — 안정권"
    if flight:
        note += " | ⚠️ 안전자산 선호 감지 (BTC↓ + 스테이블코인↑)"

    return StablecoinResult(total_mcap_b=total_b, usdt_dom_pct=usdt_dom,
                            usdc_dom_pct=usdc_dom, btc_24h_pct=btc_24h,
                            flight_to_safety=flight, signal=signal, note=note)


def analyze(snapshot: dict = None) -> dict:
    if snapshot is None:
        files = sorted(Path(CONTEXT_DIR).glob("snapshot_*.json"), reverse=True)
        if not files:
            return {"error": "snapshot 없음 — python main.py --brief 먼저 실행"}
        with open(files[0], encoding="utf-8") as f:
            snapshot = json.load(f)

    regime = detect_regime(snapshot.get("macro", {}))
    stablecoin = analyze_stablecoins(snapshot.get("stablecoins", {}),
                                     snapshot.get("crypto", {}))
    impl = _IMPLICATIONS[regime.regime]
    danal = DanalResult(**impl)

    result = {
        "analyzed_at": datetime.now().isoformat(),
        "source_snapshot": snapshot.get("collected_at", "unknown"),
        "regime": asdict(regime),
        "stablecoin_signal": asdict(stablecoin),
        "danal_implications": asdict(danal),
    }
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/analysis_{datetime.now().strftime('%Y%m%d')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 분석 저장: {path}")
    return result


if __name__ == "__main__":
    result = analyze()
    r = result.get("regime", {})
    s = result.get("stablecoin_signal", {})
    print(f"\n레짐: {r.get('regime')} ({r.get('confidence')})")
    print(f"스테이블코인: {s.get('note')}")
