"""Smoke tests — 핵심 모듈 import + 기본 동작 검증."""

import pytest


# ── risk.py ───────────────────────────────────────────────────────────────

def test_risk_assess_usdc():
    from src.risk import assess_risk, CoinProfile, CollateralType
    profile = CoinProfile(
        ticker="USDC", collateral_type=CollateralType.TREASURY_CASH,
        market_cap_b=45.0, genius_act_compliant=True, pays_interest=False,
        transparency=0.95, audits=5, peg_stability=99.5,
    )
    result = assess_risk(profile)
    assert result["grade"] in ("A", "B")
    assert 0 <= result["total"] <= 100


def test_risk_assess_dai():
    from src.risk import assess_risk, CoinProfile, CollateralType
    profile = CoinProfile(
        ticker="DAI", collateral_type=CollateralType.CRYPTO_BACKED,
        market_cap_b=4.2, genius_act_compliant=False, pays_interest=True,
        transparency=0.90, audits=4, peg_stability=98.0,
    )
    result = assess_risk(profile)
    assert result["grade"] in ("C", "D", "F")
    assert result["credit"] > result["total"] * 0  # credit exists


def test_stress_test_severe():
    from src.risk import stress_test, CoinProfile, CollateralType, STRESS_SCENARIOS
    profile = CoinProfile(
        ticker="USDT", collateral_type=CollateralType.MIXED_RESERVE,
        market_cap_b=130.0, genius_act_compliant=False, pays_interest=False,
        transparency=0.60, audits=2, peg_stability=99.0,
    )
    result = stress_test(profile, STRESS_SCENARIOS["severe"])
    assert 0 <= result["depeg_prob"] <= 100
    assert result["rating"] in ("LOW", "MODERATE", "ELEVATED", "HIGH", "CRITICAL")


def test_evaluate_stablecoins_with_snapshot():
    from src.risk import evaluate_stablecoins
    snapshot = {
        "stablecoins": {
            "USDT": {"market_cap": 130e9, "price_change_7d": -0.1},
            "USDC": {"market_cap": 45e9, "price_change_7d": 0.05},
            "DAI": {"market_cap": 4.2e9, "price_change_7d": -0.3},
        }
    }
    result = evaluate_stablecoins(snapshot)
    assert len(result["assessments"]) >= 3
    assert "USDT" in result["stress_tests"]


# ── calibrate.py ──────────────────────────────────────────────────────────

def test_calibrate_default_weights():
    from src.calibrate import calibrate, CalibrationConfig, DEFAULT_WEIGHTS
    config = CalibrationConfig(min_samples=999)  # 항상 기본값 폴백
    result = calibrate(config)
    assert result["meta"]["method"] == "default"
    assert set(result["weights"].keys()) == set(DEFAULT_WEIGHTS.keys())


def test_spearman_rho():
    from src.calibrate import _spearman_rho
    # 완전 양의 상관
    assert abs(_spearman_rho([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]) - 1.0) < 0.01
    # 완전 음의 상관
    assert abs(_spearman_rho([1, 2, 3, 4, 5], [10, 8, 6, 4, 2]) + 1.0) < 0.01


def test_load_calibrated_weights_fallback():
    from src.calibrate import load_calibrated_weights, DEFAULT_WEIGHTS
    weights = load_calibrated_weights()
    assert isinstance(weights, dict)
    assert len(weights) > 0


# ── analyze.py (레짐 판단) ────────────────────────────────────────────────

def test_detect_regime_goldilocks():
    from src.analyze import detect_regime
    macro = {
        "FEDFUNDS": {"value": "3.5"},
        "DGS10": {"value": "4.0"},
        "DGS2": {"value": "3.6"},
        "DEXKOUS": {"value": "1380"},
    }
    result = detect_regime(macro)
    assert result.regime in ("Goldilocks", "Overheating", "Late-Cycle",
                              "Stagflation", "Recession")
    assert 0 <= result.confidence_score <= 1.0
    assert len(result.signals) > 0


def test_detect_regime_no_data():
    from src.analyze import detect_regime
    result = detect_regime({})
    assert result.regime  # 빈 데이터도 폴백 레짐 반환
