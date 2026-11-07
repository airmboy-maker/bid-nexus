from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from itertools import combinations
import numpy as np

# 1,365 조합 상수 (1회만 생성)
ALL_COMBOS = tuple(combinations(range(15), 4))
COMBS_ARRAY = np.asarray(ALL_COMBOS, dtype=np.int32)

DEFAULT_RHO_FALLBACK = 0.30
RHO_SENSITIVITY_BOUNDS = (0.15, 0.60)
MIN_EVT_SAMPLES = 20

F8_HONEST_WARNING = (
    "본 시스템은 확률적 추정 도구입니다. 예정가격은 추첨으로 결정되므로 투찰 전 확정될 수 없습니다. "
    "제시된 확률은 과거 개찰 이력에 기반한 추정치이며, 실제 결과를 보장하지 않습니다."
)


def ceil_won(val) -> int:
    """원단위 절상 (은행가 반올림 round() 금지)"""
    return int(Decimal(str(val)).to_integral_value(rounding=ROUND_CEILING))


def floor_won(val) -> int:
    """원단위 절사"""
    return int(Decimal(str(val)).to_integral_value(rounding=ROUND_FLOOR))
