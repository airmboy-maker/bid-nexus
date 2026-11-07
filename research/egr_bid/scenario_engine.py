from decimal import Decimal
from typing import List, Dict
from bid_math_fixed import (
    estimate_price, lower_limit, ceil_won, get_qual_profile,
    check_net_cost_98pct, evaluate_official_qual_score
)
from .evidence_contract import VerifiedNotice


def evaluate_candidates_across_scenarios(
    notice: VerifiedNotice,
    m6_dist: Dict,
    candidate_wedges: List[int] = (0, 19, 50, 100),
) -> Dict:
    """
    기존 bid_math_fixed.py의 Rule Engine을 수정 없이 그대로 호출하여
    M6 사정률 분위수 시나리오별 예정가격, 하한선, 98% 순공사원가, 공식 적격점수를 평가 (T07 준수).
    """
    prof = get_qual_profile(notice.profile_key)
    q_map = m6_dist["quantiles_pct"]
    scenario_keys = ["q10", "q25", "q50", "q75", "q90"]

    scenarios = []
    for sk in scenario_keys:
        r_pct = q_map[sk]
        ep = estimate_price(notice.base_amt, r_pct)
        cut = lower_limit(ep, notice.a_val, notice.limit_rate)
        nc_info = check_net_cost_98pct(cut, notice.net_cost_base, est_price=ep, base_amount=notice.base_amt)
        scenarios.append({
            "scenario_id": sk,
            "rate_pct": r_pct,
            "est_price": ep,
            "lower_limit": cut,
            "min_net_cost_98": nc_info["min_net_cost_bid"],
        })

    # 후보 투찰가 집합 형성: 각 시나리오 하한선 + 웨지
    candidate_bids = sorted({
        ceil_won(sc["lower_limit"] + w)
        for sc in scenarios
        for w in candidate_wedges
    })

    evaluated_candidates = []
    for b_amt in candidate_bids:
        scenario_outcomes = []
        eligible_count = 0
        for sc in scenarios:
            qual = evaluate_official_qual_score(
                b_amt, sc["est_price"], notice.a_val, notice.limit_rate,
                notice.perf_score, profile_key=notice.profile_key,
                net_cost_amount=notice.net_cost_base, base_amount=notice.base_amt
            )
            is_el = bool(qual["is_pass"])
            if is_el:
                eligible_count += 1
            scenario_outcomes.append({
                "scenario_id": sc["scenario_id"],
                "est_price": sc["est_price"],
                "lower_limit": sc["lower_limit"],
                "is_eligible": is_el,
                "total_score": qual["total_score"],
                "reject_reason": qual["reject_reason"],
                "verdict": qual["verdict"],
            })

        eligibility_ratio = Decimal(eligible_count) / Decimal(len(scenarios))
        evaluated_candidates.append({
            "bid_amount": b_amt,
            "eligible_scenarios": eligible_count,
            "total_scenarios": len(scenarios),
            "eligibility_ratio": float(eligibility_ratio),
            "has_any_ineligible": eligible_count < len(scenarios),
            "scenario_outcomes": scenario_outcomes,
        })

    return {
        "profile_key": notice.profile_key,
        "annex_code": prof["annex_code"],
        "scenarios": scenarios,
        "candidates": evaluated_candidates,
    }
