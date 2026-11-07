import numpy as np
from .config import MIN_EVT_SAMPLES


def invert_rival_distribution(t1_array: np.ndarray, t2_array: np.ndarray, n_array: np.ndarray, grid: np.ndarray) -> tuple:
    """
    L2: 극값이론(EVT) 기반 경쟁자 투찰률 분포 역산
    - 원리 1 (생존함수): F_hat(x) = 1 - S_hat_N(x)^(1 / N_bar)
    - 원리 3 (1-2위 격차 밀도): f_hat(t1) = 1 / (N * d_bar)
    """
    t1 = np.asarray(t1_array, dtype=np.float64)
    t2 = np.asarray(t2_array, dtype=np.float64)
    n_arr = np.maximum(np.asarray(n_array, dtype=np.float64), 1.0)
    grid = np.asarray(grid, dtype=np.float64)

    F_hat = np.zeros(len(grid), dtype=np.float64)
    f_hat = np.full(len(grid), 1e-9, dtype=np.float64)

    if len(t1) == 0:
        return F_hat, f_hat

    for i, x in enumerate(grid):
        mask = t1 > x
        if not np.any(mask):
            F_hat[i] = 1.0
        else:
            S_hat = float(np.mean(mask))
            N_bar = float(np.mean(n_arr[mask])) if np.any(mask) else float(np.mean(n_arr))
            F_hat[i] = 1.0 - (S_hat ** (1.0 / max(N_bar, 1.0)))

        near = np.abs(t1 - x) < 0.12
        if np.sum(near) >= 2:
            diffs = t2[near] - t1[near]
            pos_diffs = diffs[diffs > 1e-9]
            if len(pos_diffs) > 0:
                d_bar = float(np.mean(pos_diffs))
                N_loc = float(np.mean(n_arr[near]))
                f_hat[i] = max(1.0 / (N_loc * d_bar), 1e-9)

    F_hat = np.maximum.accumulate(np.clip(F_hat, 0.0, 1.0))
    f_hat = np.maximum(f_hat, 1e-9)
    return F_hat, f_hat


def estimate_n_bidders(org: str, base_amt: int, hist_n_bidders: list = None) -> float:
    if hist_n_bidders and len(hist_n_bidders) > 0:
        return float(max(np.mean(hist_n_bidders), 2.0))
    if base_amt >= 3000000000:
        return 48.0
    return 65.0
