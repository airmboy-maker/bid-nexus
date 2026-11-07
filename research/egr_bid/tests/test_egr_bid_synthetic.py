#!/usr/bin/env python3
import os
import sys
import subprocess
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from research.egr_bid.evidence_contract import VerifiedNotice, HistoricalOpeningRecord
from research.egr_bid.robust_selector import egr_bid_recommend


def _make_valid_notice(**overrides) -> VerifiedNotice:
    base = dict(
        notice_id="202611-00892",
        revision_id="REV-0",
        source_sha256="a1b2c3d4e5f60718293a4b5c6d7e8f90",
        source_verified=True,
        is_demo_data=False,
        profile_key="MOIS_BP3_30B_50B",
        base_amt=3605411000,
        a_val=170640956,
        net_cost_base=3082754189,
        deadline_at="2026-11-13T10:00:00",
        limit_rate=Decimal("88.745"),
        perf_score=Decimal("30.00"),
        joint_venture_allowed=False,
        provenance_class="OFFICIAL_VERIFIED",
    )
    base.update(overrides)
    return VerifiedNotice(**base)


def _make_verified_history(n=6, rate_spread=0.0004, with_comp=True, provenance="OFFICIAL_VERIFIED"):
    rows = []
    for i in range(n):
        mult = Decimal("1.0002") + Decimal(str(i * rate_spread))
        ep = int(Decimal(3605411000) * mult)
        comp_bid = int(Decimal(ep - 170640956) * Decimal("0.8875") + Decimal(170640956)) if with_comp else None
        rows.append(
            HistoricalOpeningRecord(
                notice_id=f"HIST-2026-{i+1:03d}",
                revision_id="REV-0",
                source_sha256=f"sha256_verified_hist_record_{i+1:03d}_abcdef",
                source_verified=(provenance == "OFFICIAL_VERIFIED"),
                observed_at="2026-10-01T09:00:00",
                published_at="2026-10-01T09:00:00",
                deadline_at="2026-10-10T10:00:00",
                opening_at="2026-10-10T11:00:00",
                asof_feature_timestamp="2026-10-10T09:30:00",
                agency_id="CHUNCHEON_EDU",
                work_category="ARCH",
                region="GANGWON",
                base_amt=3605411000,
                a_val=170640956,
                limit_rate=Decimal("88.745"),
                profile_key="MOIS_BP3_30B_50B",
                net_cost_base=3082754189,
                estimated_price_final=ep,
                participant_count=42 + i,
                top_valid_competitor_bid=comp_bid,
                provenance_class=provenance,
            )
        )
    return rows


def test_T01_unknown_demo_untrusted_fail_closed():
    hist = _make_verified_history()
    for bad in (
        _make_valid_notice(notice_id=""),
        _make_valid_notice(is_demo_data=True),
        _make_valid_notice(provenance_class="UNKNOWN"),
    ):
        res = egr_bid_recommend(bad, hist)
        assert res.status == "FAIL_CLOSED" and res.recommendation_won is None


def test_T02_missing_source_hash_fail_closed():
    hist = _make_verified_history()
    res = egr_bid_recommend(_make_valid_notice(source_verified=True, source_sha256=""), hist)
    assert res.status == "FAIL_CLOSED" and "FAIL_CLOSED_MISSING_SOURCE_HASH" in res.reasons


def test_T03_invalid_net_cost_profile_score_fail_closed():
    hist = _make_verified_history()
    for bad in (
        _make_valid_notice(net_cost_base=0),
        _make_valid_notice(a_val=-10),
        _make_valid_notice(profile_key="UNKNOWN_PROF"),
        _make_valid_notice(perf_score=Decimal("31.00")),
    ):
        res = egr_bid_recommend(bad, hist)
        assert res.status == "FAIL_CLOSED"


def test_T04_revision_conflict_fail_closed():
    hist = _make_verified_history()
    res = egr_bid_recommend(
        _make_valid_notice(revision_id="REV-0"),
        hist,
        policy={"latest_revision_map": {"202611-00892": "REV-1"}},
    )
    assert res.status == "FAIL_CLOSED"
    assert any("REVISION_CONFLICT" in r for r in res.reasons)


def test_T05_temporal_leakage_fail_closed():
    leaked_hist = _make_verified_history()
    leaked_hist[0] = HistoricalOpeningRecord(
        **{**leaked_hist[0].__dict__, "asof_feature_timestamp": "2026-10-10T12:00:00"}  # >= opening_at
    )
    res = egr_bid_recommend(_make_valid_notice(), leaked_hist)
    assert res.status == "FAIL_CLOSED"
    assert any("TEMPORAL_LEAKAGE" in r for r in res.reasons)


def test_T06_synthetic_only_history_holds():
    syn_hist = _make_verified_history(provenance="DEMO_SYNTHETIC")
    res = egr_bid_recommend(_make_valid_notice(), syn_hist)
    assert res.status == "HOLD_NO_RELIABLE_RECOMMENDATION"
    assert res.recommendation_won is None
    assert res.validation_tag == "NOT_PRODUCTION_VALIDATED"


def test_T07_scenario_specific_eligibility_and_robust_filtering():
    hist = _make_verified_history()
    res = egr_bid_recommend(_make_valid_notice(), hist)
    assert res.status == "PASS_ADVISORY"
    scen_eval = res.verified_rule_checks["scenario_evaluation"]
    # 낮은 사정률(q10) 하한선 기준 후보는 높은 사정률(q90) 시나리오에서 하한선 미달(is_eligible=False)이 명시적으로 기록됨
    lowest_cand = scen_eval["candidates"][0]
    assert lowest_cand["has_any_ineligible"] is True
    # 반면 최종 선택된 강건 후보는 요구 강건성 비율(>=0.60)을 충족함
    chosen = res.verified_rule_checks["chosen_candidate"]
    assert chosen["eligibility_ratio"] >= 0.60


def test_T08_deterministic_reproducibility():
    hist = _make_verified_history()
    notice = _make_valid_notice()
    results = [egr_bid_recommend(notice, hist) for _ in range(5)]
    first_won = results[0].recommendation_won
    assert first_won is not None
    for r in results[1:]:
        assert r.recommendation_won == first_won
        assert r.reasons == results[0].reasons


def test_T09_baseline_m5_and_round15_suite_preserved():
    proc = subprocess.run(["./test_audit_suite.py"], capture_output=True, text=True)
    assert proc.returncode == 0 and "ALL 5/5 TEST SUITES PASSED" in proc.stdout


def test_T10_excessive_uncertainty_triggers_m8_hold():
    wide_hist = _make_verified_history(rate_spread=0.015)  # 80% 예측구간 폭이 0.80%p 초과하도록 유도
    res = egr_bid_recommend(_make_valid_notice(), wide_hist, policy={"max_pi80_width_pct": "0.5000"})
    assert res.status == "HOLD_NO_RELIABLE_RECOMMENDATION"
    assert any("M8_EXCESSIVE_UNCERTAINTY_PI80" in r for r in res.reasons)


def test_T11_missing_competitor_and_cost_reasons_separated():
    hist_no_comp = _make_verified_history(with_comp=False)
    res = egr_bid_recommend(_make_valid_notice(), hist_no_comp, cost_input=None)
    assert "PROBABILITY_UNAVAILABLE" in res.reasons
    assert "COST_UNKNOWN" in res.reasons


def test_T12_no_unverified_profit_displayed_when_cost_unknown():
    hist = _make_verified_history()
    res = egr_bid_recommend(_make_valid_notice(), hist, cost_input=None)
    p_info = res.verified_rule_checks["profit_info"]
    assert p_info["verified_expected_margin_won"] is None
    assert p_info["cost_status"] == "COST_UNKNOWN"


if __name__ == "__main__":
    test_T01_unknown_demo_untrusted_fail_closed()
    test_T02_missing_source_hash_fail_closed()
    test_T03_invalid_net_cost_profile_score_fail_closed()
    test_T04_revision_conflict_fail_closed()
    test_T05_temporal_leakage_fail_closed()
    test_T06_synthetic_only_history_holds()
    test_T07_scenario_specific_eligibility_and_robust_filtering()
    test_T08_deterministic_reproducibility()
    test_T09_baseline_m5_and_round15_suite_preserved()
    test_T10_excessive_uncertainty_triggers_m8_hold()
    test_T11_missing_competitor_and_cost_reasons_separated()
    test_T12_no_unverified_profit_displayed_when_cost_unknown()
    print("✅ [EGR-BID ADD-ON ALL 12/12 TESTS (T01~T12) PASSED] 기존 15차 코어 무결성 100% 보존 + M6·M7·M8 샌드박스 검증 완료!")
