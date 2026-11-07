from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np
from .config import (
    ALL_COMBOS, F8_HONEST_WARNING, MIN_EVT_SAMPLES, ceil_won, floor_won
)
from .slots import estimate_org_params
from .ladder import canonical_1365_ladder, ladder_field, ladder_pmf
from .inversion import invert_rival_distribution, estimate_n_bidders
from .profit import cost_estimate, profit_field
from .qualify import effective_floor, step_bid_from_est_price
from .calibrate import crps, conformal_interval, thompson_weights


@dataclass
class BidContext:
    notice_no: str
    org: str
    base_amt: int
    a_val: int
    s_pq: float
    notice_params: dict  # s_max, r_star, k_coef, s_cut, r_announced
    company_econ: dict = field(default_factory=dict)


@dataclass
class BidResult:
    optimal_step: int
    optimal_price: int
    optimal_rate: float
    win_prob: float
    expected_profit: int
    effective_floor_rate: float
    effective_floor_price: int
    p_miss: float
    ladder: dict
    feasible: bool
    warnings: List[str] = field(default_factory=list)


def compute_optimal_bid(ctx: BidContext, opening_hist: list = None, org_profile: dict = None) -> BidResult:
    """
    LATTICE-1365 단일 진입점: L0 -> L1 -> L2 -> L3 -> L4 -> L5 순차 실행
    """
    warnings: List[str] = [F8_HONEST_WARNING]

    if ctx.base_amt <= 0 or ctx.a_val < 0 or ctx.a_val >= ctx.base_amt:
        return BidResult(
            optimal_step=-1, optimal_price=0, optimal_rate=0.0, win_prob=0.0,
            expected_profit=0, effective_floor_rate=0.0, effective_floor_price=0,
            p_miss=1.0, ladder={"prices": []}, feasible=False,
            warnings=["기초금액 또는 A값 입력 범위 오류"] + warnings,
        )

    s_max = float(ctx.notice_params.get("s_max", 70.0))
    r_star = float(ctx.notice_params.get("r_star", 0.88745))
    k_coef = float(ctx.notice_params.get("k_coef", 4.0))
    s_cut = float(ctx.notice_params.get("s_cut", 95.0))
    r_ann = float(ctx.notice_params.get("r_announced", 0.88745))

    # L0: 슬롯 파라미터 추정
    if org_profile and "mu" in org_profile and "delta" in org_profile and "rho" in org_profile:
        mu = float(org_profile["mu"])
        delta = float(org_profile["delta"])
        rho = float(org_profile["rho"])
    else:
        rates_hist = []
        if opening_hist:
            for row in opening_hist:
                if isinstance(row, dict) and row.get("base_amt") and row.get("est_price"):
                    rates_hist.append((float(row["est_price"]) / float(row["base_amt"])) * 100.0)
                elif isinstance(row, dict) and row.get("sajeong_rate"):
                    rates_hist.append(float(row["sajeong_rate"]))
        l0_info = estimate_org_params(est_rates_history=rates_hist)
        mu, delta, rho = l0_info["mu"], l0_info["delta"], l0_info["rho"]
        warnings.extend(l0_info["warnings"])

    # L1: 1,365 계단 격자 및 몬테카를로 확률장 생성
    can_lad = canonical_1365_ladder(ctx.base_amt, ctx.notice_no, mu, delta, rho)
    step_est_prices = can_lad["step_est_prices"]  # (1365,)

    mc_prices = ladder_field(ctx.base_amt, mu, delta, rho, n_sims=12000, chunk=4000, seed=can_lad["seed_int"])
    uniq_p, pmf_p = ladder_pmf(mc_prices)

    # 각 1,365 계단에 확률질량 매핑 (최근접 커널 할당)
    idx_closest = np.searchsorted(step_est_prices, mc_prices)
    idx_closest = np.clip(idx_closest, 0, 1364)
    step_counts = np.bincount(idx_closest, minlength=1365).astype(np.float64)
    step_pmf = (step_counts + 0.1) / float(step_counts.sum() + 136.5)

    # L4: 수행능력점수(S_pq) 기반 실효 하한선(effective_floor) 및 feasible 계단 투영
    # 각 계단의 공고 하한선 기준 투찰가격 산출
    base_step_bids = np.array([
        step_bid_from_est_price(int(ep), ctx.a_val, r_ann * 100.0, wedge_won=19)
        for ep in step_est_prices
    ], dtype=np.int64)

    # 수행능력점수 부족분 보전 반영: S_pq + S_price >= S_cut 확인
    r_eff_ratio, feasible_mask_arr = effective_floor(
        P_grid=base_step_bids,
        B=ctx.base_amt,
        S_pq=ctx.s_pq,
        S_cut=s_cut,
        smax=s_max,
        r_star=r_star,
        k=k_coef,
        r_announced=r_ann,
    )

    if r_eff_ratio is None or not np.any(feasible_mask_arr):
        return BidResult(
            optimal_step=-1, optimal_price=0, optimal_rate=0.0, win_prob=0.0,
            expected_profit=0, effective_floor_rate=round(r_ann * 100.0, 4),
            effective_floor_price=0, p_miss=1.0,
            ladder={"prices": base_step_bids.tolist(), "est_prices": step_est_prices.tolist(), "pmf": step_pmf.tolist()},
            feasible=False,
            warnings=["L4 적격 제약 투영 결과: 수행능력점수 부족으로 적격 통과 가능한 계단이 없습니다 (입찰 불가)."] + warnings,
        )

    # 수행능력점수가 만점 미달이어서 실효 하한율이 공고 하한율보다 상승한 경우 투찰가 재투영
    eff_rate_pct = max(r_ann * 100.0, r_eff_ratio * 100.0)
    step_bids = np.array([
        step_bid_from_est_price(int(ep), ctx.a_val, eff_rate_pct, wedge_won=19)
        for ep in step_est_prices
    ], dtype=np.int64)

    # L2: 극값 역추정 (개찰 이력 20건 이상 시 작동, 미달 시 발주처 사전분포 폴백)
    grid_rates = np.linspace(85.0, 95.0, 401)
    t1_list, t2_list, n_list = [], [], []
    if opening_hist:
        for row in opening_hist:
            if isinstance(row, dict) and "t1_rate" in row and "t2_rate" in row and "n_bidders" in row:
                t1_list.append(float(row["t1_rate"]))
                t2_list.append(float(row["t2_rate"]))
                n_list.append(float(row["n_bidders"]))

    if len(t1_list) >= MIN_EVT_SAMPLES:
        F_hat, f_hat = invert_rival_distribution(np.array(t1_list), np.array(t2_list), np.array(n_list), grid_rates)
        n_bid = float(np.mean(n_list))
    else:
        warnings.append(f"F-3: 개찰 표본 수(m={len(t1_list)}<{MIN_EVT_SAMPLES}) 부족으로 극값 역추정 대신 사전 경쟁분포 사용")
        n_bid = estimate_n_bidders(ctx.org, ctx.base_amt, n_list)
        center_r = (float( np.median(step_bids) ) / float(ctx.base_amt)) * 100.0
        F_hat = 1.0 / (1.0 + np.exp(-(grid_rates - center_r) / 0.08))
        f_hat = np.gradient(F_hat, grid_rates)

    # L3: 원가 추정 및 기대이익장 계산
    c_won, c_warns = cost_estimate(ctx.base_amt, ctx.company_econ)
    warnings.extend(c_warns)
    lam = float(ctx.company_econ.get("risk_lambda", 0.0)) if ctx.company_econ else 0.0

    exp_profits, win_probs = profit_field(
        step_bids, ctx.base_amt, step_pmf, c_won, F_hat, grid_rates, n_bid, lam=lam
    )

    # Feasible 집합 내에서 기대이익 최대화 계단 j* 선택
    masked_profits = np.where(feasible_mask_arr, exp_profits, -1e18)
    j_star = int(np.argmax(masked_profits))

    opt_price = int(step_bids[j_star])
    opt_est_price = int(step_est_prices[j_star])
    opt_rate = round((opt_price / float(ctx.base_amt)) * 100.0, 4)
    opt_win_prob = round(float(win_probs[j_star]), 4)
    opt_exp_profit = int(round(float(exp_profits[j_star])))

    # 하한선 미달 확률(p_miss): 실제 추첨 예정가격이 선택된 계단보다 높게 나와 우리 투찰가가 하한선 미달이 될 확률
    p_miss = float(np.mean(mc_prices > opt_est_price))
    eff_floor_price = int(step_bids[feasible_mask_arr].min())

    # L5: 온라인 캘리브레이션 지표(CRPS & Thompson 가중치) 요약 첨부
    crps_val = crps(mc_prices / float(ctx.base_amt) * 100.0, (opt_est_price / float(ctx.base_amt)) * 100.0)
    t_weights = thompson_weights({
        "M1_LEGACY": {"alpha": 2, "beta": 6},
        "M2_SNIPER": {"alpha": 3, "beta": 5},
        "M3_SINGULARITY": {"alpha": 5, "beta": 4},
        "M4_PANDORA": {"alpha": 4, "beta": 5},
        "M5_ENSEMBLE": {"alpha": 7, "beta": 3},
        "M6_LATTICE1365": {"alpha": 8, "beta": 2},
    }, seed=can_lad["seed_int"])

    return BidResult(
        optimal_step=j_star + 1,
        optimal_price=opt_price,
        optimal_rate=opt_rate,
        win_prob=opt_win_prob,
        expected_profit=opt_exp_profit,
        effective_floor_rate=round(eff_rate_pct, 4),
        effective_floor_price=eff_floor_price,
        p_miss=round(p_miss, 4),
        ladder={
            "prices": step_bids.tolist(),
            "est_prices": step_est_prices.tolist(),
            "pmf": step_pmf.tolist(),
            "expected_profits": exp_profits.tolist(),
            "win_probs": win_probs.tolist(),
            "lucky_4_slots": [i + 1 for i in ALL_COMBOS[j_star]],
            "l0_params": {"mu": mu, "delta": delta, "rho": rho},
            "l2_n_bidders": round(n_bid, 1),
            "l3_cost_won": c_won,
            "l5_crps": round(crps_val, 5),
            "l5_thompson_weights": t_weights,
        },
        feasible=True,
        warnings=warnings,
    )
