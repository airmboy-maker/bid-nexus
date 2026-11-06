#!/usr/bin/env python3
import ast
import re
import subprocess
from decimal import Decimal
from bid_math_fixed import (
    OFFICIAL_QUAL_PROFILES, NOTICE_MASTER_DB, resolve_notice_record, get_qual_profile,
    SafeDict, ensure_safe_dict, _dec, parse_int, parse_float, validate_perf_score,
    ceil_won, floor_won, estimate_price, lower_limit, check_net_cost_98pct,
    evaluate_official_qual_score, inverse_bid_for_deficit, ALL_COMBOS
)

def test_1_net_cost_3082754189_and_exact_3023839133_boundary():
    rec = resolve_notice_record("R26BK01812785-000", strict=True, allow_demo=False)
    assert rec["net_cost_base"] == 3082754189
    assert rec["source_verified"] is True and rec["is_demo_data"] is False

    nc_info = check_net_cost_98pct(3221729592, 3082754189, est_price=3608680977, base_amount=3605411000)
    assert nc_info["min_net_cost_bid"] == 3023839133
    assert nc_info["is_valid"] is True

    q_nc_fail = evaluate_official_qual_score(
        3023839132, 3608680977, 170640956, "88.745", Decimal("30.00"),
        profile_key="MOIS_BP3_30B_50B", net_cost_amount=3082754189, base_amount=3605411000
    )
    assert q_nc_fail["is_pass"] is False and q_nc_fail["reject_reason"] == "REJECT_BELOW_98PCT_NET_COST"

    nc_boundary_pass = check_net_cost_98pct(3023839133, 3082754189, est_price=3608680977, base_amount=3605411000)
    assert nc_boundary_pass["is_valid"] is True

    # [14차 감사 필수 요구] 순공사원가 누락(None 또는 0) 시 즉시 FAIL_CLOSED_MISSING_NET_COST 예외 발생 검증
    for missing_nc in (None, 0, -100):
        try:
            evaluate_official_qual_score(
                3221729592, 3608680977, 170640956, "88.745", Decimal("30.00"),
                profile_key="MOIS_BP3_30B_50B", net_cost_amount=missing_nc, base_amount=3605411000
            )
            raise AssertionError(f"Must fail-closed when net_cost_amount={missing_nc!r}")
        except ValueError as e:
            assert "FAIL_CLOSED_MISSING_NET_COST" in str(e)

def test_2_annex3_high_rate_65pt_special_rule_and_5th_decimal_rounding():
    ep = 3608680977
    av = 170640956
    denom = Decimal(ep - av)
    test_cases = [
        (Decimal("88.7450"), Decimal("65.00")),
        (Decimal("90.0000"), Decimal("70.00")),
        (Decimal("91.2500"), Decimal("65.00")),
        (Decimal("91.3000"), Decimal("65.00")),
        (Decimal("92.0000"), Decimal("65.00")),
        (Decimal("93.0000"), Decimal("65.00")),
    ]
    for target_eff_pct, expected_score in test_cases:
        bid_for_rate = ceil_won(denom * (target_eff_pct / Decimal("100")) + Decimal(av))
        res = evaluate_official_qual_score(
            bid_for_rate, ep, av, "88.745", Decimal("30.00"),
            profile_key="MOIS_BP3_30B_50B", net_cost_amount=3082754189, base_amount=3605411000
        )
        assert res["price_score"] == expected_score

def test_3_unknown_and_unverified_demo_notice_fail_closed_all_cli_paths():
    # 1. 일반 호출 차단 검증
    for bad_id in ("UNKNOWN-NOTICE", "", None, "999999-99999"):
        try:
            resolve_notice_record(bad_id, strict=True, allow_demo=False)
            raise AssertionError(f"Should fail-closed on {bad_id}")
        except ValueError:
            pass

    for demo_id in ("202611-09999", "202611-03011", "202611-03110", "202611-03429"):
        proc_demo = subprocess.run(["./bid.sh", demo_id], capture_output=True, text=True)
        assert proc_demo.returncode != 0 and "FAIL_CLOSED_UNVERIFIED_DEMO_NOTICE" in proc_demo.stderr

    # 2. [14차 감사 핵심 요구사항] 수동 6인자 호출 경로에서도 데모 공고(202611-09999) 및 미등록 공고(UNKNOWN-NOTICE) 차단 검증!
    proc_manual_demo = subprocess.run(
        ["./bid.sh", "202611-09999", "4250000000", "195400000", "88.745", "30", "MOIS_BP3_30B_50B"],
        capture_output=True, text=True
    )
    assert proc_manual_demo.returncode != 0 and "FAIL_CLOSED_UNVERIFIED_DEMO_NOTICE" in proc_manual_demo.stderr

    proc_manual_unknown = subprocess.run(
        ["./bid.sh", "UNKNOWN-NOTICE", "3605411000", "170640956", "88.745", "30", "MOIS_BP3_30B_50B"],
        capture_output=True, text=True
    )
    assert proc_manual_unknown.returncode != 0 and "FAIL_CLOSED_UNKNOWN_NOTICE" in proc_manual_unknown.stderr

    # 3. 검증된 소양초 공고라도 수동 7번째 인자(순공사원가)에 0 또는 불일치 값을 넣으면 차단되는지 검증
    proc_manual_bad_nc = subprocess.run(
        ["./bid.sh", "202611-00892", "3605411000", "170640956", "88.745", "30", "MOIS_BP3_30B_50B", "0"],
        capture_output=True, text=True
    )
    assert proc_manual_bad_nc.returncode != 0 and "FAIL_CLOSED_PARAMETER_MISMATCH" in proc_manual_bad_nc.stderr

def test_4_full_web_schema_and_cli_4way_integration():
    with open("app_v2.py", "r", encoding="utf-8") as f:
        src = f.read()
    assert "87.745" not in src
    assert re.search(r"\b35\.8\b", src) is None
    assert re.search(r"\b99\.8\b", src) is None

    tree = ast.parse(src)
    isolated_ns = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in (
            "ensure_safe_dict", "verify_ocr_engineer_counts",
            "_v204_Sync_Top_KPI", "_compute_master_ensemble_for_notice"
        ):
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, "app_v2.py", "exec"), isolated_ns)

    kpi_fn = isolated_ns["_v204_Sync_Top_KPI"]
    ens_fn = isolated_ns["_compute_master_ensemble_for_notice"]

    dict_int = {"id": "202611-00892", "base": 3605411000, "a_val": 170640956, "limit": 88.745}
    dict_g2b = {"id": "R26BK01812785-000", "base": 3605411000, "a_val": 170640956, "limit": 88.745}
    res_dict_int = ens_fn(dict_int, 0)
    res_dict_g2b = ens_fn(dict_g2b, 0)

    required_ui_keys = ("rate", "opt_bid", "est_profit", "win_rate", "def_rate", "step_no", "lucky_4")
    for rk in required_ui_keys:
        assert rk in res_dict_int and rk in res_dict_g2b

    assert res_dict_int["opt_bid"] == res_dict_g2b["opt_bid"] == 3221729592
    assert res_dict_int["rate"] == res_dict_g2b["rate"] == 100.0907
    assert res_dict_int["step_no"] == res_dict_g2b["step_no"] == 238
    assert res_dict_int["lucky_4"] == res_dict_g2b["lucky_4"] == [1, 5, 11, 15]
    assert res_dict_int["est_price"] == res_dict_g2b["est_price"] == 3608680977
    assert res_dict_int["policy_status"] == res_dict_g2b["policy_status"] == "PASS_FULL_PERF"

    kpi_int_bid, _, kpi_int_prof, _ = kpi_fn(3605411000, 170640956, 88.745, "202611-00892")
    kpi_g2b_bid, _, kpi_g2b_prof, _ = kpi_fn(3605411000, 170640956, 88.745, "R26BK01812785-000")
    assert kpi_int_bid == kpi_g2b_bid == 3221729592
    assert res_dict_int["est_profit"] == kpi_int_prof == kpi_g2b_prof

    for demo_input in ({"id": "202611-09999"}, "202611-03110"):
        try:
            ens_fn(demo_input, 0)
            raise AssertionError("Web ensemble must isolate unverified demo notices in production mode")
        except ValueError as e:
            assert "FAIL_CLOSED_UNVERIFIED_DEMO_NOTICE" in str(e)

    res_29_dict = ens_fn({"id": "R26BK01812785-000", "perf_score": 29.0}, 0)
    assert res_29_dict["recommended_bid"] == 3221729592
    assert res_29_dict["policy_status"] == "HOLD_SINGLE_BID_ONLY_NO_JV_ALLOWED"

    cli_int = subprocess.check_output("./bid.sh 202611-00892", shell=True, text=True)
    cli_g2b = subprocess.check_output("./bid.sh R26BK01812785-000", shell=True, text=True)
    cli_bat = subprocess.check_output("./batch_bid.sh", shell=True, text=True)
    assert cli_int == cli_g2b
    assert "3,221,729,592" in cli_int and "3,023,839,133원" in cli_int
    assert "1번 · 5번 · 11번 · 15번" in cli_int
    assert "3,221,729,592" in cli_bat and "202611-09999" not in cli_bat

def test_5_app_wide_43_dicts_zero_mismatch_and_js_labels():
    with open("app_v2.py", "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    checked_dicts = 0
    mismatches = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            d_map = {}
            for k_node, v_node in zip(node.keys, node.values):
                if isinstance(k_node, ast.Constant) and isinstance(v_node, (ast.Constant, ast.UnaryOp)):
                    try:
                        d_map[str(k_node.value)] = ast.literal_eval(v_node)
                    except Exception:
                        pass
            nid = d_map.get("id") or d_map.get("notice_no") or d_map.get("공고번호")
            if isinstance(nid, str) and re.match(r"^2026\d{2}-\d{5}$", nid):
                rec = resolve_notice_record(nid, strict=True, allow_demo=True)
                checked_dicts += 1
                for tk in ("title", "name", "공고명", "공사명"):
                    if tk in d_map and d_map[tk] != rec["title"]:
                        mismatches.append((nid, tk, d_map[tk], rec["title"]))
                for bk in ("base", "base_amt", "기초금액", "기초"):
                    if bk in d_map and int(d_map[bk]) != rec["base_amt"]:
                        mismatches.append((nid, bk, d_map[bk], rec["base_amt"]))
                for ak in ("a_val", "a", "A값"):
                    if ak in d_map and int(d_map[ak]) != rec["a_val"]:
                        mismatches.append((nid, ak, d_map[ak], rec["a_val"]))
                for dk in ("deadline", "deadline_date", "마감일", "마감", "end_dt", "close_dt"):
                    if dk in d_map and "2026-" in str(d_map[dk]) and d_map[dk] != rec["deadline_date"]:
                        mismatches.append((nid, dk, d_map[dk], rec["deadline_date"]))

    assert checked_dicts == 43, f"Expected 43 dicts checked, got {checked_dicts}"
    assert len(mismatches) == 0, f"Found field mismatches: {mismatches}"

    banned_phrases = [
        "기대 낙찰률", "기대낙찰률", "평균 낙찰률", "평균낙찰률",
        "일반 대비 15배", "방어율", "🏆 낙찰률", "(방어 '", "(방어 "
    ]
    for phrase in banned_phrases:
        assert phrase not in src, f"Banned phrase {phrase!r} still exists in app_v2.py"

if __name__ == "__main__":
    test_1_net_cost_3082754189_and_exact_3023839133_boundary()
    test_2_annex3_high_rate_65pt_special_rule_and_5th_decimal_rounding()
    test_3_unknown_and_unverified_demo_notice_fail_closed_all_cli_paths()
    test_4_full_web_schema_and_cli_4way_integration()
    test_5_app_wide_43_dicts_zero_mismatch_and_js_labels()
    print("✅ [ROUND 15 ALL 5/5 TEST SUITES PASSED WITH EXIT CODE 0] CLI 수동 6인자 데모/미등록/원가누락 우회 완전 차단 완료")
