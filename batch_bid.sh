#!/usr/bin/env python3
import sys, hashlib, numpy as np
from decimal import Decimal
from bid_math_fixed import (
    NOTICE_MASTER_DB, get_qual_profile, estimate_price, slot_prices, step_ladder,
    snap_above, floor_won, ALL_COMBOS, validate_perf_score, inverse_bid_for_deficit
)

include_demo = ("--include-demo" in sys.argv)
args = [a for a in sys.argv[1:] if a != "--include-demo"]
user_score_arg = args[0] if len(args) > 0 else None

# [13차 감사 필수 조치] 기본 운영 모드에서는 source_verified=True이고 is_demo_data=False인 검증 완료 실공고만 추천 실행!
target_notices = {
    k: rec for k, rec in NOTICE_MASTER_DB.items()
    if include_demo or (rec.get("source_verified", False) and not rec.get("is_demo_data", True))
}
isolated_demo_count = len(NOTICE_MASTER_DB) - len(target_notices)

print("====================================================================================================================================================")
print(f"👑 [BID-NEXUS v20.4 실전 검증 공고 일괄 브리핑] 운영 추천 대상: {len(target_notices)}건 (미검증 데모 격리 제외: {isolated_demo_count}건)")
print("====================================================================================================================================================")
print(f"{'내부/G2B번호':<29} | {'공고명':<20} | {'별표/하한율':<15} | {'순수하한선(원)':>14} | {'공식추천투찰가(원)':>15} | {'공동도급':<8} | {'판정상태'}")
print("----------------------------------------------------------------------------------------------------------------------------------------------------")

for n_no, rec in target_notices.items():
    n_title = rec["title"]
    base_amt = rec["base_amt"]
    a_val = rec["a_val"]
    limit_r = rec["limit_rate"]
    profile_key = rec["profile_key"]
    jv_allowed = rec["joint_venture_allowed"]
    net_cost_base = rec["net_cost_base"]
    prof = get_qual_profile(profile_key)

    # 프로파일별 수행능력 배점한도(예: 별표3=30점, 별표5=20점)에 맞춰 입력 점수 검증 (일률 30점 전달 금지)
    raw_score = user_score_arg if user_score_arg is not None else prof["perf_max"]
    perf_score = validate_perf_score(raw_score, max_perf_score=prof["perf_max"])

    hv = int(hashlib.md5(f"{n_no}_0".encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.default_rng(hv)
    r_leg = round(100.015 + (hv % 40) * 0.001, 4)
    r_sni = round(r_leg + 0.038 + (hv % 15) * 0.001, 4)
    raw_15 = (np.linspace(98.25, 101.75, 15) + 0.085 + rng.normal(0, 0.025, 15)).tolist()
    slots_w = slot_prices(base_amt, raw_15)
    ladder_w = step_ladder(slots_w)
    r_sin = round((snap_above(floor_won(Decimal(base_amt) * (Decimal(str(r_leg + 0.0523)) / Decimal("100"))), ladder_w) / base_amt) * 100.0, 4)
    r_pan = round(r_sin + 0.0115, 4)
    raw_ens = (Decimal(str(r_sin)) * Decimal("0.40")) + (Decimal(str(r_pan)) * Decimal("0.35")) + (Decimal(str(r_sni)) * Decimal("0.25"))

    comb_eps = [floor_won(sum(Decimal(slots_w[i]) for i in c) / Decimal("4")) for c in ALL_COMBOS]
    step_idx = int(np.argmin([abs(ep - estimate_price(base_amt, raw_ens)) for ep in comb_eps]))
    exact_ep = comb_eps[step_idx]

    inv_info = inverse_bid_for_deficit(
        exact_ep, a_val, limit_r, perf_score,
        profile_key=profile_key, joint_venture_allowed=jv_allowed, net_cost_amount=net_cost_base, base_amount=base_amt
    )
    pure_cut = inv_info["pure_cut"]
    rec_bid = inv_info["recommended_bid"]
    id_col = f"{n_no}({rec['g2b_notice_no'][:11]})"
    br_col = f"{prof['annex_code']}/{limit_r}%"
    jv_col = "허용" if jv_allowed else "불허"
    st_str = "PASS(95점통과)" if not inv_info["has_deficit"] else inv_info["policy_status"]
    print(f"{id_col:<29} | {n_title:<18} | {br_col:<15} | {pure_cut:>14,} | {rec_bid:>15,} | {jv_col:<6} | {st_str}")

print("====================================================================================================================================================")
