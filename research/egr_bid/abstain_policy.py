from decimal import Decimal
from typing import Dict, List, Optional
from .evidence_contract import VerifiedNotice


def evaluate_m8_abstention(
    notice: VerifiedNotice,
    m6_dist: Dict,
    m7_dist: Dict,
    max_pi80_width_pct: Decimal = Decimal("0.8000"),
    cost_input: Optional[int] = None,
) -> Dict:
    """
    M8: Contradiction & Abstention Model
    - 표본 부족, 예측구간 과대(pi80_width > max_pi80_width_pct), 비가격 점수 미달+공동도급 불허 충돌 시
      즉시 추천을 억제(HOLD_NO_RELIABLE_RECOMMENDATION)하고 상세 사유를 분리 기록 (T10, T11, T12 준수).
    """
    hold_reasons: List[str] = []
    advisory_notes: List[str] = []

    if not m6_dist.get("available", False):
        hold_reasons.append(m6_dist.get("reason", "INSUFFICIENT_M6_EVIDENCE"))
    else:
        width = m6_dist["pi80_width_pct"]
        if width > max_pi80_width_pct:
            hold_reasons.append(f"M8_EXCESSIVE_UNCERTAINTY_PI80:{width}%>{max_pi80_width_pct}%")

    if not m7_dist.get("available", False):
        advisory_notes.append("PROBABILITY_UNAVAILABLE")

    if cost_input is None or int(cost_input) <= 0:
        advisory_notes.append("COST_UNKNOWN")

    if notice.perf_score < Decimal("30.00") and not notice.joint_venture_allowed:
        hold_reasons.append("M8_DEFICIT_WITH_NO_JV_ALLOWED")

    return {
        "should_abstain": len(hold_reasons) > 0,
        "hold_reasons": hold_reasons,
        "advisory_notes": advisory_notes,
    }
