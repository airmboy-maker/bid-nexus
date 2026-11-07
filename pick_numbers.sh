#!/usr/bin/env python3
import sys
from decimal import Decimal
from bid_math_fixed import resolve_notice_record
from research.egr_bid.evidence_contract import VerifiedNotice
from research.egr_bid.robust_selector import egr_bid_recommend
from research.egr_bid.csv_loader import load_verified_history_from_csv
from research.egr_bid.report_formatter import compute_m1_to_m5_breakdown
from lattice1365.selector_ai import compute_ai_slot_selection_Automation

arg1 = sys.argv[1].strip() if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "R26BK01812785-000"
target_mode = sys.argv[2].strip().lower() if len(sys.argv) > 2 else "m5"  # m5 | egr | lattice

rec = resolve_notice_record(arg1, strict=True, allow_demo=False)
m1_m5 = compute_m1_to_m5_breakdown(
    rec["internal_id"], rec["base_amt"], rec["a_val"],
    rec["limit_rate"], Decimal("30.00"), rec["profile_key"], rec["net_cost_base"]
)
hist = load_verified_history_from_csv("research/egr_bid/verified_opening_template.csv")
notice = VerifiedNotice(
    notice_id=rec["internal_id"], revision_id="REV-0",
    source_sha256="41a5bfd7790732771f9430b13fb74c0ef7476f18",
    source_verified=True, is_demo_data=False, profile_key=rec["profile_key"],
    base_amt=rec["base_amt"], a_val=rec["a_val"], net_cost_base=rec["net_cost_base"],
    deadline_at=rec["deadline_date"], limit_rate=rec["limit_rate"],
)
egr_res = egr_bid_recommend(notice, hist)
lat_res = m1_m5["lattice_res"]

if target_mode == "egr" and egr_res.verified_rule_checks:
    target_ep = egr_res.verified_rule_checks["scenario_evaluation"]["scenarios"][2]["est_price"]
    mode_label = "번외 1: 제미나이 EGR-BID (M6-Q50 중앙 시나리오)"
elif target_mode == "lattice" and lat_res.feasible:
    target_ep = lat_res.ladder["est_prices"][lat_res.optimal_step - 1]
    mode_label = f"번외 2: 젠스파크 LATTICE-1365 (계단 #{lat_res.optimal_step})"
else:
    target_ep = m1_m5["m5_est_price"]
    mode_label = f"기준선: M5 양자계단 (계단 #{m1_m5['m5_step_no']})"

ai_pick = compute_ai_slot_selection_Automation(
    notice_no=rec["internal_id"],
    base_amt=rec["base_amt"],
    a_val=rec["a_val"],
    limit_rate_pct=float(rec["limit_rate"]),
    target_est_price=target_ep,
)

p2 = ai_pick["primary_2_pick"]
b2 = ai_pick["backup_2_pick"]
c4 = ai_pick["exact_combo_4"]

print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
print(f"┃ 🎯 [AI 복수예가 추첨번호 & 1,365 조합 자동 분석기] {rec['title']} ({rec['internal_id']})")
print(f"┃  • 기준 타점 모델 : {mode_label} (목표 예정가격: {target_ep:,}원)")
print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
print("┃ [1] 나라장터 전자입찰서 제출 화면 — AI 자동 추천 응찰 번호 (2개 체크)")
print(f"┃  👑 1순위 최적 응찰 번호 (Primary 2-Pick) : 【 {p2[0]}번 · {p2[1]}번 】 (다수결 코어 동조율 최상)")
print(f"┃  🛡️ 2순위 예비 응찰 번호 (Backup 2-Pick)  : 【 {b2[0]}번 · {b2[1]}번 】 (분산 방어 조합)")
print(f"┃  🍀 목표 타점 4개 조합 (Target 4-Slot)    :  {c4[0]}번 · {c4[1]}번 · {c4[2]}번 · {c4[3]}번 (계단 #{ai_pick['exact_step_no']}/1,365)")
print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
print("┃ [2] 1~15번 예비가격 슬롯별 AI 다수결 선택확률 및 행동편향 분석표")
print("┃ --------------------------------------------------------------------------------------")
print(f"┃  {'번호':<4} | {'예비가격(원)':>14} | {'사정률(%)':>9} | {'다수결 선택확률':>12} | {'행동편향 구간':<14} | {'AI 추천등급'}")
print("┃ --------------------------------------------------------------------------------------")
for s in ai_pick["slot_table"]:
    print(f"┃  {s['번호']:<4} | {s['예비가격(원)']:>14,} | {s['사정률(%)']:>8.4f}% | {s['AI 다수결 선택확률(%)']:>11.2f}% | {s['행동편향 분류']:<14} | {s['추천등급']}")
print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
print("┃ [3] 1,365개 조합(15C4) 중 목표 타점 근접 × 다수결 추첨 시너지 TOP 5 조합")
print("┃ --------------------------------------------------------------------------------------")
for row in ai_pick["top_10_combos"][:5]:
    print(
        f"┃  TOP {row['rank']} (계단 #{row['step_no']:<4}) : [{row['combo_str']:<19}] -> 핵심2픽({row['best_2_str']}) "
        f"| 예가 {row['est_price']:,}원 ({row['sajeong_rate']:.4f}%) | 시너지 {row['synergy_score']:.1f}점"
    )
print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
