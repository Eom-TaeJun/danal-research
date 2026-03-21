# 목적: 스테이블코인 개별 리스크 평가 (4축 스코어링 + 스트레스 테스트)
# 입력: collect.py가 수집한 snapshot (stablecoins, crypto, macro)
# 출력: 코인별 리스크 등급 (A~F) + 4축 점수 + 스트레스 결과
# 구조: eco_system_v2 패턴 (frozen dataclass + linear_scale + 파라미터화)
# 도메인: eimas genius_act 리스크 프레임워크 (구조화 + 탈하드코딩)

from dataclasses import dataclass, field
from enum import Enum


# ── 설정 (eco_system_v2 패턴: frozen dataclass로 파라미터화) ──────────────

class CollateralType(Enum):
    TREASURY_CASH = "treasury_cash"      # USDC, PYUSD
    MIXED_RESERVE = "mixed_reserve"      # USDT
    CRYPTO_BACKED = "crypto_backed"      # DAI
    ODL_HYBRID = "odl_hybrid"            # RLUSD


@dataclass(frozen=True)
class RiskWeights:
    """4축 가중치 — 합계 1.0"""
    credit: float = 0.30
    liquidity: float = 0.25
    regulatory: float = 0.25
    technical: float = 0.20


@dataclass(frozen=True)
class StressScenario:
    """스트레스 테스트 시나리오 파라미터"""
    name: str
    depeg_base_prob: float
    loss_multiplier: float
    crypto_vol_shock: float


# 시나리오 정의 (eimas 도메인 + 파라미터화)
STRESS_SCENARIOS = {
    "mild":     StressScenario("금리 50bp 상승", 0.01, 0.02, 0.20),
    "moderate": StressScenario("유동성 위기", 0.05, 0.10, 0.40),
    "severe":   StressScenario("은행 위기 (SVB급)", 0.15, 0.30, 0.60),
    "extreme":  StressScenario("UST 디페그급", 0.30, 0.80, 0.80),
}

# 담보유형별 기본 리스크 계수 (0=안전, 1=위험)
COLLATERAL_RISK = {
    CollateralType.TREASURY_CASH: 0.10,
    CollateralType.MIXED_RESERVE: 0.40,
    CollateralType.CRYPTO_BACKED: 0.65,
    CollateralType.ODL_HYBRID: 0.35,
}


# ── 스코어링 유틸 (eco_system_v2 패턴: linear_scale) ─────────────────────

def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def _linear_scale(value: float, low: float, high: float, invert: bool = False) -> float:
    """[low, high] → [0, 100]. invert=True면 높을수록 낮은 점수."""
    if high == low:
        return 50.0
    score = (value - low) / (high - low) * 100
    if invert:
        score = 100.0 - score
    return _clamp(score)


# ── 코인 프로필 (수집 데이터 + 정적 속성) ────────────────────────────────

@dataclass
class CoinProfile:
    """코인별 리스크 평가 입력"""
    ticker: str
    collateral_type: CollateralType
    market_cap_b: float           # CoinGecko 수집
    genius_act_compliant: bool    # GENIUS Act 준수 여부
    pays_interest: bool           # 이자 지급 여부 (SEC 증권 리스크)
    transparency: float           # 0~1 (준비금 공개 수준)
    audits: int                   # 스마트 컨트랙트 감사 횟수
    peg_stability: float          # 0~100 (7일 페그 안정성)


# 정적 속성 (API로 못 가져오는 것만 — 시총은 수집 데이터로 덮어씀)
COIN_ATTRS = {
    "USDT": dict(collateral_type=CollateralType.MIXED_RESERVE,
                 genius_act_compliant=False, pays_interest=False,
                 transparency=0.60, audits=2),
    "USDC": dict(collateral_type=CollateralType.TREASURY_CASH,
                 genius_act_compliant=True, pays_interest=False,
                 transparency=0.95, audits=5),
    "DAI":  dict(collateral_type=CollateralType.CRYPTO_BACKED,
                 genius_act_compliant=False, pays_interest=True,
                 transparency=0.90, audits=4),
    "RLUSD": dict(collateral_type=CollateralType.ODL_HYBRID,
                  genius_act_compliant=True, pays_interest=False,
                  transparency=0.70, audits=1),
}


# ── 4축 리스크 평가 ──────────────────────────────────────────────────────

def _score_credit(profile: CoinProfile) -> float:
    """신용 리스크: 담보유형 + 투명성 → 0(안전)~100(위험)"""
    base = COLLATERAL_RISK.get(profile.collateral_type, 0.5) * 100
    transparency_bonus = profile.transparency * 20  # 투명할수록 리스크 감소
    return _clamp(base - transparency_bonus)


def _score_liquidity(profile: CoinProfile) -> float:
    """유동성 리스크: 시총 규모 → 0(안전)~100(위험)"""
    # 시총 클수록 유동성 위험 낮음
    return _linear_scale(profile.market_cap_b, 0, 100, invert=True)


def _score_regulatory(profile: CoinProfile) -> float:
    """규제 리스크: GENIUS Act 준수 + 이자 지급(증권성) → 0(안전)~100(위험)"""
    score = 40.0
    if profile.genius_act_compliant:
        score -= 20.0
    elif profile.collateral_type == CollateralType.CRYPTO_BACKED:
        score += 5.0   # DeFi — 규제 대상 자체가 다름 (직접 비교 부적절)
    else:
        score += 15.0
    if profile.pays_interest:
        score += 15.0  # SEC 증권 분류 리스크
    return _clamp(score)


def _score_technical(profile: CoinProfile) -> float:
    """기술 리스크: 감사 횟수 + 페그 안정성 → 0(안전)~100(위험)"""
    audit_risk = _linear_scale(profile.audits, 0, 5, invert=True)
    peg_risk = 100.0 - profile.peg_stability
    return _clamp(audit_risk * 0.4 + peg_risk * 0.6)


def assess_risk(
    profile: CoinProfile,
    weights: RiskWeights = RiskWeights(),
) -> dict:
    """코인별 4축 리스크 종합 평가.

    Returns:
        dict(ticker, credit, liquidity, regulatory, technical,
             total, grade, weights_used)
    """
    scores = {
        "credit": round(_score_credit(profile), 1),
        "liquidity": round(_score_liquidity(profile), 1),
        "regulatory": round(_score_regulatory(profile), 1),
        "technical": round(_score_technical(profile), 1),
    }

    total = (
        scores["credit"] * weights.credit
        + scores["liquidity"] * weights.liquidity
        + scores["regulatory"] * weights.regulatory
        + scores["technical"] * weights.technical
    )
    total = round(total, 1)

    if total < 20:
        grade = "A"
    elif total < 35:
        grade = "B"
    elif total < 50:
        grade = "C"
    elif total < 70:
        grade = "D"
    else:
        grade = "F"

    return {
        "ticker": profile.ticker,
        **scores,
        "total": total,
        "grade": grade,
    }


# ── 스트레스 테스트 ──────────────────────────────────────────────────────

def stress_test(
    profile: CoinProfile,
    scenario: StressScenario,
) -> dict:
    """디페그 확률 + 예상 손실 계산.

    Returns:
        dict(scenario, depeg_prob, expected_loss_pct, rating)
    """
    base_risk = COLLATERAL_RISK.get(profile.collateral_type, 0.5)

    # 디페그 확률: 기본 확률 × 담보 위험 계수
    depeg_prob = min(1.0, scenario.depeg_base_prob * (1 + base_risk * 3))
    if profile.pays_interest:
        depeg_prob *= 1.3  # 이자 지급 → 추가 복잡성

    # 예상 손실: 시나리오 손실 × 담보 계수
    loss_pct = min(1.0, scenario.loss_multiplier * (1 + base_risk * 2))

    # 등급
    combined = depeg_prob * 0.5 + loss_pct * 0.5
    if combined < 0.02:
        rating = "LOW"
    elif combined < 0.05:
        rating = "MODERATE"
    elif combined < 0.15:
        rating = "ELEVATED"
    elif combined < 0.30:
        rating = "HIGH"
    else:
        rating = "CRITICAL"

    return {
        "scenario": scenario.name,
        "depeg_prob": round(depeg_prob * 100, 1),
        "expected_loss_pct": round(loss_pct * 100, 1),
        "rating": rating,
    }


# ── 메인: snapshot 데이터 → 전체 평가 ────────────────────────────────────

def evaluate_stablecoins(snapshot: dict) -> dict:
    """수집 데이터로 전체 스테이블코인 리스크 평가.

    Returns:
        dict(assessments=[...], stress_tests={ticker: [...]})
    """
    stable_data = snapshot.get("stablecoins", {})
    assessments = []
    stress_results = {}

    for ticker, attrs in COIN_ATTRS.items():
        mcap = stable_data.get(ticker, {}).get("market_cap", 0) or 0
        mcap_b = mcap / 1e9 if mcap > 1000 else mcap  # 이미 B 단위면 그대로

        peg_7d = stable_data.get(ticker, {}).get("price_change_7d") or 0
        peg_stability = _clamp(100 - abs(float(peg_7d)) * 20)

        profile = CoinProfile(
            ticker=ticker,
            market_cap_b=mcap_b,
            peg_stability=peg_stability,
            **attrs,
        )

        assessments.append(assess_risk(profile))

        stress_results[ticker] = [
            stress_test(profile, scenario)
            for scenario in STRESS_SCENARIOS.values()
        ]

    return {
        "assessments": assessments,
        "stress_tests": stress_results,
    }
