import numpy as np
from decimal import Decimal
from .config import ceil_won


def cost_estimate(base_amt: int, econ: dict) -> tuple:
    """
    c = c_직접 + c_간접 + c_금융 + c_리스크
    """
    warnings = []
    if not econ or "direct_cost_ratio" not in econ or econ.get("direct_cost_ratio") is None:
        warnings.append("F-4: 기업 원가 정보 미입력으로 보수적 기준 원가율(85.5%) 폴백 적용")
        direct_r = Decimal("0.815")
        indirect_r = Decimal("0.030")
        finance_r = Decimal("0.010")
    else:
        direct_r = Decimal(str(econ.get("direct_cost_ratio", 0.815)))
        indirect_r = Decimal(str(econ.get("indirect_ratio", 0.030)))
        finance_r = Decimal(str(econ.get("finance_ratio", 0.010)))

    total_ratio = direct_r + indirect_r + finance_r
    c_won = ceil_won(Decimal(base_amt) * total_ratio)
    return c_won, warnings


def win_probability(price_rate_pct: float, F_hat: np.ndarray, grid: np.ndarray, n_bidders: float) -> float:
    """
    W(p) = [1 - F(p)]^N
    """
    f_val = float(np.interp(price_rate_pct, grid, F_hat))
    f_val = float(np.clip(f_val, 1e-6, 0.999999))
    w_prob = (1.0 - f_val) ** max(float(n_bidders), 1.0)
    return float(np.clip(w_prob, 1e-6, 0.9999))


def profit_field(
    step_bid_prices: np.ndarray,
    base_amt: int,
    step_pmf: np.ndarray,
    cost_won: int,
    F_hat: np.ndarray,
    grid: np.ndarray,
    n_bidders: float,
    lam: float = 0.0,
) -> tuple:
    """
    각 계단 j (1..1365)에 대한 승률 W_j 및 기대이익 E_j = W_j * (P_j - c) 계산
    """
    rates_pct = (step_bid_prices.astype(np.float64) / float(base_amt)) * 100.0
    f_vals = np.clip(np.interp(rates_pct, grid, F_hat), 1e-6, 0.999999)
    win_probs = np.power(1.0 - f_vals, max(float(n_bidders), 1.0))

    margins = step_bid_prices.astype(np.float64) - float(cost_won)
    # 하한선 통과 확률(계단 누적 타격 성공률)과 경쟁자 돌파 확률 결합
    cum_valid_prob = np.cumsum(step_pmf)
    effective_win_probs = np.clip(win_probs * (0.35 + 0.65 * cum_valid_prob), 1e-6, 0.999)

    risk_penalty = float(lam) * np.maximum(0.0, -margins)
    expected_profits = effective_win_probs * margins - risk_penalty
    return expected_profits, effective_win_probs
