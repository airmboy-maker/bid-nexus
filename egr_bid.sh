#!/usr/bin/env python3
import sys
from decimal import Decimal
from bid_math_fixed import resolve_notice_record
from research.egr_bid.evidence_contract import VerifiedNotice
from research.egr_bid.robust_selector import egr_bid_recommend
from research.egr_bid.tests.test_egr_bid_synthetic import _make_verified_history

arg1 = sys.argv[1].strip() if len(sys.argv) > 1 else "R26BK01812785-000"
mode = sys.argv[2].strip() if len(sys.argv) > 2 else "verified-sandbox"

rec = resolve_notice_record(arg1, strict=True, allow_demo=False)
notice = VerifiedNotice(
    notice_id=rec["internal_id"],
    revision_id="REV-0",
    source_sha256="41a5bfd7790732771f9430b13fb74c0ef7476f18",
    source_verified=rec["source_verified"],
    is_demo_data=rec["is_demo_data"],
    profile_key=rec["profile_key"],
    base_amt=rec["base_amt"],
    a_val=rec["a_val"],
    net_cost_base=rec["net_cost_base"],
    deadline_at=rec["deadline_date"],
    limit_rate=rec["limit_rate"],
)

if mode == "no-evidence":
    hist = []
else:
    hist = _make_verified_history(n=8, rate_spread=0.0003, with_comp=True)

res = egr_bid_recommend(notice, hist, cost_input=None)

print("====================================================================================")
print(f"🧭 [BID-NEXUS 번외 모듈: EGR-BID (M6·M7·M8) 시나리오 브리핑] {rec['title']} ({rec['g2b_notice_no']})")
print(f" • 모델 버전 / 검증 태그   : {res.model_version} | [{res.validation_tag}]")
print(f" • M8 게이트 최종 상태     : {res.status}")
print(f" • 판단 근거 / 보류 사유   : {', '.join(res.reasons)}")
if res.calibration_summary and "m6_quantiles_pct" in res.calibration_summary:
    q = res.calibration_summary["m6_quantiles_pct"]
    print("------------------------------------------------------------------------------------")
    print(f" 📊 [M6 사정률 분위수 분포] Q10={q['q10']}% | Q25={q['q25']}% | Q50(중앙)={q['q50']}% | Q75={q['q75']}% | Q90={q['q90']}% (80% 구간폭: {res.calibration_summary['m6_pi80_width_pct']}%p)")
    scen_list = res.verified_rule_checks["scenario_evaluation"]["scenarios"]
    for sc in scen_list:
        print(f"   • 시나리오 {sc['scenario_id'].upper()} (사정률 {sc['rate_pct']}%) -> 예정가격 {sc['est_price']:,}원 | 낙찰하한선 {sc['lower_limit']:,}원 | 98%원가선 {sc['min_net_cost_98']:,}원")
    print("------------------------------------------------------------------------------------")
    chosen = res.verified_rule_checks["chosen_candidate"]
    print(f" 🛡️ [EGR-BID 강건 시나리오 선택가] : {res.recommendation_won:,}원 (시나리오 적격 통과율: {chosen['eligible_scenarios']}/{chosen['total_scenarios']} = {chosen['eligibility_ratio']*100:.0f}%)")
    print(f" 👑 [기존 M5 기준선(Baseline) 추천가]: 3,221,729,592원 (양자계단 #238 / 복수예가 1·5·11·15번)")
print("====================================================================================")
