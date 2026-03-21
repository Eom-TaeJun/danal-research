# 목적: 거시경제 + 디지털자산 지표 → 레짐 판단 + 스테이블코인 시그널 + 다날 함의
# 입력: outputs/context/snapshot_*.json
# 출력: outputs/context/analysis_YYYYMMDD.json
# 레짐: Goldilocks / Overheating / Late-Cycle / Stagflation / Recession
# 제외: 기업 개별 분석, 포트폴리오 최적화
#
# ── 2026-03-06 업데이트: 다중 신호 합산 + 신호별 추론 기록 + 신뢰도 가중치

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = "outputs/context"
CONTEXT_DIR = "outputs/context"


# ── 스키마 ─────────────────────────────────────────────────────────────────

@dataclass
class Signal:
    """단일 분석 신호 — 이름 · 방향 · 값 · 신뢰 가중치"""
    name: str
    direction: str     # positive | neutral | negative
    value: str         # 실제 값 문자열 (출처 포함)
    weight: float      # 0.0 ~ 1.0
    rationale: str


@dataclass
class RegimeResult:
    regime: str           # Goldilocks | Overheating | Late-Cycle | Stagflation | Recession
    confidence: str       # High | Medium | Low
    confidence_score: float  # 0.0~1.0 (신호 가중 합산)
    growth_dir: str       # positive | neutral | negative
    inflation_dir: str    # high | moderate | low
    signals: list         # List[Signal] → CoT 추론 로그
    rationale: list       # 사람이 읽는 요약 (보고서용)
    alert_flags: list     # 즉시 경보 조건


@dataclass
class StablecoinResult:
    total_mcap_b: float
    usdt_dom_pct: float
    usdc_dom_pct: float
    btc_24h_pct: float
    flight_to_safety: bool
    signal: str           # bullish | neutral | bearish
    signal_score: float   # -1.0 ~ +1.0
    note: str
    adoption_phase: str   # early | growth | saturation


@dataclass
class DanalResult:
    stablecoin_saas: str
    payment_cashcow: str
    global_expansion: str
    x402_ai: str          # 신규 추가: x402 / AI 결제 축
    watch_events: list
    priority_action: str  # 이번 주 가장 중요한 단 하나의 행동


# ── 레짐 함의 ──────────────────────────────────────────────────────────────

def build_implications(regime: str, macro: dict, stablecoin_result: StablecoinResult) -> dict:
    fed = _f(macro.get("FEDFUNDS", {}).get("value"))
    krw = _f(macro.get("DEXKOUS", {}).get("value"))
    fed = fed if fed is not None else 4.0
    krw = krw if krw is not None else 1400.0
    phase = stablecoin_result.adoption_phase
    total_b = stablecoin_result.total_mcap_b

    if regime == "Goldilocks" and phase == "growth":
        stablecoin_saas = (
            f"Growth 단계(${total_b:.1f}B) — KRW SaaS 신규 계약 공략 최적 타이밍"
        )
    elif regime == "Goldilocks" and phase == "saturation":
        stablecoin_saas = (
            f"채택 포화 진입 (${total_b:.1f}B) — 점유율 경쟁 심화, 수수료 차별화 필요"
        )
    elif regime == "Overheating" and fed >= 4.5:
        stablecoin_saas = (
            f"Fed {fed:.1f}% 고금리 — Circle 준비금 이자 모델 경쟁 우위. "
            "다날 SaaS는 금리 중립이나 경쟁사 체력 강화 주의"
        )
    elif regime == "Overheating":
        stablecoin_saas = f"온건 긴축({fed:.1f}%) — SaaS 계약 속도 유지 가능"
    elif regime == "Stagflation":
        stablecoin_saas = (
            "불확실성 증가 — 스테이블코인 도입 결정 지연. 기존 고객 유지 집중"
        )
    elif regime == "Recession":
        stablecoin_saas = (
            "안전자산 선호 → KRW 스테이블코인 헤지 니즈 확대. 선점 서사 강화 타이밍"
        )
    elif regime == "Late-Cycle":
        stablecoin_saas = (
            "성장 둔화 진입 — 기존 계약 리텐션 우선, 신규 보수적 접근"
        )
    else:
        stablecoin_saas = "KRW SaaS 전략 재점검 필요"

    if krw > 1450:
        payment_cashcow = (
            f"USD/KRW {krw:.0f} 원화 약세 — 수입 비용↑, PCI 편의점 방어 역할 중요"
        )
    else:
        payment_cashcow_map = {
            "Goldilocks": "소비 안정 구간 — 휴대폰결제 거래량 방어 가능",
            "Overheating": "물가 부담 확대 — PCI 편의점 결제가 방어선 역할",
            "Stagflation": "경기 둔화 + 비용 부담 — 캐시카우 수익성 방어 우선",
            "Recession": "소비 위축 국면 — 생활밀착 결제 중심 방어 필요",
            "Late-Cycle": "소비 둔화 초입 — 고마진 가맹점 리텐션 관리 우선",
        }
        payment_cashcow = payment_cashcow_map.get(
            regime, "결제 캐시카우 모니터링 필요"
        )

    if regime == "Goldilocks" and krw < 1400:
        global_expansion = (
            "K.ONDA 출시(4월) 최적 환경 — 외국인 결제 채산성 양호"
        )
    elif krw > 1450:
        global_expansion = (
            f"KRW 약세({krw:.0f}) — K.ONDA 외국인 결제 수익성 점검 필요"
        )
    else:
        global_expansion_map = {
            "Goldilocks": "K.ONDA 출시 준비 지속 — 파트너십 확장 여건 양호",
            "Overheating": "긴축 환경 — 파트너십 확장보다 단위경제 점검 우선",
            "Stagflation": "환율·수요 변동성 확대 — 해외 결제 확장 속도 조절",
            "Recession": "리스크오프 국면 — 신규 국가 확장보다 기존 파트너 효율화",
            "Late-Cycle": "성장 둔화 구간 — K.ONDA 초기 KPI를 보수적으로 관리",
        }
        global_expansion = global_expansion_map.get(
            regime, "글로벌 확장 전략 재점검 필요"
        )

    if regime in {"Goldilocks", "Overheating"}:
        x402_ai = "AI 서비스 투자 활성 — x402 에이전트 결제 수요 증가"
    elif regime in {"Stagflation", "Late-Cycle"}:
        x402_ai = "AI 비용효율 압박 → x402 도입 명분 강화"
    elif regime == "Recession":
        x402_ai = "AI 자동화로 비용 절감 압력 → x402 장기 긍정 시그널"
    else:
        x402_ai = "x402 수요 신호 추가 확인 필요"

    watch_events = []
    if fed >= 4.5:
        watch_events.append(f"FOMC 점도표 — {fed:.1f}% 고금리 인하 시점 확인")
    if krw > 1440:
        watch_events.append(f"BOK 개입 여부 — USD/KRW {krw:.0f}")
    if phase == "growth":
        watch_events.append("KRW SaaS 신규 계약 공시")
    watch_events.extend([
        "K.ONDA 4월 출시 KPI",
        "디지털자산기본법 세부 규정",
    ])

    if krw > 1480:
        priority_action = (
            f"긴급: USD/KRW {krw:.0f} 급등 대응 — KRW SaaS 리스크 보고"
        )
    elif regime == "Stagflation":
        priority_action = "캐시카우 방어 — 기존 가맹점 이탈 방지 우선"
    elif regime == "Goldilocks" and phase == "growth":
        priority_action = (
            "K.ONDA × Binance × Circle 출시 준비 상황 모니터링 (4월 출시)"
        )
    elif regime == "Overheating" and fed >= 4.5:
        priority_action = (
            "Circle IM 투자의견 재검토 — 고금리 지속 시 준비금 수익 상향"
        )
    elif regime == "Late-Cycle":
        priority_action = (
            "다날 캐시카우 수익 방어 집중 — 신규보다 리텐션 우선"
        )
    else:
        priority_action = "K.ONDA 출시 KPI 선제 설정"

    return {
        "stablecoin_saas": stablecoin_saas,
        "payment_cashcow": payment_cashcow,
        "global_expansion": global_expansion,
        "x402_ai": x402_ai,
        "watch_events": watch_events,
        "priority_action": priority_action,
    }


# ── 신호 수집기 ────────────────────────────────────────────────────────────

def _f(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def collect_growth_signals(macro: dict) -> list:
    """성장 방향 신호 수집 (다중 지표 병렬 평가)"""
    signals = []
    fed = _f(macro.get("FEDFUNDS", {}).get("value"))
    dgs10 = _f(macro.get("DGS10", {}).get("value"))
    dgs2 = _f(macro.get("DGS2", {}).get("value"))   # 2년물 (역전 여부)

    # 신호 1: 10Y-FF 스프레드 (수익률 곡선 정상화)
    if fed is not None and dgs10 is not None:
        spread_10ff = round(dgs10 - fed, 2)
        if spread_10ff >= 0.3:
            signals.append(Signal(
                name="yield_curve_10y_ff",
                direction="positive",
                value=f"+{spread_10ff}%p (FRED DGS10·FEDFUNDS)",
                weight=0.40,
                rationale=f"10Y-FF spread +{spread_10ff}%p → 수익률 곡선 정상화, 경기 확장 기대"
            ))
        elif spread_10ff <= -0.2:
            signals.append(Signal(
                name="yield_curve_10y_ff",
                direction="negative",
                value=f"{spread_10ff}%p (FRED DGS10·FEDFUNDS)",
                weight=0.40,
                rationale=f"10Y-FF spread {spread_10ff}%p → 수익률 곡선 역전, 경기 침체 선행 신호"
            ))
        else:
            signals.append(Signal(
                name="yield_curve_10y_ff",
                direction="neutral",
                value=f"{spread_10ff:+}%p (FRED DGS10·FEDFUNDS)",
                weight=0.20,
                rationale=f"10Y-FF spread {spread_10ff:+}%p → 평탄, 성장 방향 불명확"
            ))

    # 신호 2: 2Y-10Y 스프레드 (단기 역전 지속성 확인)
    # neutral 구간 추가: -0.1 ~ +0.2 → Late-Cycle 이행 신호
    if dgs2 is not None and dgs10 is not None:
        spread_2_10 = round(dgs10 - dgs2, 2)
        if spread_2_10 >= 0.2:
            signals.append(Signal(
                name="yield_curve_2y_10y",
                direction="positive",
                value=f"+{spread_2_10}%p (FRED DGS2·DGS10)",
                weight=0.25,
                rationale=f"2Y-10Y spread +{spread_2_10}%p → 정상 곡선, 경기 확장 확인"
            ))
        elif spread_2_10 <= -0.1:
            signals.append(Signal(
                name="yield_curve_2y_10y",
                direction="negative",
                value=f"{spread_2_10}%p (FRED DGS2·DGS10)",
                weight=0.25,
                rationale=f"2Y-10Y spread {spread_2_10}%p → 역전 지속, 침체 리스크 상존"
            ))
        else:
            signals.append(Signal(
                name="yield_curve_2y_10y",
                direction="neutral",
                value=f"{spread_2_10:+}%p (FRED DGS2·DGS10)",
                weight=0.10,
                rationale=f"2Y-10Y spread {spread_2_10:+}%p → 평탄 구간, 성장 방향 불명확 (Late-Cycle 신호)"
            ))

    return signals


def collect_inflation_signals(macro: dict) -> list:
    """인플레이션 방향 신호 수집"""
    signals = []
    fed = _f(macro.get("FEDFUNDS", {}).get("value"))
    dgs10 = _f(macro.get("DGS10", {}).get("value"))
    dgs2 = _f(macro.get("DGS2", {}).get("value"))

    # 신호 3: Fed Funds 레벨 (긴축 강도)
    if fed is not None:
        if fed >= 4.5:
            signals.append(Signal(
                name="fed_funds_level",
                direction="high",  # 인플레이션 high
                value=f"{fed}% (FRED FEDFUNDS)",
                weight=0.50,
                rationale=f"Fed Funds {fed}% — 강한 긴축, 인플레이션 억제 의지 명확"
            ))
        elif fed >= 3.5:
            signals.append(Signal(
                name="fed_funds_level",
                direction="moderate",
                value=f"{fed}% (FRED FEDFUNDS)",
                weight=0.35,
                rationale=f"Fed Funds {fed}% — 완만한 긴축, 인플레이션 moderate 구간"
            ))
        else:
            signals.append(Signal(
                name="fed_funds_level",
                direction="low",  # 인플레이션 low
                value=f"{fed}% (FRED FEDFUNDS)",
                weight=0.50,
                rationale=f"Fed Funds {fed}% — 완화 기조, 물가 안정 확인"
            ))

    # 신호 4: 10Y 실질금리 프록시 (10Y 레벨)
    if dgs10 is not None:
        if dgs10 >= 4.5:
            signals.append(Signal(
                name="10y_yield_level",
                direction="high",
                value=f"{dgs10}% (FRED DGS10)",
                weight=0.20,
                rationale=f"10Y 국채 {dgs10}% — 인플레이션 프리미엄 반영된 고금리"
            ))
        elif dgs10 <= 3.5:
            signals.append(Signal(
                name="10y_yield_level",
                direction="low",
                value=f"{dgs10}% (FRED DGS10)",
                weight=0.20,
                rationale=f"10Y 국채 {dgs10}% — 디플레이션 우려 또는 안전자산 선호"
            ))
        else:
            signals.append(Signal(
                name="10y_yield_level",
                direction="moderate",
                value=f"{dgs10}% (FRED DGS10)",
                weight=0.10,
                rationale=f"10Y 국채 {dgs10}% — 중립 구간"
            ))

    return signals


def collect_risk_signals(macro: dict, crypto: dict, stable: dict) -> list:
    """위험선호 및 경보 신호 수집"""
    signals = []
    krw = _f(macro.get("DEXKOUS", {}).get("value"))
    btc_24h = crypto.get("BTC", {}).get("change_24h") or 0
    total_mcap = sum(v.get("market_cap", 0) or 0 for v in stable.values()) / 1e9

    # 신호 5: USD/KRW 환율 경보
    if krw is not None:
        if krw > 1500:
            signals.append(Signal(
                name="usd_krw_alert",
                direction="negative",
                value=f"{krw:.0f} (FRED DEXKOUS)",
                weight=0.30,
                rationale=f"⚠️ USD/KRW {krw:.0f} — BOK 개입 임계(1,500) 돌파, KRW SaaS 리스크"
            ))
        elif krw > 1440:
            signals.append(Signal(
                name="usd_krw_watch",
                direction="neutral",
                value=f"{krw:.0f} (FRED DEXKOUS)",
                weight=0.10,
                rationale=f"USD/KRW {krw:.0f} — 원화 약세 지속, KRW SaaS 수출 경쟁력 유리"
            ))

    # 신호 6: BTC 모멘텀 (위험자산 선호 대리변수)
    btc_24h = round(float(btc_24h), 2)
    if btc_24h >= 5:
        signals.append(Signal(
            name="btc_momentum",
            direction="positive",
            value=f"+{btc_24h}% 24h (CoinGecko)",
            weight=0.15,
            rationale=f"BTC +{btc_24h}% — 강한 위험선호, 디지털자산 全 채택 증가 신호"
        ))
    elif btc_24h <= -5:
        signals.append(Signal(
            name="btc_momentum",
            direction="negative",
            value=f"{btc_24h}% 24h (CoinGecko)",
            weight=0.15,
            rationale=f"BTC {btc_24h}% — 위험회피, 스테이블코인 안전자산 선호 가능성"
        ))

    # 신호 7: 스테이블코인 시총 레벨
    if total_mcap >= 270:
        signals.append(Signal(
            name="stablecoin_mcap",
            direction="positive",
            value=f"${total_mcap:.1f}B (CoinGecko)",
            weight=0.10,
            rationale=f"스테이블코인 시총 ${total_mcap:.1f}B — 사상 최고권, 채택 가속 신호"
        ))
    elif total_mcap <= 200:
        signals.append(Signal(
            name="stablecoin_mcap",
            direction="negative",
            value=f"${total_mcap:.1f}B (CoinGecko)",
            weight=0.10,
            rationale=f"스테이블코인 시총 ${total_mcap:.1f}B — 수요 감소, 채택 역행"
        ))

    return signals


# ── 레짐 판단 (가중 신호 합산) ───────────────────────────────────

def detect_regime(macro: dict, crypto: dict = None, stable: dict = None) -> RegimeResult:
    """
    다중 신호를 수집하고 가중 합산으로 레짐 판단.
    모든 신호는 signals 리스트에 보존.
    """
    crypto = crypto or {}
    stable = stable or {}

    growth_signals = collect_growth_signals(macro)
    inflation_signals = collect_inflation_signals(macro)
    risk_signals = collect_risk_signals(macro, crypto, stable)

    all_signals = growth_signals + inflation_signals + risk_signals

    # 성장 방향 가중 투표
    growth_score = 0.0
    growth_total_w = sum(s.weight for s in growth_signals)
    for s in growth_signals:
        if s.direction == "positive":
            growth_score += s.weight
        elif s.direction == "negative":
            growth_score -= s.weight
    growth_norm = growth_score / growth_total_w if growth_total_w > 0 else 0
    if growth_norm >= 0.2:
        growth_dir = "positive"
    elif growth_norm <= -0.2:
        growth_dir = "negative"
    else:
        growth_dir = "neutral"

    # 인플레이션 방향 가중 투표
    infl_score = 0.0
    infl_total_w = sum(s.weight for s in inflation_signals)
    for s in inflation_signals:
        if s.direction == "high":
            infl_score += s.weight
        elif s.direction == "low":
            infl_score -= s.weight
    infl_norm = infl_score / infl_total_w if infl_total_w > 0 else 0
    if infl_norm >= 0.3:
        inflation_dir = "high"
    elif infl_norm <= -0.3:
        inflation_dir = "low"
    else:
        inflation_dir = "moderate"

    # 레짐 매핑
    regime_map = {
        ("positive", "high"):     "Overheating",
        ("positive", "moderate"): "Goldilocks",
        ("positive", "low"):      "Goldilocks",
        ("neutral",  "high"):     "Late-Cycle",
        ("neutral",  "moderate"): "Late-Cycle",
        ("neutral",  "low"):      "Late-Cycle",
        ("negative", "high"):     "Stagflation",
        ("negative", "moderate"): "Recession",
        ("negative", "low"):      "Recession",
    }
    regime = regime_map.get((growth_dir, inflation_dir), "Goldilocks")

    # 신뢰도 점수: 신호 수 + 방향 일관성
    signal_count = len(all_signals)
    consistency = abs(growth_norm) + abs(infl_norm)
    confidence_score = min(1.0, (signal_count / 7) * 0.6 + consistency * 0.4)
    if confidence_score >= 0.7:
        confidence = "High"
    elif confidence_score >= 0.4:
        confidence = "Medium"
    else:
        confidence = "Low"

    # 경보 플래그
    alert_flags = []
    for s in risk_signals:
        if "alert" in s.name or s.direction == "negative":
            alert_flags.append(s.rationale)

    # 사람이 읽는 요약
    rationale = [s.rationale for s in all_signals
                 if s.direction != "neutral" and s.direction != "moderate"]

    return RegimeResult(
        regime=regime,
        confidence=confidence,
        confidence_score=round(confidence_score, 2),
        growth_dir=growth_dir,
        inflation_dir=inflation_dir,
        signals=[asdict(s) for s in all_signals],
        rationale=rationale or ["데이터 부족 — 추가 수집 필요"],
        alert_flags=alert_flags,
    )


# ── 스테이블코인 분석 ──────────────────────────────────────────────────────

def analyze_stablecoins(stable: dict, crypto: dict) -> StablecoinResult:
    total = sum(v.get("market_cap", 0) or 0 for v in stable.values())
    total_b = round(total / 1e9, 1)
    usdt = stable.get("USDT", {}).get("market_cap", 0) or 0
    usdc = stable.get("USDC", {}).get("market_cap", 0) or 0
    usdt_dom = round(usdt / total * 100, 1) if total else 0
    usdc_dom = round(usdc / total * 100, 1) if total else 0
    btc_24h = round(float(crypto.get("BTC", {}).get("change_24h") or 0), 2)
    stab_7d = stable.get("USDT", {}).get("price_change_7d") or 0
    flight = stab_7d > 0.5 and btc_24h < -3.0

    # 신호 점수: -1(매우 부정) ~ +1(매우 긍정)
    score = 0.0
    if total_b >= 270:
        score += 0.4
        signal, note = "bullish", f"시총 ${total_b}B — 성장세 지속 (사상 최고권)"
        phase = "growth"
    elif total_b >= 250:
        score += 0.1
        signal, note = "neutral", f"시총 ${total_b}B — 안정권 유지"
        phase = "growth"
    elif total_b <= 200:
        score -= 0.4
        signal, note = "bearish", f"시총 ${total_b}B — 수요 감소"
        phase = "early"
    else:
        signal, note = "neutral", f"시총 ${total_b}B — 안정권"
        phase = "growth"

    if btc_24h >= 5: score += 0.3
    elif btc_24h <= -5: score -= 0.3
    if usdc_dom >= 30: score += 0.1  # USDC 점유율 회복 = GENIUS Act 수혜 신호
    if flight:
        note += " | ⚠️ 안전자산 선호 감지 (BTC↓ + 스테이블코인↑)"

    # 채택 라이프사이클
    if total_b >= 300: phase = "saturation"
    elif total_b >= 200: phase = "growth"
    else: phase = "early"

    return StablecoinResult(
        total_mcap_b=total_b, usdt_dom_pct=usdt_dom, usdc_dom_pct=usdc_dom,
        btc_24h_pct=btc_24h, flight_to_safety=flight,
        signal=signal, signal_score=round(min(1.0, max(-1.0, score)), 2),
        note=note, adoption_phase=phase,
    )


# ── 메인 ──────────────────────────────────────────────────────────────────

def analyze(snapshot: dict = None) -> dict:
    if snapshot is None:
        files = sorted(Path(CONTEXT_DIR).glob("snapshot_*.json"), reverse=True)
        if not files:
            return {"error": "snapshot 없음 — python main.py --brief 먼저 실행"}
        with open(files[0], encoding="utf-8") as f:
            snapshot = json.load(f)

    macro = snapshot.get("macro", {})
    stable = snapshot.get("stablecoins", {})
    crypto = snapshot.get("crypto", {})

    regime = detect_regime(macro, crypto, stable)
    stablecoin = analyze_stablecoins(stable, crypto)

    danal_data = build_implications(regime.regime, macro, stablecoin)
    danal = DanalResult(**danal_data)

    result = {
        "analyzed_at":      datetime.now().isoformat(),
        "source_snapshot":  snapshot.get("collected_at", "unknown"),
        "regime":           asdict(regime),
        "stablecoin_signal": asdict(stablecoin),
        "danal_implications": asdict(danal),
        "signal_count":     len(regime.signals),
        "analysis_version": "2.1.0",  # 동적 함의 + Late-Cycle 업데이트
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/analysis_{datetime.now().strftime('%Y%m%d')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 분석 저장: {path}")
    print(f"  ✓ 신호 수집: {result['signal_count']}개 | 레짐: {regime.regime} ({regime.confidence}, score={regime.confidence_score})")
    return result


if __name__ == "__main__":
    result = analyze()
    r = result.get("regime", {})
    s = result.get("stablecoin_signal", {})
    d = result.get("danal_implications", {})
    print(f"\n=== 레짐 분석 결과 ===")
    print(f"레짐: {r.get('regime')} ({r.get('confidence')}, score={r.get('confidence_score')})")
    print(f"성장: {r.get('growth_dir')} | 인플레이션: {r.get('inflation_dir')}")
    print(f"스테이블코인: {s.get('note')} (score={s.get('signal_score')})")
    print(f"채택 단계: {s.get('adoption_phase')}")
    print(f"\n[다날 우선 행동]")
    print(f"  {d.get('priority_action')}")
    if r.get("alert_flags"):
        print(f"\n[경보 플래그]")
        for flag in r.get("alert_flags", []):
            print(f"  ⚠️ {flag}")
