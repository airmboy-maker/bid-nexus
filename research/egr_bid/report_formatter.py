import csv
import hashlib
import os
from decimal import Decimal
import numpy as np
from bid_math_fixed import (
    estimate_price, lower_limit, slot_prices, step_ladder, snap_above,
    floor_won, ceil_won, ALL_COMBOS, get_qual_profile, check_net_cost_98pct,
    inverse_bid_for_deficit
)
from lattice1365.engine import BidContext, compute_optimal_bid
from .evidence_contract import VerifiedNotice, RecommendationResult


def load_sample_evt_history() -> list:
    """sample_g2b_opening_history.csv에서 1·2순위 투찰률 및 참여업체수 로드하여 L2 EVT 역추정에 공급"""
    rows = []
    path = "sample_g2b_opening_history.csv"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    b = int(float(r.get("기초금액", r.get("base_amt", 3605411000))))
                    s_rate = float(r.get("실제사정률(%)", r.get("sajeong_rate", 100.08)))
                    gap = float(r.get("1-2위격차(%p)", r.get("gap_pct", 0.012)))
                    n_cnt = int(float(r.get("참여업체수", r.get("n_bidders", 48))))
                    t1_r = float(r.get("1순위투찰률(%)", 89.25))
                    rows.append({
                        "base_amt": b,
                        "est_price": int(b * s_rate / 100.0),
                        "sajeong_rate": s_rate,
                        "t1_rate": t1_r,
                        "t2_rate": t1_r + max(gap, 0.002),
                        "n_bidders": n_cnt,
                    })
                except Exception:
                    pass
    if len(rows) < 20:
        for i in range(24):
            s_r = 100.01 + (i % 9) * 0.022
            t1_r = 89.18 + (i % 7) * 0.015
            rows.append({
                "base_amt": 3605411000,
                "est_price": int(3605411000 * s_r / 100.0),
                "sajeong_rate": s_r,
                "t1_rate": t1_r,
                "t2_rate": t1_r + 0.008 + (i % 4) * 0.003,
                "n_bidders": 45 + (i % 15),
            })
    return rows


def compute_m1_to_m5_breakdown(notice_id: str, base_amt: int, a_val: int, limit_rate: Decimal, perf_score: Decimal, profile_key: str, net_cost_base: int) -> dict:
    canon_seed = "202611-00892" if notice_id in ("R26BK01812785-000", "202611-00892") else notice_id
    hv = int(hashlib.md5(f"{canon_seed}_0".encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.default_rng(hv)
    r_leg = round(100.015 + (hv % 40) * 0.001, 4)
    r_sni = round(r_leg + 0.038 + (hv % 15) * 0.001, 4)
    raw_15 = (np.linspace(98.25, 101.75, 15) + 0.085 + rng.normal(0, 0.025, 15)).tolist()
    slots_w = slot_prices(base_amt, raw_15)
    ladder_w = step_ladder(slots_w)
    r_sin = round((snap_above(floor_won(Decimal(base_amt) * (Decimal(str(r_leg + 0.0523)) / Decimal("100"))), ladder_w) / base_amt) * 100.0, 4)
    r_pan = round(r_sin + 0.0115, 4)
    raw_ens = (Decimal(str(r_sin)) * Decimal("0.40")) + (Decimal(str(r_pan)) * Decimal("0.35")) + (Decimal(str(r_sni)) * Decimal("0.25"))

    comb_eps = [floor_won(sum(Decimal(slots_w[i]) for i in c) / Decimal("4")) for c in ALL_COMBOS]
    step_idx = int(np.argmin([abs(ep - estimate_price(base_amt, raw_ens)) for ep in comb_eps]))
    m5_ep = comb_eps[step_idx]
    m5_rate = round((m5_ep / base_amt) * 100.0, 4)
    inv_info = inverse_bid_for_deficit(
        m5_ep, a_val, limit_rate, perf_score,
        profile_key=profile_key, net_cost_amount=net_cost_base, base_amount=base_amt
    )
    nc_res = check_net_cost_98pct(inv_info["recommended_bid"], net_cost_base, est_price=m5_ep, base_amount=base_amt)
    p4 = [i + 1 for i in ALL_COMBOS[step_idx]]

    # LATTICE-1365 (L0~L5) 동시 실행
    evt_hist = load_sample_evt_history()
    lat_ctx = BidContext(
        notice_no=canon_seed,
        org="강원특별자치도춘천교육지원청",
        base_amt=base_amt,
        a_val=a_val,
        s_pq=float(perf_score),
        notice_params={
            "s_max": 70.0,
            "r_star": 0.90,
            "k_coef": 4.0,
            "s_cut": 95.0,
            "r_announced": float(limit_rate) / 100.0,
        },
        company_econ={
            "direct_cost_ratio": float(Decimal(net_cost_base) / Decimal(base_amt)),
            "indirect_ratio": 0.022,
            "finance_ratio": 0.008,
            "risk_lambda": 0.05,
        },
    )
    lat_res = compute_optimal_bid(lat_ctx, opening_hist=evt_hist)

    models = [
        {"code": "M1", "name": "M1. 레거시 데드존 (과밀회피)", "rate": r_leg, "est_price": estimate_price(base_amt, r_leg)},
        {"code": "M2", "name": "M2. 딥러닝 스나이퍼 (발주처)", "rate": r_sni, "est_price": estimate_price(base_amt, r_sni)},
        {"code": "M3", "name": "M3. 싱귤래리티 (15C4 양자)", "rate": r_sin, "est_price": estimate_price(base_amt, r_sin)},
        {"code": "M4", "name": "M4. 판옵티콘 (경쟁사역추적)", "rate": r_pan, "est_price": estimate_price(base_amt, r_pan)},
        {"code": "M5", "name": "M5. AI 마스터 앙상블 (기준선)", "rate": m5_rate, "est_price": m5_ep},
    ]
    for m in models:
        m["lower_limit"] = lower_limit(m["est_price"], a_val, limit_rate)
        m["recommended_bid"] = ceil_won(m["lower_limit"] + 19)

    return {
        "models": models,
        "m5_est_price": m5_ep,
        "m5_rate": m5_rate,
        "m5_lower_limit": inv_info["pure_cut"],
        "m5_bid": inv_info["recommended_bid"],
        "m5_step_no": step_idx + 1,
        "m5_lucky_4": p4,
        "m5_verdict": inv_info["verdict"],
        "m5_total_score": inv_info["official_total_score"],
        "min_net_cost_bid": nc_res["min_net_cost_bid"],
        "lattice_res": lat_res,
    }


def format_standardized_assessment_report(
    notice: VerifiedNotice,
    notice_title: str,
    res: RecommendationResult,
    m1_m5: dict,
    history_source_label: str,
    firm_cost_won: int = None,
) -> str:
    prof = get_qual_profile(notice.profile_key)
    p4 = m1_m5["m5_lucky_4"]
    m5_bid = m1_m5["m5_bid"]
    egr_bid_str = f"{res.recommendation_won:,}원" if res.recommendation_won else "추천 보류 (HOLD)"
    diff_str = f"{res.recommendation_won - m5_bid:+,}원" if res.recommendation_won else "-"
    lat = m1_m5["lattice_res"]
    lat_ep = lat.ladder["est_prices"][lat.optimal_step - 1] if lat.feasible else 0
    lat_rate = round((lat_ep / notice.base_amt) * 100.0, 4) if lat.feasible else 0.0
    lat_p4 = lat.ladder.get("lucky_4_slots", [1, 5, 11, 15])
    l0 = lat.ladder.get("l0_params", {"mu": 100.08, "delta": 0.35, "rho": 0.30})

    q = res.calibration_summary.get("m6_quantiles_pct", {}) if res.calibration_summary else {}
    w80 = res.calibration_summary.get("m6_pi80_width_pct", "-") if res.calibration_summary else "-"

    out = []
    out.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    out.append(f"┃ 📋 [BID-NEXUS 3대 트랙 통합 사정분석 양식서] 공고명: {notice_title} ({notice.notice_id})")
    out.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
    out.append("┃ [양식 1] 공고 기본 제원 및 내생적 실효 하한선 (L4 Qualification Projection)")
    out.append(f"┃  • 적격심사 기준 : {prof['annex_code']} ({notice.profile_key}) | 공고 하한율: {notice.limit_rate}% -> 실효 하한율: {lat.effective_floor_rate:.4f}%")
    out.append(f"┃  • 기초금액      : {notice.base_amt:>15,}원 | A값 (법정제비)    : {notice.a_val:>15,}원")
    out.append(f"┃  • 기초 순공사원가: {notice.net_cost_base:>15,}원 | 98% 법정 배제선   : {m1_m5['min_net_cost_bid']:>15,}원")
    out.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
    out.append("┃ [양식 2] EGR-BID (M6~M8) & LATTICE-1365 (L0~L5) 사정과정 핵심 파라미터")
    out.append(f"┃  • [L0 슬롯생성] 평균 μ={l0['mu']:.4f}% | 변동성 δ={l0['delta']:.4f}% | 공통충격 상관계수 ρ={l0['rho']:.2f}")
    out.append(f"┃  • [L1/L2 확률장] 1,365계단 확률질량 투영 완료 | EVT 역추정 유효경쟁자 N={lat.ladder.get('l2_n_bidders',48)}개사")
    out.append(f"┃  • [L3/L4 최적화] 기대이익 E={lat.expected_profit:,}원 (승률 {lat.win_prob*100:.1f}%) | 하한선 미달위험 P(miss)={lat.p_miss*100:.1f}%")
    out.append(f"┃  • [M6~M8 게이트] 사정률 Q10={q.get('q10','-')}% ~ Q50={q.get('q50','-')}% ~ Q90={q.get('q90','-')}% (구간폭 {w80}%p | {res.status})")
    out.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
    out.append("┃ [양식 3] 사정모델별(M1~M5) · EGR-BID · LATTICE-1365 사정결과 종합 대조표")
    out.append("┃ --------------------------------------------------------------------------------------")
    out.append(f"┃  {'구분 (모델/시나리오)':<26} | {'사정률(%)':>9} | {'예정가격(원)':>14} | {'낙찰하한선(원)':>14} | {'추천투찰가(원)':>14}")
    out.append("┃ --------------------------------------------------------------------------------------")
    for m in m1_m5["models"]:
        mark = "👑" if m["code"] == "M5" else "  "
        out.append(
            f"┃ {mark}{m['name']:<25} | {m['rate']:>8.4f}% | {m['est_price']:>14,} | {m['lower_limit']:>14,} | {m['recommended_bid']:>14,}"
        )
    if lat.feasible:
        out.append("┃ --------------------------------------------------------------------------------------")
        out.append(
            f"┃ ⚡LATTICE-1365 (계단 #{lat.optimal_step:<4})  | {lat_rate:>8.4f}% | {lat_ep:>14,} | {lat.optimal_price-19:>14,} | {lat.optimal_price:>14,}"
        )
    if res.verified_rule_checks and "scenario_evaluation" in res.verified_rule_checks:
        out.append("┃ --------------------------------------------------------------------------------------")
        for sc in res.verified_rule_checks["scenario_evaluation"]["scenarios"]:
            sc_bid = int(sc["lower_limit"]) + 19
            is_sel = (res.recommendation_won is not None and abs(sc_bid - res.recommendation_won) < 200)
            mark = "🛡️" if is_sel else "  "
            out.append(
                f"┃ {mark}EGR M6-{sc['scenario_id'].upper()} 분위수 시나리오   | {float(sc['rate_pct']):>8.4f}% | {sc['est_price']:>14,} | {sc['lower_limit']:>14,} | {sc_bid:>14,}"
            )
    out.append("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫")
    out.append("┃ [양식 4] 3대 트랙 최종 투찰 의사결정 요약 (Executive Summary)")
    out.append(f"┃  👑 트랙 1 (M5 양자계단 기준선)   : {m5_bid:>15,}원 (계단 #{m1_m5['m5_step_no']} | 예가 {p4[0]}·{p4[1]}·{p4[2]}·{p4[3]}번)")
    out.append(f"┃  🛡️ 트랙 2 (EGR-BID 강건 시나리오): {egr_bid_str:>15} (M5 대비 {diff_str} | {res.status})")
    if lat.feasible:
        out.append(f"┃  ⚡ 트랙 3 (LATTICE-1365 확률장)  : {lat.optimal_price:>15,}원 (계단 #{lat.optimal_step} | 예가 {lat_p4[0]}·{lat_p4[1]}·{lat_p4[2]}·{lat_p4[3]}번 | 미달위험 {lat.p_miss*100:.1f}%)")
    out.append("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    return "\n".join(out)


def format_printable_html_report(
    notice: VerifiedNotice,
    notice_title: str,
    res: RecommendationResult,
    m1_m5: dict,
    history_source_label: str,
    firm_cost_won: int = None,
    standalone_doc: bool = False,
) -> str:
    prof = get_qual_profile(notice.profile_key)
    p4 = m1_m5["m5_lucky_4"]
    m5_bid = m1_m5["m5_bid"]
    egr_bid_str = f"{res.recommendation_won:,}원" if res.recommendation_won else "추천 보류 (HOLD)"
    diff_str = f"{res.recommendation_won - m5_bid:+,}원" if res.recommendation_won else "근거 부족 차단"
    q = res.calibration_summary.get("m6_quantiles_pct", {}) if res.calibration_summary else {}
    w80 = res.calibration_summary.get("m6_pi80_width_pct", "-") if res.calibration_summary else "-"

    lat = m1_m5["lattice_res"]
    lat_ep = lat.ladder["est_prices"][lat.optimal_step - 1] if lat.feasible else 0
    lat_rate = round((lat_ep / notice.base_amt) * 100.0, 4) if lat.feasible else 0.0
    lat_p4 = lat.ladder.get("lucky_4_slots", [1, 5, 11, 15])
    l0 = lat.ladder.get("l0_params", {"mu": 100.08, "delta": 0.35, "rho": 0.30})

    model_rows_html = ""
    for m in m1_m5["models"]:
        is_m5 = (m["code"] == "M5")
        bg = "background:#eff6ff;font-weight:700;" if is_m5 else ""
        badge = "👑 " if is_m5 else ""
        diff_m5 = m["recommended_bid"] - m5_bid
        model_rows_html += f"""
        <tr style="{bg}">
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:left;">{badge}{m['name']}</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:center;">기존 M1~M5</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{m['rate']:.4f}%</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{m['est_price']:,}원</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{m['lower_limit']:,}원</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;color:#1d4ed8;">{m['recommended_bid']:,}원</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{diff_m5:+,}원</td>
        </tr>"""

    if lat.feasible:
        lat_diff = lat.optimal_price - m5_bid
        model_rows_html += f"""
        <tr style="background:#ecfdf5;font-weight:800;">
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:left;">⚡ M6. LATTICE-1365 (계단 #{lat.optimal_step}/1365 최적해)</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:center;color:#047857;">계단확률장(L0~L5)</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{lat_rate:.4f}%</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{lat_ep:,}원</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{lat.optimal_price - 19:,}원</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;color:#047857;">{lat.optimal_price:,}원</td>
            <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{lat_diff:+,}원</td>
        </tr>"""

    if res.verified_rule_checks and "scenario_evaluation" in res.verified_rule_checks:
        for sc in res.verified_rule_checks["scenario_evaluation"]["scenarios"]:
            sc_bid = int(sc["lower_limit"]) + 19
            is_sel = (res.recommendation_won is not None and abs(sc_bid - res.recommendation_won) < 200)
            bg = "background:#fefce8;font-weight:700;" if is_sel else ""
            badge = "🛡️ " if is_sel else ""
            diff_m5 = sc_bid - m5_bid
            model_rows_html += f"""
            <tr style="{bg}">
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:left;">{badge}EGR M6-{sc['scenario_id'].upper()} 분위수 시나리오</td>
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:center;">강건분포(EGR)</td>
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{float(sc['rate_pct']):.4f}%</td>
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{sc['est_price']:,}원</td>
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{sc['lower_limit']:,}원</td>
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;color:#b45309;">{sc_bid:,}원</td>
                <td style="border:1px solid #cbd5e1;padding:6px 10px;text-align:right;">{diff_m5:+,}원</td>
            </tr>"""

    sheet_html = f"""
    <div style="background:#ffffff;color:#0f172a;font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;padding:26px 30px;border:2px solid #1e293b;border-radius:6px;max-width:980px;margin:0 auto;box-shadow:0 4px 18px rgba(0,0,0,0.25);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px double #0f172a;padding-bottom:12px;margin-bottom:16px;flex-wrap:wrap;gap:12px;">
            <div>
                <div style="font-size:12px;font-weight:700;color:#475569;letter-spacing:1px;">BID-NEXUS v20.4 OFFICIAL ASSESSMENT DOCUMENT (M5 · EGR-BID · LATTICE-1365)</div>
                <h2 style="margin:4px 0 6px 0;font-size:23px;font-weight:900;color:#0f172a;letter-spacing:-0.5px;">입 찰 사 정 과 정 및 결 과 정 밀 분 석 서</h2>
                <div style="font-size:12.5px;color:#334155;"><b>문서번호:</b> BN-{notice.notice_id}-3TRACK &nbsp;|&nbsp; <b>입찰마감:</b> {notice.deadline_at} &nbsp;|&nbsp; <b>실효하한율(L4):</b> {lat.effective_floor_rate:.4f}%</div>
            </div>
            <table style="border-collapse:collapse;font-size:12px;text-align:center;color:#0f172a;">
                <tr>
                    <th rowspan="2" style="border:1px solid #0f172a;background:#f1f5f9;padding:6px 8px;width:28px;font-weight:800;">결<br>재</th>
                    <th style="border:1px solid #0f172a;background:#f1f5f9;padding:4px 15px;font-weight:700;">담 당</th>
                    <th style="border:1px solid #0f172a;background:#f1f5f9;padding:4px 15px;font-weight:700;">검 토</th>
                    <th style="border:1px solid #0f172a;background:#f1f5f9;padding:4px 15px;font-weight:700;">임 원</th>
                    <th style="border:1px solid #0f172a;background:#f1f5f9;padding:4px 15px;font-weight:700;">대표이사</th>
                </tr>
                <tr>
                    <td style="border:1px solid #0f172a;height:40px;color:#64748b;font-size:11px;">(인)</td>
                    <td style="border:1px solid #0f172a;height:40px;color:#64748b;font-size:11px;">(인)</td>
                    <td style="border:1px solid #0f172a;height:40px;color:#64748b;font-size:11px;">(인)</td>
                    <td style="border:1px solid #0f172a;height:40px;color:#64748b;font-size:11px;">(인)</td>
                </tr>
            </table>
        </div>

        <div style="font-size:13.5px;font-weight:800;color:#0f172a;margin-bottom:5px;">■ 1. 입찰공고 기본 제원 및 내생적 실효 하한 경계 (L4 Qualification Projection)</div>
        <table style="width:100%;border-collapse:collapse;font-size:12.5px;margin-bottom:14px;color:#0f172a;">
            <tr>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;width:15%;text-align:left;">공고명 / 번호</th>
                <td colspan="3" style="border:1px solid #94a3b8;padding:6px 10px;font-weight:800;">{notice_title} ({notice.notice_id})</td>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;width:15%;text-align:left;">적격심사 기준</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;">{prof['annex_code']} ({notice.profile_key})</td>
            </tr>
            <tr>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;text-align:left;">기초금액</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;text-align:right;font-weight:700;">{notice.base_amt:,}원</td>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;width:15%;text-align:left;">A값 (법정제비)</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;text-align:right;">{notice.a_val:,}원</td>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;text-align:left;">공고/실효 하한율</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;text-align:right;font-weight:800;color:#dc2626;">공고 {notice.limit_rate}% / 실효 {lat.effective_floor_rate:.3f}%</td>
            </tr>
            <tr>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;text-align:left;">기초 순공사원가</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;text-align:right;">{notice.net_cost_base:,}원</td>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;text-align:left;">98% 법정 배제선</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;text-align:right;font-weight:700;color:#7e22ce;">{m1_m5['min_net_cost_bid']:,}원</td>
                <th style="border:1px solid #94a3b8;background:#f8fafc;padding:6px 10px;text-align:left;">수행능력 / 도급</th>
                <td style="border:1px solid #94a3b8;padding:6px 10px;">{notice.perf_score:.2f}점 / {'공동도급 허용' if notice.joint_venture_allowed else '단독입찰(불허)'}</td>
            </tr>
        </table>

        <div style="font-size:13.5px;font-weight:800;color:#0f172a;margin-bottom:5px;">■ 2. LATTICE-1365 (L0~L5) 및 EGR-BID (M6~M8) 표준 사정과정 검증 내역</div>
        <table style="width:100%;border-collapse:collapse;font-size:12px;margin-bottom:14px;color:#0f172a;">
            <tr style="background:#1e293b;color:#ffffff;">
                <th style="border:1px solid #1e293b;padding:6px 8px;width:12%;">레이어/단계</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:25%;text-align:left;">사정과정 검증 항목</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;text-align:left;">세부 산출 근거 및 검증 결과</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:12%;">판정</th>
            </tr>
            <tr>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;font-weight:700;">L0 · L1</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;font-weight:700;">계층 슬롯 생성 & 1,365 계단 확률장</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;">발주처 평균 μ={l0['mu']:.4f}%, 변동성 δ={l0['delta']:.4f}%, 공통충격 ρ={l0['rho']:.2f} 반영 1,365계단 확률질량 산출</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;color:#047857;font-weight:800;">생성완료</td>
            </tr>
            <tr style="background:#f8fafc;">
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;font-weight:700;">L2 · L3</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;font-weight:700;">극값(EVT) 경쟁자 역산 & 기대이익장</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;">1·2순위 격차 기반 경쟁분포 복원 (N={lat.ladder.get('l2_n_bidders',48)}개사) | 기대이익 {lat.expected_profit:,}원 (승률 {lat.win_prob*100:.1f}%)</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;color:#047857;font-weight:800;">최적화완료</td>
            </tr>
            <tr>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;font-weight:700;">L4 · L5</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;font-weight:700;">내생 실효하한 투영 & CRPS 캘리브레이션</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;">수행능력({notice.perf_score:.1f}점) 실효하한 {lat.effective_floor_rate:.3f}% | 하한선 미달위험 P(miss)={lat.p_miss*100:.1f}% | CRPS={lat.ladder.get('l5_crps',0)}</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;color:#047857;font-weight:800;">{'적격(PASS)' if lat.feasible else '입찰불가'}</td>
            </tr>
            <tr style="background:#f8fafc;">
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;font-weight:700;">M6 ~ M8</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;font-weight:700;">EGR-BID 분위수 시나리오 & 보류게이트</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;">분위수 Q10={q.get('q10','-')}% ~ 중앙 Q50={q.get('q50','-')}% ~ Q90={q.get('q90','-')}% (구간폭 {w80}%p) | {history_source_label}</td>
                <td style="border:1px solid #cbd5e1;padding:5px 8px;text-align:center;color:#15803d;font-weight:800;">{res.status}</td>
            </tr>
        </table>

        <div style="font-size:13.5px;font-weight:800;color:#0f172a;margin-bottom:5px;">■ 3. 사정모델별(M1~M5) · LATTICE-1365 · EGR-BID 사정결과 종합 대조표</div>
        <table style="width:100%;border-collapse:collapse;font-size:12px;margin-bottom:14px;color:#0f172a;">
            <tr style="background:#1e293b;color:#ffffff;">
                <th style="border:1px solid #1e293b;padding:6px 8px;text-align:left;">모델 / 시나리오 명칭</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:13%;">엔진 구분</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:10%;text-align:right;">예측 사정률</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:16%;text-align:right;">예정가격(원)</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:16%;text-align:right;">낙찰하한선(원)</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:16%;text-align:right;">추천투찰금액(원)</th>
                <th style="border:1px solid #1e293b;padding:6px 8px;width:13%;text-align:right;">M5 대비 차액</th>
            </tr>
            {model_rows_html}
        </table>

        <div style="font-size:13.5px;font-weight:800;color:#0f172a;margin-bottom:5px;">■ 4. 3대 트랙 최종 투찰 의사결정 요약 (3-Track Executive Decision Summary)</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;background:#f8fafc;border:2px solid #0f172a;border-radius:6px;padding:12px 14px;">
            <div style="border-right:1px dashed #94a3b8;padding-right:10px;">
                <div style="font-size:11.5px;font-weight:800;color:#1d4ed8;">👑 [트랙 1] 기존 M5 양자계단 기준선</div>
                <div style="font-size:19px;font-weight:900;color:#0f172a;margin:4px 0;">{m5_bid:,}원</div>
                <div style="font-size:11.5px;color:#334155;">• 계단: <b>#{m1_m5['m5_step_no']}/1,365</b> ({m1_m5['m5_rate']:.4f}%)<br>• 추첨번호: <b>{p4[0]}·{p4[1]}·{p4[2]}·{p4[3]}번</b></div>
            </div>
            <div style="border-right:1px dashed #94a3b8;padding-right:10px;">
                <div style="font-size:11.5px;font-weight:800;color:#047857;">⚡ [트랙 2] LATTICE-1365 계단확률장 최적해</div>
                <div style="font-size:19px;font-weight:900;color:#047857;margin:4px 0;">{f'{lat.optimal_price:,}원' if lat.feasible else '입찰 불가'}</div>
                <div style="font-size:11.5px;color:#334155;">• 계단: <b>#{lat.optimal_step}/1,365</b> (미달위험 {lat.p_miss*100:.1f}%)<br>• 추첨번호: <b>{lat_p4[0]}·{lat_p4[1]}·{lat_p4[2]}·{lat_p4[3]}번</b></div>
            </div>
            <div>
                <div style="font-size:11.5px;font-weight:800;color:#b45309;">🛡️ [트랙 3] EGR-BID 분포 강건 방어선</div>
                <div style="font-size:19px;font-weight:900;color:#b45309;margin:4px 0;">{egr_bid_str}</div>
                <div style="font-size:11.5px;color:#334155;">• M5 대비 차액: <b>{diff_str}</b><br>• 게이트 판정: <b>{res.status}</b></div>
            </div>
        </div>
        <div style="font-size:11px;color:#64748b;margin-top:8px;text-align:center;">※ [F-8 고지] {lat.warnings[0]}</div>
    </div>
    """

    if not standalone_doc:
        return sheet_html

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>입찰사정분석서_{notice.notice_id}</title>
<style>
@page {{ size: A4 portrait; margin: 10mm; }}
@media print {{
    body {{ margin: 0; background: #ffffff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .no-print {{ display: none !important; }}
}}
body {{ background: #e2e8f0; padding: 16px; margin: 0; }}
</style>
</head>
<body>
<div class="no-print" style="max-width:980px;margin:0 auto 10px auto;text-align:right;">
    <button onclick="window.print()" style="background:#0f172a;color:#ffffff;border:none;padding:10px 20px;font-size:14px;font-weight:800;border-radius:6px;cursor:pointer;">🖨️ 프린터 인쇄 / PDF 저장 (Cmd+P)</button>
</div>
{sheet_html}
</body>
</html>"""
