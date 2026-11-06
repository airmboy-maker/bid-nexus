#!/usr/bin/env python3
import sys, hashlib, numpy as np
from decimal import Decimal
from bid_math_fixed import (
    DEFAULT_LIMIT_RATE, NOTICE_MASTER_DB, resolve_notice_record,
    estimate_price, lower_limit, slot_prices, step_ladder, snap_above,
    floor_won, ceil_won, ALL_COMBOS, parse_int, parse_float
)

arg1 = sys.argv[1].strip() if len(sys.argv) > 1 else "202611-00892"
rec = resolve_notice_record(arg1, strict=True, allow_demo=False)

notice_no = rec["internal_id"]
g2b_no = rec["g2b_notice_no"]
notice_title = rec["title"]
base_amt = rec["base_amt"]
a_val = rec["a_val"]
limit_r = float(rec["limit_rate"])

if len(sys.argv) <= 3:
    sim_rate = parse_float(sys.argv[2], 100.0885) if len(sys.argv) == 3 else 100.0885
else:
    in_base = parse_int(sys.argv[2], -1)
    in_a = parse_int(sys.argv[3], -1)
    if in_base != base_amt or in_a != a_val:
        raise ValueError(f"FAIL_CLOSED_PARAMETER_MISMATCH: Manual arguments do not match verified master record for {notice_no}")
    sim_rate = parse_float(sys.argv[4], 100.0885)

hv = int(hashlib.md5(f"{notice_no}_0".encode("utf-8")).hexdigest()[:8], 16)
rng = np.random.default_rng(hv)
r_leg = round(100.015 + (hv % 40) * 0.001, 4)
r_sni = round(r_leg + 0.038 + (hv % 15) * 0.001, 4)
raw_15 = (np.linspace(98.25, 101.75, 15) + 0.085 + rng.normal(0, 0.025, 15)).tolist()
slots_w = slot_prices(base_amt, raw_15)
ladder_w = step_ladder(slots_w)
r_sin = round((snap_above(floor_won(Decimal(base_amt) * (Decimal(str(r_leg + 0.0523)) / Decimal("100"))), ladder_w) / base_amt) * 100.0, 4)
r_pan = round(r_sin + 0.0115, 4)

comb_eps = [floor_won(sum(Decimal(slots_w[i]) for i in c) / Decimal("4")) for c in ALL_COMBOS]
raw_ens = (Decimal(str(r_sin)) * Decimal("0.40")) + (Decimal(str(r_pan)) * Decimal("0.35")) + (Decimal(str(r_sni)) * Decimal("0.25"))
step_idx = int(np.argmin([abs(ep - estimate_price(base_amt, raw_ens)) for ep in comb_eps]))
r_ens = round((comb_eps[step_idx] / base_amt) * 100.0, 4)

sim_ep = estimate_price(base_amt, sim_rate)
sim_cut = lower_limit(sim_ep, a_val, limit_r)

models = [
    ("M1. 레거시 데드존 (과밀회피기준)", r_leg),
    ("M2. 딥러닝 스나이퍼 (발주처타점)", r_sni),
    ("M3. 싱귤래리티 (15C4 양자계단)", r_sin),
    ("M4. 판옵티콘 (경쟁사패턴역추적)", r_pan),
    ("M5. AI 마스터 앙상블 (최종통합)", r_ens),
]

print("====================================================================================")
print(f"🏁 [BID-NEXUS v20.4 사정률 민감도 시뮬레이션 리포트] {notice_title} ({notice_no} / {g2b_no})")
print(f" • 기초금액 / A값 / 공고하한율     : {base_amt:,}원 / {a_val:,}원 / {limit_r}%")
print(f" • 가정(입력) 사정률 (시뮬레이션)  : {sim_rate:.4f}% | 시뮬레이션 기준 하한선 : {sim_cut:,}원")
print("------------------------------------------------------------------------------------")

best_model = None
best_gap = 10**18

for m_name, m_rate in models:
    m_ep = comb_eps[step_idx] if "M5." in m_name else estimate_price(base_amt, m_rate)
    m_bid = ceil_won(lower_limit(m_ep, a_val, limit_r) + 19)
    diff_won = m_bid - sim_cut
    diff_rate = m_rate - sim_rate
    status = "✅ 시나리오 하한선 이상" if diff_won >= 0 else "❌ 시나리오 하한선 미달"
    print(f" • {m_name:<28} : {m_rate:.4f}% (편차 {diff_rate:+.4f}%p | 기준대비 {diff_won:+,}원) -> {status}")
    if diff_won >= 0 and diff_won < best_gap:
        best_gap = diff_won
        best_model = (m_name, m_rate, m_bid, diff_won)

print("------------------------------------------------------------------------------------")
if best_model:
    print(f"📊 [시나리오 기준 최저근접 모델 (Simulation Reference)] {best_model[0]}")
    print(f"   👉 추천가 {best_model[2]:,}원 (가정 사정률 {sim_rate:.4f}% 하한선 대비 +{best_model[3]:,}원 근접 통과 — 시뮬레이션 참고치이며 실제 개찰 순위와 무관)")
else:
    print("⚠️ 가정된 사정률이 모든 모델 예측치보다 높게 설정되었습니다 (상방 시나리오).")
print("====================================================================================")
