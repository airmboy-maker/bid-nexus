import numpy as np
from decimal import Decimal
from .config import ceil_won


def price_score(rate_ratio: np.ndarray, smax: float, r_star: float, k_coef: float) -> np.ndarray:
    """
    S_price(r) = S_max - k * |r* - r| * 100
    """
    r_arr = np.asarray(rate_ratio, dtype=np.float64)
    scores = float(smax) - float(k_coef) * np.abs(float(r_star) - r_arr) * 100.0
    return np.maximum(0.0, scores)


def effective_floor(
    P_grid: np.ndarray,
    B: int,
    S_pq: float,
    S_cut: float,
    smax: float,
    r_star: float,
    k: float,
    r_announced: float,
) -> tuple:
    """
    L4 핵심 함수: 수행능력점수(S_pq)에 따른 내생적 실효 하한선(r_eff) 및 적격 가능 계단(feasible) 마스크 반환.
    r_eff = max(r_announced, min_{P_j in F} P_j / B)
    (단, S_pq가 높을수록 더 낮은 입찰률에서도 S_pq + S_price >= S_cut를 통과하므로 실효 하한은 단조 감소/비증가함)
    """
    if B <= 0 or len(P_grid) == 0:
        return None, np.zeros(len(P_grid), dtype=bool)

    r = P_grid.astype(np.float64) / float(B)
    s_price = price_score(r, smax=smax, r_star=r_star, k_coef=k)
    feasible = ((float(S_pq) + s_price) >= float(S_cut)) & (r >= float(r_announced))

    if not np.any(feasible):
        return None, np.zeros_like(feasible, dtype=bool)

    r_eff = max(float(r_announced), float(r[feasible].min()))
    return r_eff, feasible


def step_bid_from_est_price(est_price: int, a_val: int, eff_limit_rate_pct: float, wedge_won: int = 19) -> int:
    """
    원단위 절상(ROUND_CEILING) 기반 계단별 하한선 + 웨지 산출
    """
    ep_d = Decimal(int(est_price))
    a_d = Decimal(int(a_val))
    r_d = Decimal(str(round(eff_limit_rate_pct, 6))) / Decimal("100")
    pure_cut = ceil_won((ep_d - a_d) * r_d + a_d)
    return int(pure_cut + int(wedge_won))
