# -*- coding: utf-8 -*-
"""
BID-NEXUS v20.0 코어 산식 교정 모듈 (Genspark Audit Verified Drop-in)
"""
from __future__ import annotations
import decimal
import random
from itertools import combinations
from math import comb
from typing import Iterable, Sequence

C = decimal.Context(prec=40)
DEFAULT_LIMIT_RATE = 87.745

def _dec(x: float) -> decimal.Decimal:
    return decimal.Decimal(repr(float(x)))

def ceil_won(x: float) -> int:
    """원단위 미만 절상(올림)."""
    return int(_dec(x).to_integral_value(rounding=decimal.ROUND_CEILING))

def floor_won(x: float) -> int:
    """원단위 미만 절사(버림)."""
    return int(_dec(x).to_integral_value(rounding=decimal.ROUND_FLOOR))

def estimate_price(base_amt: int | float, rate_pct: float) -> int:
    """예정가격 = 기초금액 x 사정률, 원단위 절상."""
    if base_amt is None or float(base_amt) <= 0:
        return 0
    return ceil_won(float(base_amt) * float(rate_pct) / 100.0)

def lower_limit(est_price: int | float, a_val: int | float, limit_pct: float = DEFAULT_LIMIT_RATE) -> int:
    """낙찰하한선 = (예정가격 - A값) x 하한율 + A값, 원단위 절상."""
    if est_price is None or float(est_price) <= 0:
        return 0
    return ceil_won((int(est_price) - int(a_val)) * float(limit_pct) / 100.0 + int(a_val))

def bid_price(base_amt: int | float, rate_pct: float, a_val: int | float, limit_pct: float = DEFAULT_LIMIT_RATE) -> int:
    """사정률 -> 예정가격 -> 낙찰하한선 (1원 단위 절상 정밀 타격)."""
    return lower_limit(estimate_price(base_amt, rate_pct), a_val, limit_pct)

ALL_COMBOS: tuple[tuple[int, int, int, int], ...] = tuple(combinations(range(15), 4))
assert len(ALL_COMBOS) == comb(15, 4) == 1365

def slot_prices(base_amt: int | float, slot_rates_pct: Sequence[float]) -> list[int]:
    """15개 예비가격(원). 각 슬롯은 원단위 절사."""
    if len(slot_rates_pct) != 15:
        raise ValueError("예비가격 슬롯은 정확히 15개여야 합니다")
    return [floor_won(float(base_amt) * float(r) / 100.0) for r in slot_rates_pct]

def step_ladder(slots_won: Sequence[int]) -> list[int]:
    """1,365개 조합의 산술평균(원단위 절사) = 예정가격 계단."""
    if len(slots_won) != 15:
        raise ValueError("슬롯은 15개여야 합니다")
    prices = {floor_won(sum(slots_won[i] for i in c) / 4.0) for c in ALL_COMBOS}
    return sorted(prices)

def snap_above(target: int, ladder: Iterable[int]) -> int:
    """target 이상인 계단 중 최솟값(하한선 직상단 1원 타격)."""
    for p in ladder:
        if p >= target:
            return p
    raise ValueError("목표가보다 높은 계단이 없습니다")

if __name__ == "__main__":
    B, A, L = 3_605_411_000, 170_640_956, DEFAULT_LIMIT_RATE
    est = estimate_price(B, 100.045)
    lim = lower_limit(est, A, L)
    assert lim == 3_185_903_537, f"Expected 3185903537, got {lim}"
    print(f"✅ [bid_math_fixed 자체 테스트 PASS] 예정가격={est:,}원 | 낙찰하한선(87.745%)={lim:,}원")
