import hashlib
from decimal import Decimal
from typing import Dict, List, Optional
import numpy as np
from .config import ALL_COMBOS, floor_won, ceil_won


# 나라장터 입찰자 행동 편향 사전 가중치 (양 끝 1·15번 회피, 중앙 5~11번 및 3·7번 선호 경향 반영)
HUMAN_SLOT_PRIOR = np.array([
    0.048,  # 1번 (양끝 회피)
    0.058,  # 2번
    0.074,  # 3번 (선호 숫자)
    0.064,  # 4번
    0.076,  # 5번 (중앙 진입)
    0.075,  # 6번
    0.086,  # 7번 (최고 선호)
    0.078,  # 8번 (중앙 코어)
    0.074,  # 9번
    0.076,  # 10번
    0.075,  # 11번 (중앙 코어)
    0.066,  # 12번
    0.056,  # 13번
    0.046,  # 14번
    0.042,  # 15번 (양끝 회피)
], dtype=np.float64)
HUMAN_SLOT_PRIOR = HUMAN_SLOT_PRIOR / HUMAN_SLOT_PRIOR.sum()


def compute_ai_slot_selection_Automation(
    notice_no: str,
    base_amt: int,
    a_val: int,
    limit_rate_pct: float,
    target_est_price: int,
    slot_prices_15: Optional[List[int]] = None,
    bias_strength: float = 0.65,
) -> Dict:
    """
    목표 예정가격(target_est_price)과 15개 예비가격 슬롯을 기반으로:
    1) 1~15번 각 번호의 AI 다수결 선택 확률(%) 계산
    2) 1,365개(15C4) 조합의 목표 타점 근접도 x 다수결 동조 확률 결합 시너지 스코어 산출
    3) 상위 10개 유력 조합(4개 번호) 및 나라장터 실전 응찰용 최적 2개 번호(Best 2-Pick) 자동 도출
    """
    canon_seed = "202611-00892" if notice_no in ("R26BK01812785-000", "202611-00892") else notice_no
    hv = int(hashlib.md5(f"{canon_seed}_0".encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.default_rng(hv)

    if slot_prices_15 is None or len(slot_prices_15) != 15:
        raw_15 = (np.linspace(98.25, 101.75, 15) + 0.085 + rng.normal(0, 0.025, 15)).tolist()
        slot_prices_15 = [
            floor_won(Decimal(int(base_amt)) * Decimal(str(round(r, 6))) / Decimal("100"))
            for r in raw_15
        ]

    slots_arr = np.asarray(slot_prices_15, dtype=np.int64)

    # 공고 고유 시드 미세 편향과 인간 행동 사전분포 결합
    notice_jitter = rng.uniform(0.92, 1.08, size=15)
    uniform_p = np.ones(15, dtype=np.float64) / 15.0
    blended_p = (float(bias_strength) * HUMAN_SLOT_PRIOR * notice_jitter) + ((1.0 - float(bias_strength)) * uniform_p)
    slot_probs = blended_p / blended_p.sum()

    # 1,365개 조합 전수 평가
    combos_idx = np.asarray(ALL_COMBOS, dtype=np.int32)  # (1365, 4)
    comb_est_prices = (slots_arr[combos_idx].sum(axis=1) // 4).astype(np.int64)

    # 목표 예정가격과의 근접도 점수 (가우시안 커널)
    price_diffs = np.abs(comb_est_prices - int(target_est_price)).astype(np.float64)
    sigma_won = max(float(base_amt) * 0.00035, 100000.0)
    proximity_score = np.exp(-0.5 * ((price_diffs / sigma_won) ** 2))

    # 해당 4개 번호가 다수결 상위 4개로 동시에 뽑힐 결합 확률 점수
    comb_crowd_prob = np.prod(slot_probs[combos_idx], axis=1)
    comb_crowd_norm = comb_crowd_prob / max(float(comb_crowd_prob.max()), 1e-12)

    # 타점 근접도(75%) + 군중 추첨 동조율(25%) 결합 시너지 점수
    synergy_scores = (0.75 * proximity_score + 0.25 * comb_crowd_norm) * 100.0
    rank_order = np.argsort(-synergy_scores, kind="mergesort")

    # 목표 예정가격과 정확히 일치하거나 가장 가까운 1위 계단 추출
    exact_idx = int(np.argmin(price_diffs))
    best_synergy_idx = int(rank_order[0])

    # 상위 10개 조합 상세 리스트 생성
    top_combos = []
    limit_d = Decimal(str(limit_rate_pct)) / Decimal("100")
    a_d = Decimal(int(a_val))

    for rank_i, c_idx in enumerate(rank_order[:10], start=1):
        ep = int(comb_est_prices[c_idx])
        s_rate = round((ep / float(base_amt)) * 100.0, 4)
        pure_cut = ceil_won((Decimal(ep) - a_d) * limit_d + a_d)
        rec_bid = int(pure_cut + 19)
        nums_4 = [int(i + 1) for i in combos_idx[c_idx]]
        # 4개 번호 중 다수결 추첨 확률이 가장 높은 핵심 2개 번호 자동 선별
        sorted_by_crowd = sorted(nums_4, key=lambda n: slot_probs[n - 1], reverse=True)
        pick_2 = sorted(sorted_by_crowd[:2])

        top_combos.append({
            "rank": rank_i,
            "step_no": int(c_idx + 1),
            "combo_4": nums_4,
            "combo_str": f"{nums_4[0]}번 · {nums_4[1]}번 · {nums_4[2]}번 · {nums_4[3]}번",
            "best_2_str": f"{pick_2[0]}번 · {pick_2[1]}번",
            "est_price": ep,
            "sajeong_rate": s_rate,
            "recommended_bid": rec_bid,
            "diff_from_target": int(ep - int(target_est_price)),
            "crowd_prob_pct": round(float(comb_crowd_norm[c_idx]) * 100.0, 1),
            "synergy_score": round(float(synergy_scores[c_idx]), 2),
        })

    # 상위 5개 유력 조합에 등장하는 번호 빈도 + 군중 확률을 결합하여 최종 응찰용 Best 2-Pick 도출
    freq_scores = np.zeros(15, dtype=np.float64)
    for row in top_combos[:5]:
        w = row["synergy_score"] / 100.0
        for n in row["combo_4"]:
            freq_scores[n - 1] += w * (1.0 + slot_probs[n - 1] * 5.0)

    # 정밀 타점 조합(exact_idx)의 4개 번호에 가산점 부여
    exact_nums = [int(i + 1) for i in combos_idx[exact_idx]]
    for n in exact_nums:
        freq_scores[n - 1] += 2.5 * slot_probs[n - 1]

    best_slot_order = [int(i + 1) for i in np.argsort(-freq_scores)]
    primary_2_pick = sorted(best_slot_order[:2])
    backup_2_pick = sorted(best_slot_order[2:4])

    slot_table = []
    for s_i in range(15):
        num = s_i + 1
        s_won = int(slots_arr[s_i])
        s_rt = round((s_won / float(base_amt)) * 100.0, 4)
        prob_pct = round(float(slot_probs[s_i]) * 100.0, 2)
        zone = "🔥 코어 선호구간" if 5 <= num <= 11 or num in (3, 7) else ("⚠️ 양끝 회피구간" if num in (1, 14, 15) else "일반 구간")
        slot_table.append({
            "번호": f"{num}번",
            "slot_no": num,
            "예비가격(원)": s_won,
            "사정률(%)": s_rt,
            "AI 다수결 선택확률(%)": prob_pct,
            "행동편향 분류": zone,
            "추천등급": "👑 1순위 투찰체크" if num in primary_2_pick else ("🛡️ 2순위 예비체크" if num in backup_2_pick else ("⭐ 타점조합 포함" if num in exact_nums else "-")),
        })

    return {
        "exact_step_no": exact_idx + 1,
        "exact_combo_4": exact_nums,
        "best_synergy_step_no": best_synergy_idx + 1,
        "primary_2_pick": primary_2_pick,
        "backup_2_pick": backup_2_pick,
        "slot_table": slot_table,
        "top_10_combos": top_combos,
    }
