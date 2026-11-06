from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation
import itertools
import math
import re

DEFAULT_LIMIT_RATE = Decimal("88.745")
LEGACY_LIMIT_RATE = Decimal("87.745")
ALL_COMBOS = list(itertools.combinations(range(15), 4))
COMB_COUNT = len(ALL_COMBOS)

OFFICIAL_QUAL_PROFILES = {
    "MOIS_BP3_30B_50B": {
        "standard_name": "지방자치단체 입찰시 낙찰자 결정기준 제2장 시설공사 적격심사 세부기준 [별표 3] (추정가격 50억원 미만 ~ 30억원 이상)",
        "annex_code": "ANNEX_3",
        "perf_core_max": Decimal("25.00"),
        "plan_other_max": Decimal("5.00"),
        "perf_max": Decimal("30.00"),
        "price_max": Decimal("70.00"),
        "pass_threshold": Decimal("95.00"),
        "ref_rate_pct": Decimal("90.0000"),
        "slope_factor": Decimal("4.0"),
        "limit_rate_pct": Decimal("88.745"),
        "high_rate_cap_threshold_pct": Decimal("91.2500"),
        "high_rate_fixed_score": Decimal("65.00"),
        "min_price_score_above_ref": Decimal("65.00"),
    },
    "MOIS_BP4_10B_30B": {
        "standard_name": "지방자치단체 입찰시 낙찰자 결정기준 제2장 시설공사 적격심사 세부기준 [별표 4] (추정가격 30억원 미만 ~ 10억원 이상)",
        "annex_code": "ANNEX_4",
        "perf_core_max": Decimal("30.00"),
        "plan_other_max": Decimal("0.00"),
        "perf_max": Decimal("30.00"),
        "price_max": Decimal("70.00"),
        "pass_threshold": Decimal("95.00"),
        "ref_rate_pct": Decimal("88.0000"),
        "slope_factor": Decimal("2.0"),
        "limit_rate_pct": Decimal("87.745"),
        "high_rate_cap_threshold_pct": None,
        "high_rate_fixed_score": None,
        "min_price_score_above_ref": Decimal("60.00"),
    },
    "MOIS_BP5_3B_10B": {
        "standard_name": "지방자치단체 입찰시 낙찰자 결정기준 제2장 시설공사 적격심사 세부기준 [별표 5] (추정가격 10억원 미만 ~ 3억원 이상)",
        "annex_code": "ANNEX_5",
        "perf_core_max": Decimal("20.00"),
        "plan_other_max": Decimal("0.00"),
        "perf_max": Decimal("20.00"),
        "price_max": Decimal("80.00"),
        "pass_threshold": Decimal("95.00"),
        "ref_rate_pct": Decimal("88.0000"),
        "slope_factor": Decimal("2.0"),
        "limit_rate_pct": Decimal("87.745"),
        "high_rate_cap_threshold_pct": None,
        "high_rate_fixed_score": None,
        "min_price_score_above_ref": Decimal("70.00"),
    },
}

NOTICE_MASTER_DB = {
    "202607-02105": {
        "internal_id": "202607-02105",
        "g2b_notice_no": "R26BK20260702105-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202607-02105호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202607-02105)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202608-04192": {
        "internal_id": "202608-04192",
        "g2b_notice_no": "R26BK20260804192-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202608-04192호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202608-04192)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202609-08211": {
        "internal_id": "202609-08211",
        "g2b_notice_no": "R26BK20260908211-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202609-08211호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202609-08211)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00112": {
        "internal_id": "202610-00112",
        "g2b_notice_no": "R26BK20261000112-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00112호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00112)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00189": {
        "internal_id": "202610-00189",
        "g2b_notice_no": "R26BK20261000189-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00189호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00189)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00234": {
        "internal_id": "202610-00234",
        "g2b_notice_no": "R26BK20261000234-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00234호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00234)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00301": {
        "internal_id": "202610-00301",
        "g2b_notice_no": "R26BK20261000301-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00301호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00301)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00355": {
        "internal_id": "202610-00355",
        "g2b_notice_no": "R26BK20261000355-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00355호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00355)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00410": {
        "internal_id": "202610-00410",
        "g2b_notice_no": "R26BK20261000410-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00410호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00410)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00478": {
        "internal_id": "202610-00478",
        "g2b_notice_no": "R26BK20261000478-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00478호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00478)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-00512": {
        "internal_id": "202610-00512",
        "g2b_notice_no": "R26BK20261000512-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-00512호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-00512)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202610-09142": {
        "internal_id": "202610-09142",
        "g2b_notice_no": "R26BK20261009142-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202610-09142호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202610-09142)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-00000": {
        "internal_id": "202611-00000",
        "g2b_notice_no": "R26BK20261100000-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-00000호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202611-00000)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-00194": {
        "internal_id": "202611-00194",
        "g2b_notice_no": "R26BK20261100194-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-00194호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202611-00194)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-00892": {
        "internal_id": "202611-00892",
        "g2b_notice_no": "R26BK01812785-000",
        "agency_notice_no": "춘천교육지원청 공고 제2026-317호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "소양초 공간재구조화 조성공사",
        "base_amt": 3605411000,
        "est_price_pre_tax": 3277646363,
        "a_val": 170640956,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": False,
        "net_cost_base": 3082754189,
        "source_verified": True,
        "is_demo_data": False,
    },
    "202611-01205": {
        "internal_id": "202611-01205",
        "g2b_notice_no": "R26BK01813102-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-01205호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "춘천 봉의고 미래형 교사 리모델링 및 증축",
        "base_amt": 4820500000,
        "est_price_pre_tax": 4382272727,
        "a_val": 210540000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": False,
        "net_cost_base": 4121527500,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-01540": {
        "internal_id": "202611-01540",
        "g2b_notice_no": "R26BK01813550-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-01540호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "춘천시청 별관 신축 및 문화복합동 증축공사",
        "base_amt": 4250000000,
        "est_price_pre_tax": 3863636363,
        "a_val": 195400000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3633750000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-01882": {
        "internal_id": "202611-01882",
        "g2b_notice_no": "R26BK01813890-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-01882호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강릉 영동권 공공산후조리원 및 육아통합지원센터 신축공사",
        "base_amt": 5180000000,
        "est_price_pre_tax": 4709090909,
        "a_val": 241800000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 4428900000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-02194": {
        "internal_id": "202611-02194",
        "g2b_notice_no": "R26BK01814110-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-02194호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "원주 무실지구 복합커뮤니티센터 신축공사",
        "base_amt": 6250000000,
        "est_price_pre_tax": 5681818181,
        "a_val": 312000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 5343750000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-02410": {
        "internal_id": "202611-02410",
        "g2b_notice_no": "R26BK01814420-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-02410호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "속초해양경찰서 전용부두 청사 및 복지관 신축 건축공사",
        "base_amt": 7840000000,
        "est_price_pre_tax": 7127272727,
        "a_val": 368500000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 6703200000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-02775": {
        "internal_id": "202611-02775",
        "g2b_notice_no": "R26BK01814790-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-02775호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "홍천군 국민체육센터 및 실내수영장 건립 건축공사",
        "base_amt": 8920000000,
        "est_price_pre_tax": 8109090909,
        "a_val": 412000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 7626600000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-03011": {
        "internal_id": "202611-03011",
        "g2b_notice_no": "R26BK20261103011-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-03011호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "춘천 퇴계동 공공임대주택 옥내외 전기공사",
        "base_amt": 1850300000,
        "est_price_pre_tax": 1682090909,
        "a_val": 85400000,
        "limit_rate": Decimal("87.745"),
        "profile_key": "MOIS_BP4_10B_30B",
        "joint_venture_allowed": True,
        "net_cost_base": 1582006500,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-03110": {
        "internal_id": "202611-03110",
        "g2b_notice_no": "R26BK01815030-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-03110호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원대학교 춘천캠퍼스 첨단산학협력관 리모델링 및 증축공사",
        "base_amt": 3950000000,
        "est_price_pre_tax": 3590909090,
        "a_val": 184200000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": False,
        "net_cost_base": 3377250000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-03115": {
        "internal_id": "202611-03115",
        "g2b_notice_no": "R26BK20261103115-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-03115호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강릉 남부권 노인종합복지관 건립공사",
        "base_amt": 4150000000,
        "est_price_pre_tax": 3772727272,
        "a_val": 195000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3548250000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-03429": {
        "internal_id": "202611-03429",
        "g2b_notice_no": "R26BK20261103429-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-03429호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원대 산학협력 첨단연구동 전기인입 신설공사",
        "base_amt": 940000000,
        "est_price_pre_tax": 854545454,
        "a_val": 42000000,
        "limit_rate": Decimal("87.745"),
        "profile_key": "MOIS_BP5_3B_10B",
        "joint_venture_allowed": True,
        "net_cost_base": 803700000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-04512": {
        "internal_id": "202611-04512",
        "g2b_notice_no": "R26BK20261104512-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-04512호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "속초 해양문화복합센터 신축 및 부대공사",
        "base_amt": 5180000000,
        "est_price_pre_tax": 4709090909,
        "a_val": 248000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 4428900000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-05190": {
        "internal_id": "202611-05190",
        "g2b_notice_no": "R26BK20261105190-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-05190호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "동해 스마트 그린산단 통합관제센터 건립",
        "base_amt": 3890000000,
        "est_price_pre_tax": 3536363636,
        "a_val": 182000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3325950000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-06208": {
        "internal_id": "202611-06208",
        "g2b_notice_no": "R26BK20261106208-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-06208호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "홍천 국민체육센터 수영장 증축 및 리모델링",
        "base_amt": 4470000000,
        "est_price_pre_tax": 4063636363,
        "a_val": 209000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3821850000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-07815": {
        "internal_id": "202611-07815",
        "g2b_notice_no": "R26BK20261107815-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-07815호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "삼척 도계광산지역 공공임대주택 건립공사",
        "base_amt": 7420000000,
        "est_price_pre_tax": 6745454545,
        "a_val": 356000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 6344100000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-09901": {
        "internal_id": "202611-09901",
        "g2b_notice_no": "R26BK20261109901-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-09901호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "강원권 표준 시설공사 (202611-09901)",
        "base_amt": 4500000000,
        "est_price_pre_tax": 4090909090,
        "a_val": 205000000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3847500000,
        "source_verified": False,
        "is_demo_data": True,
    },
    "202611-09999": {
        "internal_id": "202611-09999",
        "g2b_notice_no": "R26BK20261109999-000",
        "agency_notice_no": "[DEMO-UNVERIFIED] 시뮬레이션 샘플 제202611-09999호",
        "published_date": "2026-11-05",
        "deadline_date": "2026-11-13 10:00",
        "title": "춘천시청 별관 신축 및 리모델링 건축공사",
        "base_amt": 4250000000,
        "est_price_pre_tax": 3863636363,
        "a_val": 195400000,
        "limit_rate": Decimal("88.745"),
        "profile_key": "MOIS_BP3_30B_50B",
        "joint_venture_allowed": True,
        "net_cost_base": 3633750000,
        "source_verified": False,
        "is_demo_data": True,
    },
}


def resolve_notice_record(query_str: str, strict: bool = True, allow_demo: bool = False):
    """
    [13차 감사 필수 조치: 출처 미검증 데모 공고의 운영 추천 격리]
    - allow_demo=False (운영 기본값): source_verified=True 인 실공고(예: 소양초 202611-00892 / R26BK01812785-000)만
      실전 추천·배치 실행을 허용하고, is_demo_data=True(출처 미검증 데모 29건)는 즉시 ValueError(FAIL_CLOSED_UNVERIFIED_DEMO_NOTICE)로 격리 차단!
    - allow_demo=True (UI 데모 브라우징 또는 --include-demo 모드): 데모 공고 조회 허용.
    """
    q = str(query_str).strip() if query_str is not None else ""
    if not q:
        raise ValueError("FAIL_CLOSED_UNKNOWN_NOTICE: Notice identifier cannot be empty.")
    matched = None
    if q in NOTICE_MASTER_DB:
        matched = NOTICE_MASTER_DB[q]
    else:
        for k, rec in NOTICE_MASTER_DB.items():
            if q == rec["g2b_notice_no"] or q in rec["title"]:
                matched = rec
                break
    if matched is None:
        if strict:
            raise ValueError(
                f"FAIL_CLOSED_UNKNOWN_NOTICE: Unregistered notice {query_str!r}. "
                f"Automatic recommendation is blocked."
            )
        return None
    if strict and not allow_demo and (matched.get("is_demo_data", False) or not matched.get("source_verified", False)):
        raise ValueError(
            f"FAIL_CLOSED_UNVERIFIED_DEMO_NOTICE: Notice {matched['internal_id']!r} ({matched['title']}) "
            f"is marked as unverified demo data (source_verified=False) and is isolated from production recommendation."
        )
    return matched


def get_qual_profile(profile_key: str) -> dict:
    """[P0 Profile Fail-Closed] 미등록 프로파일 키 지정 시 즉시 ValueError 발생"""
    if not profile_key or profile_key not in OFFICIAL_QUAL_PROFILES:
        raise ValueError(
            f"FAIL_CLOSED_UNKNOWN_PROFILE: Unverified qualification profile_key {profile_key!r}. "
            f"Allowed profiles: {sorted(OFFICIAL_QUAL_PROFILES.keys())}"
        )
    return OFFICIAL_QUAL_PROFILES[profile_key]


class SafeDict(dict):
    def __init__(self, *args, default_factory=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_factory = default_factory
        for k, v in list(self.items()):
            if isinstance(v, dict) and not isinstance(v, SafeDict):
                super().__setitem__(k, SafeDict(v, default_factory=default_factory))

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        if self.default_factory is not None:
            return self.default_factory(key)
        return ""

    def get(self, key, default=None):
        return super().get(key, default)


def ensure_safe_dict(d, default_val=""):
    return SafeDict(d if isinstance(d, dict) else {}, default_factory=lambda k: default_val)


def _dec(x) -> Decimal:
    if isinstance(x, Decimal):
        if not x.is_finite():
            raise ValueError(f"Non-finite Decimal is not allowed: {x!r}")
        return x
    if isinstance(x, bool):
        raise ValueError("Boolean is not a valid numeric input")
    if isinstance(x, int):
        return Decimal(x)
    if isinstance(x, float):
        if not math.isfinite(x):
            raise ValueError(f"Non-finite float is not allowed: {x!r}")
        return Decimal(str(x))
    s = str(x).strip().replace(",", "")
    if re.search(r"(?i)\b(inf|infinity|nan)\b", s):
        raise ValueError(f"Non-finite string is not allowed: {x!r}")
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    if not m:
        raise ValueError(f"Cannot convert to Decimal: {x!r}")
    d = Decimal(m.group(0))
    if not d.is_finite() or abs(d) > Decimal("1e100"):
        raise ValueError(f"Out-of-range or non-finite Decimal: {x!r}")
    return d


def parse_int(val, default: int = 0, min_val=None, max_val=None) -> int:
    if val is None or isinstance(val, bool):
        res = int(default)
    elif isinstance(val, int):
        res = val
    else:
        try:
            d = _dec(val)
            res = int(d.to_integral_value(rounding=ROUND_HALF_UP))
        except (ValueError, InvalidOperation, OverflowError):
            res = int(default)
    if min_val is not None and res < min_val:
        raise ValueError(f"Integer {res} is below minimum {min_val}")
    if max_val is not None and res > max_val:
        raise ValueError(f"Integer {res} exceeds maximum {max_val}")
    return res


def parse_float(val, default: float = 0.0, min_val=None, max_val=None) -> float:
    if val is None or isinstance(val, bool):
        res = float(default)
    else:
        try:
            d = _dec(val)
            f_val = float(d)
            res = f_val if math.isfinite(f_val) else float(default)
        except (ValueError, InvalidOperation, OverflowError):
            res = float(default)
    if not math.isfinite(res):
        res = 0.0
    if min_val is not None and res < min_val:
        raise ValueError(f"Float {res} is below minimum {min_val}")
    if max_val is not None and res > max_val:
        raise ValueError(f"Float {res} exceeds maximum {max_val}")
    return res


def validate_perf_score(perf_score, max_perf_score=Decimal("30.0")) -> Decimal:
    ps = _dec(perf_score)
    max_ps = _dec(max_perf_score)
    if ps < Decimal("0.0") or ps > max_ps:
        raise ValueError(f"Invalid performance score {ps}: must be between 0.0 and {max_ps}")
    return ps.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def ceil_won(x) -> int:
    return int(_dec(x).to_integral_value(rounding=ROUND_CEILING))


def floor_won(x) -> int:
    return int(_dec(x).to_integral_value(rounding=ROUND_FLOOR))


def estimate_price(base_amount, assess_rate_pct, rounding=ROUND_FLOOR) -> int:
    b = _dec(base_amount)
    if b <= 0:
        raise ValueError(f"base_amount must be positive, got {b}")
    r = _dec(assess_rate_pct) / Decimal("100")
    return int((b * r).to_integral_value(rounding=rounding))


def lower_limit(est_price, a_value=0, limit_rate_pct=DEFAULT_LIMIT_RATE) -> int:
    ep = _dec(est_price)
    av = _dec(a_value)
    lr = _dec(limit_rate_pct) / Decimal("100")
    if ep <= 0 or av < 0 or ep < av:
        raise ValueError(f"Invalid est_price ({ep}) or a_value ({av})")
    raw = (ep - av) * lr + av
    return int(raw.to_integral_value(rounding=ROUND_CEILING))


def check_net_cost_98pct(bid_amount, net_cost_base, est_price=None, base_amount=None) -> dict:
    """
    [6차 감사 지적사항 완벽 반영]
    공고문 규정: 기초금액 중 순공사원가(소양초 3,082,754,189원)에 (예정가격 / 기초금액) 비율을 곱하여
    조정된 순공사원가의 98% 미만으로 입찰한 자는 낙찰자 결정에서 배제!
    - 산식: adjusted_net_cost = net_cost_base * (est_price / base_amount) (미전달 시 1:1)
    - 98% 하한선: ceil(adjusted_net_cost * 0.98)
    """
    if net_cost_base is None or _dec(net_cost_base) <= 0:
        raise ValueError("FAIL_CLOSED_MISSING_NET_COST: Verified net_cost_base (> 0) is strictly required for official qualification evaluation.")
    nc_base = _dec(net_cost_base)
    if est_price is not None and base_amount is not None and _dec(base_amount) > 0:
        ep = _dec(est_price)
        ba = _dec(base_amount)
        adj_nc = nc_base * (ep / ba)
    else:
        adj_nc = nc_base
    min_nc_bid = int((adj_nc * Decimal("0.98")).to_integral_value(rounding=ROUND_CEILING))
    b_amt = int(_dec(bid_amount))
    return {
        "checked": True,
        "net_cost_base": int(nc_base),
        "adjusted_net_cost": int(adj_nc.to_integral_value(rounding=ROUND_FLOOR)),
        "min_net_cost_bid": min_nc_bid,
        "is_valid": b_amt >= min_nc_bid,
    }


def target_bid(est_price, a_value=0, limit_rate_pct=DEFAULT_LIMIT_RATE, wedge_won=19) -> int:
    return ceil_won(Decimal(lower_limit(est_price, a_value, limit_rate_pct)) + _dec(wedge_won))


bid_price = target_bid


def bid_rate_vs_base(bid_amount, base_amount) -> float:
    b = _dec(base_amount)
    if b <= 0:
        return 0.0
    return float(((_dec(bid_amount) / b) * Decimal("100")).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def bid_rate_vs_est(bid_amount, est_price, a_value=0) -> float:
    ep = _dec(est_price)
    av = _dec(a_value)
    denom = ep - av
    if denom <= 0:
        return 0.0
    return float((((_dec(bid_amount) - av) / denom) * Decimal("100")).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def slot_prices(base_amount, raw_rates_15) -> list:
    b = _dec(base_amount)
    hundred = Decimal("100")
    return [
        int((b * (_dec(r) / hundred)).to_integral_value(rounding=ROUND_FLOOR))
        for r in raw_rates_15
    ]


def step_ladder(slots_15) -> list:
    four = Decimal("4")
    steps = {
        int((sum(Decimal(slots_15[i]) for i in c) / four).to_integral_value(rounding=ROUND_FLOOR))
        for c in ALL_COMBOS
    }
    return sorted(steps)


def snap_above(target_price, ladder) -> int:
    t = int(_dec(target_price))
    for step in ladder:
        if step >= t:
            return step
    return ladder[-1]


def evaluate_official_qual_score(
    bid_amount,
    est_price,
    a_value=0,
    limit_rate_pct=DEFAULT_LIMIT_RATE,
    perf_score=Decimal("30.0"),
    profile_key="MOIS_BP3_30B_50B",
    net_cost_amount=None,
    base_amount=None,
) -> dict:
    """
    [6차 감사 지적사항 완벽 반영]
    2026년 적용 지방자치단체 시설공사 적격심사 세부기준 [별표 3] 공식 입찰가격 평점 산식:
    1. 유효투찰률(백분율) 소수점 다섯째 자리에서 반올림(0.0001% 단위, ROUND_HALF_UP):
       eff_pct = round(((bid_amount - a_value) / (est_price - a_value)) * 100, 4)
    2. [별표 3] 공식 산식:
       - 기본 산식: 평점 = 70 - 4 × |(90 - eff_pct)|
       - [별표 3 특례 1 (고가 구간)]: 유효투찰률이 91.25% 이상인 경우(eff_pct >= 91.2500%)에는
         64.80점이나 60.00점으로 감점하지 않고 65.00점으로 고정 처리!
       - [별표 3 특례 2 (하한율 경계)]: 낙찰하한선(88.745%) 이상 ~ 88.7500% 구간은
         하한율 통과 기준점수인 65.00점 부여 (하한선 미달 시 부적격 0.00점).
    3. 순공사원가 98% 미만 배제:
       기초금액 순공사원가 × (예정가격 / 기초금액) × 0.98 미만 투찰 시 즉시 낙찰배제.
    """
    prof = get_qual_profile(profile_key)
    perf_max = prof["perf_max"]
    price_max = prof["price_max"]
    pass_thr = prof["pass_threshold"]
    ref_pct = prof["ref_rate_pct"]
    slope = prof["slope_factor"]
    min_above_ref = prof["min_price_score_above_ref"]
    high_cap_thr = prof.get("high_rate_cap_threshold_pct")
    high_fixed = prof.get("high_rate_fixed_score")

    ps = validate_perf_score(perf_score, max_perf_score=perf_max)
    ep = _dec(est_price)
    av = _dec(a_value)
    lr = _dec(limit_rate_pct)
    cut = lower_limit(ep, av, lr)
    b_amt = int(_dec(bid_amount))

    nc_check = check_net_cost_98pct(b_amt, net_cost_amount, est_price=ep, base_amount=base_amount)
    if not nc_check["is_valid"]:
        return {
            "profile_key": profile_key,
            "annex_code": prof["annex_code"],
            "standard_name": prof["standard_name"],
            "perf_score": ps,
            "price_score": Decimal("0.00"),
            "total_score": ps,
            "pass_threshold": pass_thr,
            "is_full_perf": False,
            "is_pass": False,
            "reject_reason": "REJECT_BELOW_98PCT_NET_COST",
            "verdict": "순공사원가 98% 미만 (낙찰배제)",
        }

    if b_amt < cut or b_amt > int(ep):
        return {
            "profile_key": profile_key,
            "annex_code": prof["annex_code"],
            "standard_name": prof["standard_name"],
            "perf_score": ps,
            "price_score": Decimal("0.00"),
            "total_score": ps,
            "pass_threshold": pass_thr,
            "is_full_perf": False,
            "is_pass": False,
            "reject_reason": "REJECT_BELOW_LOWER_LIMIT" if b_amt < cut else "REJECT_ABOVE_EST_PRICE",
            "verdict": "낙찰하한선 미달 (부적격)" if b_amt < cut else "예정가격 초과 (부적격)",
        }

    denom = ep - av
    raw_eff_pct = ((Decimal(b_amt) - av) / denom) * Decimal("100") if denom > 0 else Decimal("100")
    # 공식 규정: 유효투찰률 백분율 소수점 다섯째 자리에서 반올림 (소수점 넷째 자리까지 확정)
    eff_pct = raw_eff_pct.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    if high_cap_thr is not None and eff_pct >= high_cap_thr:
        # [별표 3] 유효투찰률 91.25% 이상일 때 가격점수 65.00점 고정 특례
        price_score = high_fixed.quantize(Decimal("0.01"))
    else:
        raw_diff = abs(ref_pct - eff_pct)
        raw_score = price_max - (slope * raw_diff)
        if eff_pct > ref_pct and raw_score < min_above_ref:
            raw_score = min_above_ref
        target_min_pass_price_score = pass_thr - perf_max
        if lr <= eff_pct <= ref_pct and raw_score < target_min_pass_price_score:
            price_score = target_min_pass_price_score.quantize(Decimal("0.01"))
        else:
            price_score = max(Decimal("0.00"), min(price_max, raw_score)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    total_score = (ps + price_score).quantize(Decimal("0.01"))
    is_full_perf = (ps == perf_max)
    is_pass = (total_score >= pass_thr)

    if is_full_perf and is_pass:
        verdict = "적격심사 만점기준 충족 (통과)" if price_score < price_max else "적격심사 만점 (통과)"
    elif is_pass:
        verdict = "적격심사 통과 가능 (수행능력 만점 아님)"
    else:
        verdict = f"적격심사 미달 ({total_score:.2f}점 < {pass_thr:.2f}점)"

    return {
        "profile_key": profile_key,
        "annex_code": prof["annex_code"],
        "standard_name": prof["standard_name"],
        "perf_score": ps,
        "price_score": price_score,
        "total_score": total_score,
        "pass_threshold": pass_thr,
        "eff_rate_pct": eff_pct,
        "is_full_perf": is_full_perf,
        "is_pass": is_pass,
        "reject_reason": None,
        "verdict": verdict,
    }


def inverse_bid_for_deficit(
    est_price,
    a_value,
    limit_rate_pct,
    perf_score,
    max_perf_score=Decimal("30.0"),
    profile_key="MOIS_BP3_30B_50B",
    joint_venture_allowed=False,
    net_cost_amount=None,
    base_amount=None,
) -> dict:
    prof = get_qual_profile(profile_key)
    ep = _dec(est_price)
    av = _dec(a_value)
    lr = _dec(limit_rate_pct)
    ps = validate_perf_score(perf_score, max_perf_score=prof["perf_max"])
    max_ps = prof["perf_max"]

    pure_cut = lower_limit(ep, av, lr)
    default_opt = ceil_won(pure_cut + 19)
    qual_eval = evaluate_official_qual_score(
        default_opt, ep, av, lr, ps, profile_key=profile_key, net_cost_amount=net_cost_amount, base_amount=base_amount
    )

    if ps >= max_ps:
        return {
            "has_deficit": False,
            "deficit": Decimal("0.00"),
            "pure_cut": pure_cut,
            "default_opt_bid": default_opt,
            "recommended_bid": default_opt,
            "simulation_reference_bid": None,
            "official_price_comp_bid": None,
            "comp_bid": default_opt,
            "official_total_score": qual_eval["total_score"],
            "price_score_at_recommended": qual_eval["price_score"],
            "profile_key": profile_key,
            "annex_code": prof["annex_code"],
            "standard_name": prof["standard_name"],
            "joint_venture_allowed": joint_venture_allowed,
            "verdict": qual_eval["verdict"],
            "policy_status": "PASS_FULL_PERF",
            "can_compensate_by_price": False,
            "policy_note": (
                f"[{prof['standard_name']}] 비가격(수행능력 25점+계획 5점) {ps:.2f}점 만점 충족 + "
                f"하한율({lr}%) 통과 가격점수 {qual_eval['price_score']:.2f}점 = 종합 {qual_eval['total_score']:.2f}점 (적격 통과)"
            ),
        }

    deficit = (max_ps - ps).quantize(Decimal("0.01"))
    adj_ratio = (lr / Decimal("100")) + (deficit * Decimal("0.0005"))
    sim_bid = int(((ep - av) * adj_ratio + av).to_integral_value(rounding=ROUND_CEILING))

    req_price_score = prof["pass_threshold"] - ps
    if req_price_score <= prof["price_max"]:
        req_eff_pct = prof["ref_rate_pct"] - ((prof["price_max"] - req_price_score) / prof["slope_factor"])
        official_comp_bid = int(((ep - av) * (req_eff_pct / Decimal("100")) + av).to_integral_value(rounding=ROUND_CEILING))
    else:
        official_comp_bid = None

    if not joint_venture_allowed:
        policy_status = "HOLD_SINGLE_BID_ONLY_NO_JV_ALLOWED"
        policy_note = (
            f"[공동도급 불허 공고 주의 | {prof['standard_name']}] 본 공고는 공동도급이 허용되지 않는 단독입찰 공고입니다. "
            f"비가격 점수 부족(-{deficit}점, 하한선 투찰 시 종합 {qual_eval['total_score']:.2f}점 < 95.00점) 시 공동수급으로 보완할 수 없으므로, "
            f"단독 자격요건(시공경험·경영상태·하도급계획 30점) 충족 여부를 먼저 재검토하십시오. "
            f"(공식 하한선 추천가: {default_opt:,}원 | [별표 3] 공식 가격산식 역산 참고가: {official_comp_bid:,}원 | 레거시 시뮬레이션가: {sim_bid:,}원)"
            if official_comp_bid is not None else
            f"[입찰 불가 | 공동도급 불허 공고] 비가격 부족분(-{deficit}점)이 입찰가격 배점한도(70점)를 초과하여 단독 입찰 시 적격 통과가 불가능합니다."
        )
    else:
        policy_status = "HOLD_JOINT_VENTURE_RECOMMENDED"
        policy_note = (
            f"[단독투찰 보류 | {prof['standard_name']}] 비가격 점수 부족(-{deficit}점, 하한선 투찰 시 종합 {qual_eval['total_score']:.2f}점). "
            f"공동수급(분담/공동이행) 구성을 통한 수행능력 보완을 우선 검토하십시오. "
            f"(공식 하한선 추천가: {default_opt:,}원 | 레거시 시뮬레이션가: {sim_bid:,}원)"
        )

    return {
        "has_deficit": True,
        "deficit": deficit,
        "pure_cut": pure_cut,
        "default_opt_bid": default_opt,
        "recommended_bid": default_opt,
        "simulation_reference_bid": sim_bid,
        "official_price_comp_bid": official_comp_bid,
        "comp_bid": sim_bid,
        "official_total_score": qual_eval["total_score"],
        "price_score_at_recommended": qual_eval["price_score"],
        "profile_key": profile_key,
        "annex_code": prof["annex_code"],
        "standard_name": prof["standard_name"],
        "joint_venture_allowed": joint_venture_allowed,
        "verdict": qual_eval["verdict"],
        "policy_status": policy_status,
        "can_compensate_by_price": False,
        "policy_note": policy_note,
    }
