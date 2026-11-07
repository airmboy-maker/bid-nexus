import numpy as np
from .config import DEFAULT_RHO_FALLBACK


def estimate_org_params(
    slots_history: list = None,
    est_rates_history: list = None,
    ewma_alpha: float = 0.65,
) -> dict:
    """
    L0: 발주처 사정률 평균(mu), 변동성(delta), 공통충격 상관계수(rho) 추정.
    Var(R) = delta^2 * [rho + (1 - rho) / 4]
    """
    warnings = []
    n_obs = 0
    rho_hat = DEFAULT_RHO_FALLBACK

    if slots_history and len(slots_history) >= 5:
        arr = np.asarray(slots_history, dtype=np.float64)
        if arr.ndim == 2 and arr.shape[1] == 15:
            n_obs = arr.shape[0]
            corr_mat = np.corrcoef(arr, rowvar=False)
            iu = np.triu_indices(15, k=1)
            valid_corrs = corr_mat[iu]
            valid_corrs = valid_corrs[~np.isnan(valid_corrs)]
            if len(valid_corrs) > 0:
                rho_hat = float(np.mean(valid_corrs))
            row_means = arr.mean(axis=1)
            mu = float(row_means[0])
            for r_val in row_means[1:]:
                mu = ewma_alpha * float(r_val) + (1.0 - ewma_alpha) * mu
            delta = float(np.std(arr, ddof=1))
        else:
            mu, delta = 100.085, 0.35
            warnings.append("F-1: 슬롯 이력 형식이 15열이 아니므로 기본 파라미터 적용")
    elif est_rates_history and len(est_rates_history) >= 2:
        n_obs = len(est_rates_history)
        mu = float(est_rates_history[0])
        for r_val in est_rates_history[1:]:
            mu = ewma_alpha * float(r_val) + (1.0 - ewma_alpha) * mu
        var_r = float(np.var(est_rates_history, ddof=1)) if n_obs > 1 else 0.04
        if n_obs < 5:
            rho_hat = DEFAULT_RHO_FALLBACK
            warnings.append(f"F-1: 관측 표본 부족(n={n_obs}<5)으로 보수적 기본값 rho={DEFAULT_RHO_FALLBACK} 적용")
        factor = rho_hat + (1.0 - rho_hat) / 4.0
        delta = float(np.sqrt(max(var_r, 1e-6) / max(factor, 0.25)))
    else:
        mu = 100.085
        delta = 0.35
        rho_hat = DEFAULT_RHO_FALLBACK
        warnings.append("F-1: 15개 슬롯 비공개 또는 이력 부재로 보수적 기본값(rho=0.30) 적용")

    # 방어 규칙
    if rho_hat < 0.0:
        rho_hat = 0.0
    if rho_hat > 0.95:
        rho_hat = 0.95
    if n_obs > 0 and n_obs < 5:
        rho_hat = DEFAULT_RHO_FALLBACK

    return {
        "mu": round(mu, 6),
        "delta": round(max(delta, 0.05), 6),
        "rho": round(rho_hat, 4),
        "n_obs": int(n_obs),
        "warnings": warnings,
    }


def simulate_slots(mu: float, delta: float, rho: float, n_sims: int, rng: np.random.Generator) -> np.ndarray:
    """
    r_i = mu + delta * (sqrt(rho)*u + sqrt(1-rho)*eps_i)
    반환 shape: (n_sims, 15)
    """
    rho_c = float(np.clip(rho, 0.0, 0.95))
    u = rng.normal(0.0, 1.0, (n_sims, 1))
    eps = rng.normal(0.0, 1.0, (n_sims, 15))
    return mu + delta * (np.sqrt(rho_c) * u + np.sqrt(1.0 - rho_c) * eps)
