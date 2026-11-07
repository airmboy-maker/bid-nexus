#!/usr/bin/env python3
import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lattice1365.config import ceil_won
from lattice1365.slots import estimate_org_params, simulate_slots
from lattice1365.qualify import effective_floor
from lattice1365.engine import BidContext, compute_optimal_bid


def _sample_ctx(s_pq: float = 30.0) -> BidContext:
    return BidContext(
        notice_no="R26BK01812785-000",
        org="강원특별자치도춘천교육지원청",
        base_amt=3605411000,
        a_val=170640956,
        s_pq=s_pq,
        notice_params={
            "s_max": 70.0,
            "r_star": 0.90,
            "k_coef": 4.0,
            "s_cut": 95.0,
            "r_announced": 0.88745,
        },
        company_econ={
            "direct_cost_ratio": 0.815,
            "indirect_ratio": 0.030,
            "finance_ratio": 0.010,
            "risk_lambda": 0.1,
        },
    )


def test_no_banker_rounding():
    """1. 원단위 절상이 은행가 반올림에 먹히지 않는지 검증"""
    raw = 3220267461.4885
    assert ceil_won(raw) == 3220267462
    assert round(raw) == 3220267461


def test_lattice_containment():
    """2. 모든 최적 투찰가가 1,365 계단 위에 있는지 검증"""
    ctx = _sample_ctx(30.0)
    res = compute_optimal_bid(ctx)
    assert res.feasible is True
    assert res.optimal_price in set(res.ladder["prices"])
    assert len(res.ladder["prices"]) == 1365


def test_effective_floor_monotone():
    """3. 수행능력점수가 높을수록 실효 하한은 낮아져야 한다 (단조성)"""
    p_grid = np.linspace(3000000000, 3450000000, 500)
    floors = []
    for s in [26.0, 27.5, 29.0, 30.0]:
        r_eff, _ = effective_floor(
            P_grid=p_grid, B=3605411000, S_pq=s, S_cut=95.0,
            smax=70.0, r_star=0.90, k=4.0, r_announced=0.85
        )
        assert r_eff is not None
        floors.append(round(r_eff, 6))
    assert floors == sorted(floors, reverse=True)


def test_feasible_empty_returns_flag():
    """4. feasible 공집합 시 예외가 아니라 feasible=False 반환"""
    ctx_low = _sample_ctx(s_pq=15.0)  # 만점 70점 + 15점 = 85점 < 95점이므로 무조건 불가능
    res = compute_optimal_bid(ctx_low)
    assert res.feasible is False
    assert len(res.warnings) > 0


def test_rho_identification():
    """5. rho=0.5로 생성한 데이터에서 rho 추정 오차 < 0.1"""
    rng = np.random.default_rng(12345)
    sim_data = simulate_slots(mu=100.0, delta=0.5, rho=0.5, n_sims=400, rng=rng)
    est = estimate_org_params(slots_history=sim_data.tolist())
    assert abs(est["rho"] - 0.5) < 0.1


def test_reproducibility():
    """6. 동일 공고번호 -> 동일 결과 (감사 추적성)"""
    ctx = _sample_ctx(30.0)
    a = compute_optimal_bid(ctx)
    b = compute_optimal_bid(ctx)
    assert a.optimal_price == b.optimal_price
    assert a.optimal_step == b.optimal_step


if __name__ == "__main__":
    test_no_banker_rounding()
    test_lattice_containment()
    test_effective_floor_monotone()
    test_feasible_empty_returns_flag()
    test_rho_identification()
    test_reproducibility()
    print("✅ [LATTICE-1365 ALL 6/6 MANDATORY REGRESSION TESTS PASSED] L0~L5 계단 확률장 엔진 검증 완료!")
