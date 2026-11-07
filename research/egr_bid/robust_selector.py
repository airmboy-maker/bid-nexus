from decimal import Decimal
from typing import List, Dict, Optional
from bid_math_fixed import get_qual_profile, validate_perf_score
from .evidence_contract import (
    VerifiedNotice, HistoricalOpeningRecord, RecommendationResult,
    verify_notice_evidence, filter_and_validate_history
)
from .rate_distribution import estimate_m6_rate_distribution
from .competitor_distribution import estimate_m7_competitor_distribution
from .scenario_engine import evaluate_candidates_across_scenarios
from .abstain_policy import evaluate_m8_abstention


def egr_bid_recommend(
    notice: VerifiedNotice,
    verified_history: List[HistoricalOpeningRecord],
    policy: Optional[Dict] = None,
    cost_input: Optional[int] = None,
) -> RecommendationResult:
    """
    EGR-BID 메인 엔트리포인트 (기존 M1~M5 코어 불변 보존, 순수 상위 평가 계층)
    """
    policy = policy or {}
    cutoff_at = policy.get("data_cutoff_at", "2026-11-05T00:00:00")
    min_m6_samples = int(policy.get("min_m6_samples", 5))
    min_Scenario_elig_ratio = float(policy.get("min_scenario_eligibility_ratio", 0.60))
    max_pi80_width = Decimal(str(policy.get("max_pi80_width_pct", "0.8000")))
    latest_revs = policy.get("latest_revision_map", {})

    # 1. Notice & Rule Gate (T01, T02, T03, T04)
    ev_errors = verify_notice_evidence(notice, latest_revision_map=latest_revs)
    try:
        prof = get_qual_profile(notice.profile_key)
        validate_perf_score(notice.perf_score, max_perf_score=prof["perf_max"])
    except ValueError as e:
        ev_errors.append(f"FAIL_CLOSED_RULE_VALIDATION:{e}")

    if ev_errors:
        return RecommendationResult(
            status="FAIL_CLOSED",
            recommendation_won=None,
            verified_rule_checks={"passed": False, "errors": ev_errors},
            calibration_summary=None,
            evidence_ids=[],
            reasons=ev_errors,
            data_cutoff_at=cutoff_at,
        )

    # 2. Temporal Leakage & Provenance Gate (T05, T06)
    valid_hist, leak_errors, synthetic_only = filter_and_validate_history(verified_history, cutoff_at)
    if leak_errors:
        return RecommendationResult(
            status="FAIL_CLOSED",
            recommendation_won=None,
            verified_rule_checks={"passed": False, "errors": leak_errors},
            calibration_summary=None,
            evidence_ids=[],
            reasons=leak_errors,
            data_cutoff_at=cutoff_at,
        )

    if synthetic_only or len(valid_hist) == 0:
        return RecommendationResult(
            status="HOLD_NO_RELIABLE_RECOMMENDATION",
            recommendation_won=None,
            verified_rule_checks={"passed": True, "synthetic_only": True},
            calibration_summary=None,
            evidence_ids=[],
            reasons=["SYNTHETIC_OR_EMPTY_HISTORY_NO_PRODUCTION_LEARNING", "PROBABILITY_UNAVAILABLE"],
            data_cutoff_at=cutoff_at,
        )

    # 3. M6 & M7 Estimation
    m6_res = estimate_m6_rate_distribution(notice, valid_hist, min_samples=min_m6_samples)
    m7_res = estimate_m7_competitor_distribution(notice, valid_hist)

    # 4. M8 Abstention Check (T10, T11, T12)
    m8_res = evaluate_m8_abstention(notice, m6_res, m7_res, max_pi80_width_pct=max_pi80_width, cost_input=cost_input)
    if m8_res["should_abstain"]:
        return RecommendationResult(
            status="HOLD_NO_RELIABLE_RECOMMENDATION",
            recommendation_won=None,
            verified_rule_checks={"passed": True},
            calibration_summary={"m6": m6_res, "m7_available": m7_res.get("available", False)},
            evidence_ids=[r.notice_id for r in valid_hist],
            reasons=m8_res["hold_reasons"] + m8_res["advisory_notes"],
            data_cutoff_at=cutoff_at,
        )

    # 5. Scenario Evaluation & Hard Eligibility Filtering (T07, T12)
    scen_eval = evaluate_candidates_across_scenarios(notice, m6_res)
    robust_candidates = [
        c for c in scen_eval["candidates"]
        if c["eligibility_ratio"] >= min_Scenario_elig_ratio
    ]

    if not robust_candidates:
        return RecommendationResult(
            status="HOLD_NO_RELIABLE_RECOMMENDATION",
            recommendation_won=None,
            verified_rule_checks={"passed": True, "scenario_evaluation": scen_eval},
            calibration_summary={"m6": m6_res, "m7_available": m7_res.get("available", False)},
            evidence_ids=[r.notice_id for r in valid_hist],
            reasons=["NO_CANDIDATE_MEETS_ROBUST_ELIGIBILITY_THRESHOLD"] + m8_res["advisory_notes"],
            data_cutoff_at=cutoff_at,
        )

    # 강건 적격 후보 중 최저 적격 투찰가(또는 검증된 원가 존재 시 양(+)의 마진 충족 후보) 선택
    if cost_input is not None and int(cost_input) > 0:
        profitable = [c for c in robust_candidates if c["bid_amount"] > int(cost_input)]
        if not profitable:
            return RecommendationResult(
                status="HOLD_NO_RELIABLE_RECOMMENDATION",
                recommendation_won=None,
                verified_rule_checks={"passed": True, "scenario_evaluation": scen_eval},
                calibration_summary={"m6": m6_res},
                evidence_ids=[r.notice_id for r in valid_hist],
                reasons=["BELOW_VERIFIED_FIRM_COST"],
                data_cutoff_at=cutoff_at,
            )
        chosen = profitable[0]
        profit_info = {"verified_expected_margin_won": chosen["bid_amount"] - int(cost_input)}
    else:
        chosen = robust_candidates[0]
        # T12: 회사 원가가 없을 때는 est_profit을 실이익으로 표시하지 않음
        profit_info = {"verified_expected_margin_won": None, "cost_status": "COST_UNKNOWN"}

    return RecommendationResult(
        status="PASS_ADVISORY",
        recommendation_won=chosen["bid_amount"],
        verified_rule_checks={
            "passed": True,
            "chosen_candidate": chosen,
            "scenario_evaluation": scen_eval,
            "profit_info": profit_info,
        },
        calibration_summary={
            "m6_quantiles_pct": {k: str(v) for k, v in m6_res["quantiles_pct"].items()},
            "m6_pi80_width_pct": str(m6_res["pi80_width_pct"]),
            "m7_available": m7_res.get("available", False),
        },
        evidence_ids=[r.notice_id for r in valid_hist],
        reasons=["ROBUST_SCENARIO_ADVISORY_SELECTED"] + m8_res["advisory_notes"],
        data_cutoff_at=cutoff_at,
    )
