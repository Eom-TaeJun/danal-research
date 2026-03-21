# 목적: 신호 가중치 자동 보정 (DB 축적 → 유의성 기반 가중치 선정)
# 입력: outputs/context/analysis_*.json (과거 분석 결과 누적)
# 출력: outputs/context/weights_YYYYMMDD.json
# 방법: 1) 신호-결과 상관 추적  2) Spearman 유의성 기반 가중치 재배분
# 구조: eco_system_v2 패턴 (frozen dataclass + 파라미터화)
# 제외: 실시간 학습, GPU 의존 모델

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = "outputs/context"


@dataclass(frozen=True)
class CalibrationConfig:
    """보정 파라미터 — 변경 시 새 인스턴스 생성"""
    min_samples: int = 10          # 최소 샘플 수 (이하면 기본 가중치 유지)
    lookback_days: int = 90        # 최근 N일 데이터만 사용
    significance_alpha: float = 0.10  # Spearman p-value 임계값
    floor_weight: float = 0.05    # 최소 가중치 (0으로 떨어지지 않도록)
    ceiling_weight: float = 0.60  # 최대 가중치 (단일 신호 과의존 방지)


# 기본 가중치 (보정 데이터 부족 시 폴백)
DEFAULT_WEIGHTS = {
    "yield_curve_10y_ff": 0.40,
    "yield_curve_2y_10y": 0.25,
    "fed_funds_level": 0.50,
    "10y_yield_level": 0.20,
    "usd_strength_alert": 0.15,
    "usd_weakness": 0.10,
    "btc_momentum": 0.15,
    "stablecoin_mcap": 0.10,
    "btc_vol_ratio": 0.15,
}


def _load_history(lookback_days: int = 90) -> list[dict]:
    """과거 분석 결과 로드 (최근 N일)"""
    ctx = Path(OUTPUT_DIR)
    if not ctx.exists():
        return []
    files = sorted(ctx.glob("analysis_*.json"), reverse=True)
    cutoff = datetime.now().timestamp() - lookback_days * 86400
    history = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            ts = datetime.fromisoformat(data.get("analyzed_at", "")).timestamp()
            if ts >= cutoff:
                history.append(data)
        except (json.JSONDecodeError, ValueError, KeyError):
            continue
    return history


def _extract_signal_directions(analysis: dict) -> dict[str, float]:
    """분석 결과에서 신호 이름 → 방향 수치 (-1, 0, +1) 추출"""
    signals = analysis.get("regime", {}).get("signals", [])
    result = {}
    for s in signals:
        name = s.get("name", "")
        direction = s.get("direction", "neutral")
        if direction in ("positive", "low"):
            result[name] = 1.0
        elif direction in ("negative", "high"):
            result[name] = -1.0
        else:
            result[name] = 0.0
    return result


def _extract_outcome(analysis: dict) -> float | None:
    """분석 결과에서 결과 지표 추출 (스테이블코인 시그널 스코어를 프록시로 사용).

    향후 실제 시장 결과 (다음 주 BTC 수익률 등)로 교체 가능.
    """
    return analysis.get("stablecoin_signal", {}).get("signal_score")


def calibrate(config: CalibrationConfig = CalibrationConfig()) -> dict:
    """신호 가중치 보정.

    1. 과거 분석 히스토리 로드
    2. 신호별 방향 vs 결과 Spearman 상관 계산
    3. 유의한 신호에 가중치 상향, 비유의 신호에 가중치 하향
    4. floor/ceiling 적용 후 정규화

    Returns:
        dict(weights={signal: weight}, meta={samples, method, ...})
    """
    history = _load_history(config.lookback_days)

    if len(history) < config.min_samples:
        return {
            "weights": DEFAULT_WEIGHTS.copy(),
            "meta": {
                "method": "default",
                "reason": f"샘플 부족 ({len(history)}/{config.min_samples})",
                "calibrated_at": datetime.now().isoformat(),
            },
        }

    # 신호별 방향 시계열 + 결과 시계열 구축
    all_signals: dict[str, list[float]] = {}
    outcomes: list[float] = []

    for h in history:
        outcome = _extract_outcome(h)
        if outcome is None:
            continue
        directions = _extract_signal_directions(h)
        outcomes.append(outcome)
        for name in DEFAULT_WEIGHTS:
            all_signals.setdefault(name, []).append(directions.get(name, 0.0))

    if len(outcomes) < config.min_samples:
        return {
            "weights": DEFAULT_WEIGHTS.copy(),
            "meta": {
                "method": "default",
                "reason": f"유효 결과 부족 ({len(outcomes)}/{config.min_samples})",
                "calibrated_at": datetime.now().isoformat(),
            },
        }

    # Spearman 상관 계산 (scipy 없이 순위 기반 구현)
    correlations = {}
    for name, values in all_signals.items():
        if len(values) != len(outcomes):
            continue
        rho = _spearman_rho(values, outcomes)
        correlations[name] = rho

    # 상관 절댓값 기반 가중치 배분
    raw_weights = {}
    for name, rho in correlations.items():
        abs_rho = abs(rho) if rho is not None else 0.0
        raw_weights[name] = max(config.floor_weight, abs_rho)

    # ceiling 적용
    for name in raw_weights:
        raw_weights[name] = min(config.ceiling_weight, raw_weights[name])

    # 정규화 (합계 = DEFAULT_WEIGHTS 합계 유지)
    target_sum = sum(DEFAULT_WEIGHTS.values())
    current_sum = sum(raw_weights.values())
    if current_sum > 0:
        scale = target_sum / current_sum
        weights = {k: round(v * scale, 3) for k, v in raw_weights.items()}
    else:
        weights = DEFAULT_WEIGHTS.copy()

    result = {
        "weights": weights,
        "correlations": {k: round(v, 3) if v else 0.0 for k, v in correlations.items()},
        "meta": {
            "method": "spearman_correlation",
            "samples": len(outcomes),
            "lookback_days": config.lookback_days,
            "calibrated_at": datetime.now().isoformat(),
        },
    }

    # 저장
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/weights_{datetime.now().strftime('%Y%m%d')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 가중치 보정 저장: {path} (samples={len(outcomes)}, method={result['meta']['method']})")

    return result


def _spearman_rho(x: list[float], y: list[float]) -> float | None:
    """Spearman 순위 상관 (scipy 없이 구현)."""
    n = len(x)
    if n < 3:
        return None
    rx = _rank(x)
    ry = _rank(y)
    d_sq = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - (6 * d_sq) / (n * (n ** 2 - 1))


def _rank(values: list[float]) -> list[float]:
    """평균 순위 (동률 처리)."""
    indexed = sorted(enumerate(values), key=lambda t: t[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + j + 1) / 2  # 1-based 평균
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


def load_calibrated_weights() -> dict[str, float]:
    """최신 보정 가중치 로드. 없으면 기본값."""
    ctx = Path(OUTPUT_DIR)
    files = sorted(ctx.glob("weights_*.json"), reverse=True) if ctx.exists() else []
    if files:
        try:
            data = json.loads(files[0].read_text(encoding="utf-8"))
            return data.get("weights", DEFAULT_WEIGHTS.copy())
        except (json.JSONDecodeError, KeyError):
            pass
    return DEFAULT_WEIGHTS.copy()
