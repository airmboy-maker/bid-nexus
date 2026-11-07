import numpy as np


def crps(samples: np.ndarray, observed: float) -> float:
    """
    CRPS(F, y) 표본 근사
    """
    x = np.asarray(samples, dtype=np.float64)
    if len(x) > 2000:
        x = np.random.default_rng(42).choice(x, size=2000, replace=False)
    term1 = float(np.mean(np.abs(x - float(observed))))
    diffs = np.abs(x[:, None] - x[None, :])
    term2 = float(np.mean(diffs)) / 2.0
    return max(0.0, term1 - term2)


def pit_histogram(samples_list: list, observed_list: list, bins: int = 10) -> np.ndarray:
    u_vals = []
    for samp, obs in zip(samples_list, observed_list):
        s_arr = np.asarray(samp, dtype=np.float64)
        u_vals.append(float(np.mean(s_arr <= float(obs))))
    hist, _ = np.histogram(u_vals, bins=bins, range=(0.0, 1.0), density=True)
    return hist


def conformal_interval(scores: list, alpha: float = 0.05) -> float:
    arr = np.abs(np.asarray(scores, dtype=np.float64))
    if len(arr) == 0:
        return 0.25
    q_level = min(1.0, max(0.0, (1.0 - alpha) * (1.0 + 1.0 / len(arr))))
    return float(np.quantile(arr, q_level))


def thompson_weights(arm_rewards: dict, seed: int = 42) -> dict:
    """
    M1~M6 각 모델의 누적 보상(성공/실패 또는 정규 점수)으로부터 Thompson 사후 가중치 산출
    """
    rng = np.random.default_rng(seed)
    samples = {}
    for arm, stats in arm_rewards.items():
        alpha = max(float(stats.get("alpha", 2.0)), 0.5)
        beta = max(float(stats.get("beta", 2.0)), 0.5)
        samples[arm] = float(rng.beta(alpha, beta))
    total = sum(samples.values()) or 1.0
    return {k: round(v / total, 4) for k, v in samples.items()}
