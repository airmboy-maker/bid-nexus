from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
from .evidence_contract import VerifiedNotice, HistoricalOpeningRecord


def estimate_m6_rate_distribution(
    notice: VerifiedNotice,
    verified_history: List[HistoricalOpeningRecord],
    min_samples: int = 5,
) -> Dict:
    """
    M6: Source-Aware Hierarchical Rate Model
    - 발주기관(agency_id) 표본과 전체 지역/공종 표본을 계층 수축(Partial Pooling)하여
      예정가격 사정률 R(%)의 분위수(q10, q25, q50, q75, q90)와 80% 예측구간 폭(pi80_width) 산출.
    """
    if len(verified_history) < min_samples:
        return {
            "available": False,
            "reason": f"INSUFFICIENT_M6_SAMPLES:{len(verified_history)}<{min_samples}",
            "sample_count": len(verified_history),
        }

    global_rates = []
    agency_rates = []
    for r in verified_history:
        if r.base_amt > 0 and r.estimated_price_final > 0:
            rate_pct = (Decimal(r.estimated_price_final) / Decimal(r.base_amt)) * Decimal("100")
            global_rates.append(rate_pct)
            if r.agency_id == notice.agency_id:
                agency_rates.append(rate_pct)

    if len(global_rates) < min_samples:
        return {"available": False, "reason": "INSUFFICIENT_VALID_RATES", "sample_count": len(global_rates)}

    global_sorted = sorted(global_rates)
    n_g = len(global_sorted)

    def _quantile(arr, q_float):
        idx = min(len(arr) - 1, max(0, int(round((len(arr) - 1) * q_float))))
        return arr[idx].quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    g_q10, g_q25, g_q50, g_q75, g_q90 = [
        _quantile(global_sorted, q) for q in (0.10, 0.25, 0.50, 0.75, 0.90)
    ]

    # 계층 수축 가중치 w = n_agency / (n_agency + k), k = 5
    n_a = len(agency_rates)
    shrink_w = Decimal(n_a) / Decimal(n_a + 5)
    if n_a > 0:
        agency_sorted = sorted(agency_rates)
        a_q10, a_q25, a_q50, a_q75, a_q90 = [
            _quantile(agency_sorted, q) for q in (0.10, 0.25, 0.50, 0.75, 0.90)
        ]
    else:
        a_q10, a_q25, a_q50, a_q75, a_q90 = g_q10, g_q25, g_q50, g_q75, g_q90

    q10 = (shrink_w * a_q10 + (Decimal("1") - shrink_w) * g_q10).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    q25 = (shrink_w * a_q25 + (Decimal("1") - shrink_w) * g_q25).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    q50 = (shrink_w * a_q50 + (Decimal("1") - shrink_w) * g_q50).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    q75 = (shrink_w * a_q75 + (Decimal("1") - shrink_w) * g_q75).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    q90 = (shrink_w * a_q90 + (Decimal("1") - shrink_w) * g_q90).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    pi80_width = (q90 - q10).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    return {
        "available": True,
        "sample_count": n_g,
        "agency_sample_count": n_a,
        "shrinkage_weight": float(shrink_w.quantize(Decimal("0.01"))),
        "quantiles_pct": {"q10": q10, "q25": q25, "q50": q50, "q75": q75, "q90": q90},
        "pi80_width_pct": pi80_width,
    }
