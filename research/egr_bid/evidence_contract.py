from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List, Dict

ALLOWED_PROVENANCE = ("OFFICIAL_VERIFIED", "SECONDARY_VERIFIED", "DEMO_SYNTHETIC", "UNKNOWN")


@dataclass(frozen=True)
class VerifiedNotice:
    notice_id: str
    revision_id: str
    source_sha256: str
    source_verified: bool
    is_demo_data: bool
    profile_key: str
    base_amt: int
    a_val: int
    net_cost_base: int
    deadline_at: str
    limit_rate: Decimal = Decimal("88.745")
    perf_score: Decimal = Decimal("30.00")
    joint_venture_allowed: bool = False
    agency_id: str = "CHUNCHEON_EDU"
    work_category: str = "ARCH"
    region: str = "GANGWON"
    provenance_class: str = "OFFICIAL_VERIFIED"


@dataclass(frozen=True)
class HistoricalOpeningRecord:
    notice_id: str
    revision_id: str
    source_sha256: str
    source_verified: bool
    observed_at: str
    published_at: str
    deadline_at: str
    opening_at: str
    asof_feature_timestamp: str
    agency_id: str
    work_category: str
    region: str
    base_amt: int
    a_val: int
    limit_rate: Decimal
    profile_key: str
    net_cost_base: int
    estimated_price_final: int
    participant_count: int
    top_valid_competitor_bid: Optional[int]
    provenance_class: str = "OFFICIAL_VERIFIED"


@dataclass(frozen=True)
class RecommendationResult:
    status: str  # PASS_ADVISORY | HOLD_NO_RELIABLE_RECOMMENDATION | FAIL_CLOSED
    recommendation_won: Optional[int]
    verified_rule_checks: Dict
    calibration_summary: Optional[Dict]
    evidence_ids: List[str]
    reasons: List[str]
    model_version: str = "EGR-BID-REV01-SANDBOX"
    data_cutoff_at: str = ""
    validation_tag: str = "NOT_PRODUCTION_VALIDATED"


def verify_notice_evidence(notice: VerifiedNotice, latest_revision_map: Optional[Dict[str, str]] = None) -> List[str]:
    """T01, T02, T03, T04: 공고 원문 해시, 데모 격리, 정정공고 충돌, 순공사원가 검증"""
    errors = []
    if not notice or not notice.notice_id or not str(notice.notice_id).strip():
        errors.append("FAIL_CLOSED_EMPTY_NOTICE")
        return errors
    if notice.is_demo_data or not notice.source_verified:
        errors.append("FAIL_CLOSED_UNVERIFIED_OR_DEMO_NOTICE")
    if notice.provenance_class not in ("OFFICIAL_VERIFIED", "SECONDARY_VERIFIED"):
        errors.append(f"FAIL_CLOSED_UNTRUSTED_PROVENANCE:{notice.provenance_class}")
    if not notice.source_sha256 or len(str(notice.source_sha256).strip()) < 16:
        errors.append("FAIL_CLOSED_MISSING_SOURCE_HASH")
    if not notice.net_cost_base or int(notice.net_cost_base) <= 0:
        errors.append("FAIL_CLOSED_MISSING_NET_COST")
    if int(notice.base_amt) <= 0 or int(notice.a_val) < 0 or int(notice.a_val) >= int(notice.base_amt):
        errors.append("FAIL_CLOSED_INVALID_AMOUNTS")
    if latest_revision_map and notice.notice_id in latest_revision_map:
        expected_rev = latest_revision_map[notice.notice_id]
        if notice.revision_id != expected_rev:
            errors.append(f"FAIL_CLOSED_REVISION_CONFLICT:expected={expected_rev},got={notice.revision_id}")
    return errors


def filter_and_validate_history(
    records: List[HistoricalOpeningRecord],
    cutoff_timestamp: str,
) -> tuple:
    """T05, T06: 시점 누수(asof_feature_timestamp < opening_at <= cutoff) 및 출처 등급 검사"""
    valid_records = []
    leakage_errors = []
    synthetic_only = True

    for r in records:
        if r.asof_feature_timestamp >= r.opening_at:
            leakage_errors.append(f"TEMPORAL_LEAKAGE_ASOF_GE_OPENING:{r.notice_id}")
        if r.observed_at > cutoff_timestamp or r.opening_at > cutoff_timestamp:
            leakage_errors.append(f"TEMPORAL_LEAKAGE_FUTURE_RECORD:{r.notice_id}")
        if r.provenance_class == "OFFICIAL_VERIFIED" and r.source_verified and len(str(r.source_sha256).strip()) >= 16:
            synthetic_only = False
            valid_records.append(r)

    return valid_records, leakage_errors, synthetic_only
