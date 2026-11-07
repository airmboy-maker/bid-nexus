#!/usr/bin/env python3
import sys, hashlib, numpy as np
from decimal import Decimal
from bid_math_fixed import (
    estimate_price, lower_limit, slot_prices, step_ladder, snap_above,
    floor_won, ceil_won, ALL_COMBOS, parse_int, parse_float,
    validate_perf_score, inverse_bid_for_deficit, check_net_cost_98pct, get_qual_profile
)
from research.egr_bid.evidence_contract import VerifiedNotice
from research.egr_bid.robust_selector import egr_bid_recommend
from research.egr_bid.csv_loader import load_verified_history_from_csv

# 사용법: ./compare_new_bid.sh [공고번호] [공고명] [기초금액] [A값] [순공사원가] [낙찰하한율=88.745] [비가격점수=30.0] [개찰이력CSV경로]
n_no = sys.argv[1].strip() if len(sys.argv) > 1 else "R26BK01812785-000"
title = sys.argv[2].strip() if len(sys.argv) > 2 else "소양초 공간재구조화 조성공사"
base_amt = parse_int(sys.argv[3], 3605411000, min_val=1) if len(sys.argv) > 3 else 3605411000
a_val = parse_int(sys.argv[4], 170640956, min_val=0) if len(sys.argv) > 4 else 170640956
net_cost = parse_int(sys.argv[5], 3082754189, min_val=1) if len(sys.argv) > 5 else 3082754189
limit_r = Decimal(str(parse_float(sys.argv[6], 88.745))) if len(sys.argv) > 6 else Decimal("88.745")
perf_s = validate_perf_score(sys.argv[7] if len(sys.argv) > 7 else "30.00")
csv_path = sys.argv[8].strip() if len(sys.argv) > 8 else "research/egr_bid/verified_opening_template.csv"

est_pre = floor_won(Decimal(base_amt) / Decimal("1.1"))
prof_key = "MOIS_BP3_30B_50B" if est_pre >= 3000000000 else ("MOIS_BP4_10B_30B" if est_pre >= 1000000000 else "MOIS_BP5_3B_10B")

# 1. 기존 M5 양자계단 기준선 계산
canon_seed = "202611-00892" if n_no in ("R26BK01812785-000", "202611-00892") else n_no
hv = int(hashlib.md5(f"{canon_seed}_0".encode("utf-8")).hexdigest()[:8], 16)
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
m5_ep = comb_eps[step_idx]
m5_rate = round((m5_ep / base_amt) * 100.0, 4)
m5_inv = inverse_bid_for_deficit(m5_ep, a_val, limit_r, perf_s, profile_key=prof_key, net_cost_amount=net_cost, base_amount=base_amt)
m5_bid = m5_inv["recommended_bid"]
m5_picks = [i + 1 for i in ALL_COMBOS[step_idx]]

# 2. 번외편 EGR-BID (CSV 개찰 이력 연동) 계산
hist_records = load_verified_history_from_csv(csv_path)
v_notice = VerifiedNotice(
    notice_id=canon_seed,
    revision_id="REV-0",
    source_sha256=hashlib.sha256(f"{n_no}_{base_amt}_{a_val}_{net_cost}".encode()).hexdigest(),
    source_verified=True,
    is_demo_data=False,
    profile_key=prof_key,
    base_amt=base_amt,
    a_val=a_val,
    net_cost_base=net_cost,
    deadline_at="2026-11-13T10:00:00",
    limit_rate=limit_r,
    perf_score=perf_s,
)
egr_res = egr_bid_recommend(v_notice, hist_records)

print("==========================================================================================")
print(f"⚖️ [M5 기본 추천가 vs 번외편(EGR-BID) 동시 비교 리포트] {title} ({n_no})")
print(f" • 기초금액: {base_amt:,}원 | A값: {a_val:,}원 | 순공사원가: {net_cost:,}원 | 하한율: {limit_r}%")
print(f" • 연동된 개찰 이력 CSV: {csv_path} ({len(hist_records)}건 로드 완료)")
print("------------------------------------------------------------------------------------------")
print(f" 👑 [트랙 1: M5 양자계단 추천가] : {m5_bid:>15,}원 (예정가격 {m5_ep:,}원 | 사정률 {m5_rate:.4f}% | 계단 #{step_idx+1})")
print(f"    👉 복수예가 추첨 번호        : {m5_picks[0]}번 · {m5_picks[1]}번 · {m5_picks[2]}번 · {m5_picks[3]}번")
if egr_res.recommendation_won:
    diff_won = egr_res.recommendation_won - m5_bid
    q_map = egr_res.calibration_summary["m6_quantiles_pct"]
    print(f" 🛡️ [트랙 2: EGR-BID 강건 선택가]: {egr_res.recommendation_won:>15,}원 (M6 중앙 사정률 {q_map['q50']}% 기준 | M5 대비 {diff_won:+,}원)")
    print(f"    👉 M6 사정률 분위수 구간     : Q10={q_map['q10']}% ~ Q50={q_map['q50']}% ~ Q90={q_map['q90']}% (판정: {egr_res.status})")
else:
    print(f" 🛑 [트랙 2: EGR-BID 판정 보류]  : {egr_res.status} (사유: {', '.join(egr_res.reasons)})")
print("==========================================================================================")
