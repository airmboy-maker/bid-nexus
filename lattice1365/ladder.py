import hashlib
import numpy as np
from decimal import Decimal
from .config import COMBS_ARRAY, floor_won, ceil_won
from .slots import simulate_slots


def canonical_1365_ladder(base_amt: int, notice_no: str, mu: float, delta: float, rho: float) -> dict:
    """
    결정론적 공고 시드 기반으로 기준 15개 예비가격 슬롯과 정확히 1,365개의 계단(예정가격 후보) 격자를 생성하고,
    몬테카를로 확률장(L1)을 이 1,365개 계단 격자 위로 투영하여 계단별 착지확률 p[1365]를 산출한다.
    """
    seed_int = int(hashlib.sha256(f"{notice_no}_{base_amt}".encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed_int)

    # 기준 15개 슬롯 사정률 구성 (공통충격 반영 정렬 격자)
    base_grid = np.linspace(mu - 1.65 * delta, mu + 1.65 * delta, 15)
    jitter = rng.normal(0.0, delta * 0.08, 15)
    slot_rates = np.sort(base_grid + jitter)

    slot_won = np.array([floor_won(Decimal(base_amt) * Decimal(str(round(r, 6))) / Decimal("100")) for r in slot_rates], dtype=np.int64)
    comb_sums = slot_won[COMBS_ARRAY].sum(axis=1)
    step_est_prices = (comb_sums // 4).astype(np.int64)  # (1365,) 원단위 절사 예정가격

    return {
        "slot_rates": slot_rates,
        "slot_won": slot_won,
        "step_est_prices": step_est_prices,
        "seed_int": seed_int,
    }


def ladder_field(base_amt: int, mu: float, delta: float, rho: float, n_sims: int = 15000, chunk: int = 3000, seed: int = 42) -> np.ndarray:
    """
    청크 단위 벡터화로 M회 시뮬레이션된 추첨 예정가격 배열 반환 (4GB RAM 안전 동작)
    """
    rng = np.random.default_rng(seed)
    all_p = []
    remaining = int(n_sims)
    while remaining > 0:
        cur = min(chunk, remaining)
        r = simulate_slots(mu, delta, rho, cur, rng)
        s_won = np.floor(float(base_amt) * r / 100.0)
        idx = rng.integers(0, 1365, size=cur)
        picked_combs = COMBS_ARRAY[idx]  # (cur, 4)
        row_idx = np.arange(cur)[:, None]
        chosen_slots = s_won[row_idx, picked_combs]  # (cur, 4)
        p_actual = np.floor(chosen_slots.sum(axis=1) / 4.0).astype(np.int64)
        all_p.append(p_actual)
        remaining -= cur
    return np.concatenate(all_p)


def ladder_pmf(prices: np.ndarray) -> tuple:
    """(계단가격 배열, 확률질량 배열) — 확률 내림차순"""
    uniq, counts = np.unique(prices, return_counts=True)
    pmf = counts.astype(np.float64) / float(len(prices))
    order = np.argsort(-pmf)
    return uniq[order], pmf[order]
