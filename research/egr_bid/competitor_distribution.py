from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
from bid_math_fixed import lower_limit
from .evidence_contract import VerifiedNotice, HistoricalOpeningRecord


def estimate_m7_competitor_distribution(
    notice: VerifiedNotice,
    verified_history: List[HistoricalOpeningRecord],
    min_comp_samples: int = 5,
) -> Dict:
    """
    M7: Bidder-Field Competition Model
    - 실제 경쟁사 유효투찰 원시자료(top_valid_competitor_bid)가 있는 이력만 필터링하여
      낙찰하한선 대비 경쟁사 마진(웨지) 분포를 추정.
    - 경쟁사 투찰 자료가 없으면 PROBABILITY_UNAVAILABLE 반환 (T11 준수).
    """
    wedges_above_cut = []
    participant_counts = []

    for r in verified_history:
        if r.top_valid_competitor_bid is not None and r.estimated_price_final > 0:
            cut = lower_limit(r.estimated_price_final, r.a_val, r.limit_rate)
            if r.top_valid_competitor_bid >= cut:
                wedges_above_cut.append(int(r.top_valid_competitor_bid) - int(cut))
                participant_counts.append(int(r.participant_count))

    if len(wedges_above_cut) < min_comp_samples:
        return {
            "available": False,
            "reason": "PROBABILITY_UNAVAILABLE",
            "comp_sample_count": len(wedges_above_cut),
        }

    w_sorted = sorted(wedges_above_cut)
    median_wedge = w_sorted[len(w_sorted) // 2]
    avg_participants = round(sum(participant_counts) / len(participant_counts), 1)

    return {
        "available": True,
        "comp_sample_count": len(w_sorted),
        "avg_participants": avg_participants,
        "competitor_wedges_won": w_sorted,
        "median_competitor_wedge_won": median_wedge,
    }
