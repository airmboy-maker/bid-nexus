from typing import Dict, Any, List
import streamlit as st
from lattice1365.notice_dossier_vault import (
    analyze_construction_profile,
    build_notice_dossier_html,
    generate_notice_attachments,
    generate_master_zip_bundle,
    build_boq_preview_table_html,
    build_spec_sheet_html,
    build_manifest_table_html,
)
from lattice1365.boutique_vault_ui import (
    get_boutique_vault_css,
    build_jewel_showcase_tile_html,
)
from lattice1365.zero_scroll_stage import build_single_model_spotlight_html


PAGE_MENUS = [
    "🔥 [P1] 3대 AI 모델 통합 지휘소",
    "👑 [P2] M5 양자코어 (M1~M5)",
    "🛡️ [P3] EGR 강건방어 (M6~M8)",
    "⚡ [P4] LATTICE 1,365 격자",
    "🛍️ [P5] 보물섬 공고 쇼룸 (3건)",
    "📂 [P6] 문서·시방서 규격 볼트",
]


def get_true_page_swap_css() -> str:
    css = """
    <style>
    @keyframes pageSwapFade {
        0% { opacity: 0; transform: scale(0.992) translateY(6px); }
        100% { opacity: 1; transform: scale(1.0) translateY(0px); }
    }
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 1560px !important;
    }
    .page-swap-canvas {
        animation: pageSwapFade 0.25s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        word-break: keep-all;
    }
    .swap-top-hud {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        background: linear-gradient(90deg, #060a12 0%, #0f172a 50%, #060a12 100%);
        border: 1.5px solid rgba(251, 191, 36, 0.65);
        border-left: 5px solid #fbbf24;
        border-radius: 13px;
        padding: 10px 18px;
        margin-bottom: 10px;
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.75);
    }
    </style>
    """
    return "\n".join(line.lstrip() for line in css.splitlines())


def get_default_boutique_notices() -> List[Dict[str, Any]]:
    return [
        {"id": "202611-01540", "title": "춘천시청 별관 신축 및 문화복합동 증축공사", "agency": "강원특별자치도 춘천시", "deadline": "2026-11-13 10:00", "base_amount": 4250000000, "a_value": 195400000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-01882", "title": "강릉 영동권 공공산후조리원 및 육아통합지원센터 신축공사", "agency": "강원특별자치도 강릉시", "deadline": "2026-11-13 10:00", "base_amount": 5180000000, "a_value": 241800000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-02410", "title": "속초해양경찰서 전용부두 청사 및 복지관 신축 건축공사", "agency": "조달청 강원지방조달청", "deadline": "2026-11-13 10:00", "base_amount": 7840000000, "a_value": 368500000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-02775", "title": "홍천군 국민체육센터 및 실내수영장 건립 건축공사", "agency": "강원특별자치도 홍천군", "deadline": "2026-11-13 10:00", "base_amount": 8920000000, "a_value": 412000000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-03110", "title": "강원대학교 춘천캠퍼스 첨단산학협력관 리모델링 및 증축공사", "agency": "강원대학교", "deadline": "2026-11-13 10:00", "base_amount": 3950000000, "a_value": 184200000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-03490", "title": "원주 혁신도시 복합문화체육센터 신축 건축공사", "agency": "강원특별자치도 원주시", "deadline": "2026-11-14 10:00", "base_amount": 6420000000, "a_value": 298000000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-03812", "title": "동해항 제3부두 해경 파출소 및 통합관제센터 신축공사", "agency": "조달청 강원지방조달청", "deadline": "2026-11-14 14:00", "base_amount": 4890000000, "a_value": 226000000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-04125", "title": "태백시 스마트 그린리모델링 공공임대주택 및 복지관 증축공사", "agency": "강원특별자치도 태백시", "deadline": "2026-11-15 10:00", "base_amount": 3580000000, "a_value": 169000000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
        {"id": "202611-04590", "title": "삼척시 복합체육문화센터 및 다목적실내체육관 신축공사", "agency": "강원특별자치도 삼척시", "deadline": "2026-11-15 14:00", "base_amount": 7150000000, "a_value": 334000000, "lower_limit_rate": 88.745, "license": "건축공사업", "region": "강원특별자치도"},
    ]


def build_all_models_command_deck_html(prof: Dict[str, Any]) -> str:
    """
    [P1] 무스크롤 모드의 첫 화면: 사라졌던 3대 AI 모델(M5 양자코어 / EGR 강건방어 / LATTICE 1365)과
    나라장터 15개 복수예가 번호판(추천 2픽 하이라이트)을 한 화면에 스크롤 없이 완벽하게 보여주는 통합 지휘소
    """
    base_amt = prof["base_amt"]
    a_val = prof["a_val"]
    low_rate = prof["low_rate"]
    net_cost = prof["est_net_cost"]

    p_m5 = prof["bid_m5"] - net_cost
    p_egr = prof["bid_egr"] - net_cost
    p_lat = prof["bid_lat"] - net_cost

    # 1~15번 복수예비가격 번호판 생성 (2번, 3번, 12번, 13번 AI 타겟 하이라이트)
    balls_html = ""
    offsets = [-2.75, -2.35, -1.95, -1.55, -1.15, -0.75, -0.35, 0.05, 0.45, 0.85, 1.25, 1.65, 2.05, 2.45, 2.85]
    for b_no in range(1, 16):
        rate_b = 100.0 + offsets[b_no - 1]
        if b_no in (2, 12):
            bg = "linear-gradient(135deg,#0284c7,#38bdf8)"
            bd = "2px solid #fef08a"
            tag = "👑 M5 픽"
            col = "#ffffff"
        elif b_no == 3:
            bg = "linear-gradient(135deg,#d97706,#fbbf24)"
            bd = "2px solid #fef08a"
            tag = "🛡️ EGR 픽"
            col = "#020617"
        elif b_no == 13:
            bg = "linear-gradient(135deg,#059669,#10b981)"
            bd = "2px solid #fef08a"
            tag = "⚡ LAT 픽"
            col = "#020617"
        else:
            bg = "rgba(15,23,42,0.9)"
            bd = "1px solid #334155"
            tag = f"{rate_b:.2f}%"
            col = "#94a3b8"

        balls_html += f"""
<div style="background:{bg};border:{bd};border-radius:10px;padding:7px 4px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.45);">
<div style="font-size:13px;font-weight:900;color:{col};">{b_no}번</div>
<div style="font-size:9.5px;font-weight:800;color:{col};margin-top:2px;">{tag}</div>
</div>"""

    raw = f"""
<div style="background:linear-gradient(155deg,#070c18 0%,#0f172a 55%,#050811 100%);border:1.5px solid rgba(56,189,248,0.45);border-radius:18px;padding:18px 22px;box-shadow:0 18px 42px rgba(0,0,0,0.8);">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;padding-bottom:10px;margin-bottom:14px;border-bottom:1px solid rgba(148,163,184,0.2);">
<div>
<span style="background:linear-gradient(90deg,#38bdf8,#10b981);color:#020617;font-size:10px;font-weight:900;padding:3px 10px;border-radius:999px;">TRIPLE-TRACK AI ENGINE DECK</span>
<span style="font-size:17px;font-weight:900;color:#f8fafc;margin-left:8px;">🔥 [{prof['nid']}] {prof['title']} — 3대 AI 모델 동시 가동 상황판</span>
</div>
<span style="font-size:12px;font-weight:800;color:#fde68a;">💎 기초금액: {base_amt:,}원 &nbsp;|&nbsp; 🛡️ A값: {a_val:,}원 &nbsp;|&nbsp; 🎯 낙찰하한율: {low_rate:.3f}%</span>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px;">
<div style="background:linear-gradient(145deg,rgba(14,165,233,0.16),rgba(15,23,42,0.95));border:2px solid #38bdf8;border-radius:14px;padding:15px 16px;box-shadow:0 0 24px rgba(56,189,248,0.2);">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="background:#38bdf8;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">MODEL 01 · M1~M5 코어</span>
<span style="font-size:11px;font-weight:900;color:#7dd3fc;">조합 #238 Lock</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;margin-bottom:8px;">👑 M5 양자코어 (메인 기준선)</div>
<div style="background:rgba(2,6,23,0.8);border:1px solid rgba(56,189,248,0.35);border-radius:10px;padding:10px 12px;margin-bottom:8px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;"><span>목표 사정률</span><span style="color:#38bdf8;font-size:14px;font-weight:900;">100.0907%</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>권장 투찰금액</span><span style="color:#fef08a;font-size:16px;font-weight:900;">{prof['bid_m5']:,}원</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>예상 순이익</span><span style="color:#34d399;font-size:13.5px;font-weight:900;">+{p_m5:,}원</span></div>
</div>
<div style="font-size:11.5px;font-weight:800;color:#bae6fd;text-align:center;background:rgba(56,189,248,0.15);padding:5px;border-radius:8px;">🎲 나라장터 추천 2픽: <b>2번 + 12번</b></div>
</div>

<div style="background:linear-gradient(145deg,rgba(245,158,11,0.16),rgba(15,23,42,0.95));border:2px solid #fbbf24;border-radius:14px;padding:15px 16px;box-shadow:0 0 24px rgba(251,191,36,0.18);">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">MODEL 02 · M6·M7·M8</span>
<span style="font-size:11px;font-weight:900;color:#fde68a;">Q50 중위방어</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;margin-bottom:8px;">🛡️ EGR-BID 강건방어 (하한방어)</div>
<div style="background:rgba(2,6,23,0.8);border:1px solid rgba(251,191,36,0.35);border-radius:10px;padding:10px 12px;margin-bottom:8px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;"><span>목표 사정률</span><span style="color:#fbbf24;font-size:14px;font-weight:900;">100.1100%</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>권장 투찰금액</span><span style="color:#fef08a;font-size:16px;font-weight:900;">{prof['bid_egr']:,}원</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>예상 순이익</span><span style="color:#34d399;font-size:13.5px;font-weight:900;">+{p_egr:,}원</span></div>
</div>
<div style="font-size:11.5px;font-weight:800;color:#fde68a;text-align:center;background:rgba(245,158,11,0.15);padding:5px;border-radius:8px;">🎲 나라장터 추천 2픽: <b>3번 + 12번</b></div>
</div>

<div style="background:linear-gradient(145deg,rgba(16,185,129,0.16),rgba(15,23,42,0.95));border:2px solid #10b981;border-radius:14px;padding:15px 16px;box-shadow:0 0 24px rgba(16,185,129,0.18);">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="background:#10b981;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">MODEL 03 · L0~L5 격자</span>
<span style="font-size:11px;font-weight:900;color:#6ee7b7;">조합 #338 피크</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;margin-bottom:8px;">⚡ LATTICE-1365 (계단 확률장)</div>
<div style="background:rgba(2,6,23,0.8);border:1px solid rgba(16,185,129,0.35);border-radius:10px;padding:10px 12px;margin-bottom:8px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;"><span>목표 사정률</span><span style="color:#34d399;font-size:14px;font-weight:900;">100.0658%</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>권장 투찰금액</span><span style="color:#fef08a;font-size:16px;font-weight:900;">{prof['bid_lat']:,}원</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>예상 순이익</span><span style="color:#34d399;font-size:13.5px;font-weight:900;">+{p_lat:,}원</span></div>
</div>
<div style="font-size:11.5px;font-weight:800;color:#a7f3d0;text-align:center;background:rgba(16,185,129,0.15);padding:5px;border-radius:8px;">🎲 나라장터 추천 2픽: <b>2번 + 13번</b></div>
</div>
</div>

<div style="background:rgba(2,6,23,0.85);border:1px solid rgba(56,189,248,0.3);border-radius:12px;padding:10px 14px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
<span style="font-size:12px;font-weight:900;color:#f8fafc;">🎱 나라장터 15개 복수예비가격 번호판 실시간 타겟 매핑 (15C4 = 1,365계단)</span>
<span style="font-size:11px;color:#7dd3fc;font-weight:800;">상단 [P2 M5] · [P3 EGR] · [P4 LATTICE] 버튼을 누르면 개별 모델 전용 페이지로 즉시 교체됩니다</span>
</div>
<div style="display:grid;grid-template-columns:repeat(15,1fr);gap:6px;">
{balls_html}
</div>
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def render_sidebar_master_controller() -> str:
    if "_os_page_idx" not in st.session_state:
        st.session_state["_os_page_idx"] = 0

    with st.sidebar:
        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.22),rgba(15,23,42,0.96));border:1.5px solid #fbbf24;border-radius:10px;padding:8px 11px;margin-top:2px;margin-bottom:6px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:11px;font-weight:900;color:#fde68a;">💎 SCREEN MODE SWITCH</span>
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">FULL-SWAP</span>
</div>
</div>
""",
            unsafe_allow_html=True,
        )
        ui_mode = st.radio(
            "화면 모드 선택",
            [
                "💎 1-Page 화면교체 모드 (무스크롤)",
                "🌌 기존 통합 스크롤 모드 (v20.4)",
            ],
            index=0,
            key="_global_app_ui_mode",
            label_visibility="collapsed",
        )

        if "1-Page" in ui_mode:
            st.markdown(
                """
<div style="background:rgba(14,165,233,0.14);border:1px solid rgba(56,189,248,0.45);border-left:3.5px solid #38bdf8;border-radius:8px;padding:6px 10px;margin-top:4px;margin-bottom:4px;">
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗂️ AI 모델 & 쇼룸 페이지 교체</div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:700;">클릭 시 스크롤 없이 페이지가 교체됩니다</div>
</div>
""",
                unsafe_allow_html=True,
            )
            for p_i, p_label in enumerate(PAGE_MENUS):
                is_cur = (st.session_state["_os_page_idx"] == p_i)
                if st.button(
                    p_label,
                    key=f"sb_jump_p_{p_i}",
                    type="primary" if is_cur else "secondary",
                    use_container_width=True,
                ):
                    st.session_state["_os_page_idx"] = p_i
                    st.rerun()

    return ui_mode


def render_full_page_swap_os(notices: List[Dict[str, Any]] = None) -> None:
    live_bids = notices if notices else get_default_boutique_notices()

    st.markdown(get_boutique_vault_css(), unsafe_allow_html=True)
    st.markdown(get_true_page_swap_css(), unsafe_allow_html=True)

    if "_os_page_idx" not in st.session_state:
        st.session_state["_os_page_idx"] = 0
    if "_zs_page" not in st.session_state:
        st.session_state["_zs_page"] = 0
    if "_boutique_selected_idx" not in st.session_state:
        st.session_state["_boutique_selected_idx"] = 0
    if "_boutique_cart_ids" not in st.session_state:
        first_nid = analyze_construction_profile(live_bids[0], 0)["nid"]
        st.session_state["_boutique_cart_ids"] = [first_nid]

    sel_idx = min(st.session_state["_boutique_selected_idx"], max(0, len(live_bids) - 1))
    active_n = live_bids[sel_idx]
    active_prof = analyze_construction_profile(active_n, sel_idx)

    cart_profs = [
        analyze_construction_profile(x, i)
        for i, x in enumerate(live_bids)
        if analyze_construction_profile(x, i)["nid"] in st.session_state["_boutique_cart_ids"]
    ]
    total_cart_profit = sum((p["bid_m5"] - p["est_net_cost"]) for p in cart_profs)
    profit_eok = round(total_cart_profit / 100_000_000.0, 2)

    cur_p_idx = st.session_state["_os_page_idx"]

    # 최상단 타겟 공고 선택바 + 현재 페이지 표시줄
    top_h1, top_h2 = st.columns([2.3, 1.2])
    with top_h1:
        st.markdown(
            f"""
<div class="swap-top-hud" style="margin-bottom:4px;">
<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
<span style="background:linear-gradient(90deg,#fbbf24,#f59e0b);color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;">⚡ ZERO-SCROLL PAGE SWAP</span>
<span style="font-size:14px;font-weight:900;color:#fde68a;">{PAGE_MENUS[cur_p_idx]}</span>
<span style="color:#475569;">|</span>
<span style="font-size:13px;font-weight:800;color:#38bdf8;">[{active_prof['nid']}] {active_prof['title'][:20]}</span>
</div>
<span style="background:rgba(16,185,129,0.16);border:1px solid #10b981;color:#34d399;font-size:11px;font-weight:900;padding:2px 9px;border-radius:999px;">카트 {len(cart_profs)}건 (+약 {profit_eok}억)</span>
</div>
""",
            unsafe_allow_html=True,
        )
    with top_h2:
        notice_labels = [
            f"🎯 타겟공고 #{i+1:02d}: [{analyze_construction_profile(x, i)['nid']}] {analyze_construction_profile(x, i)['title'][:16]}"
            for i, x in enumerate(live_bids)
        ]
        picked_label = st.selectbox(
            "타겟 공고 즉시 변경",
            notice_labels,
            index=sel_idx,
            key="_global_top_notice_picker",
            label_visibility="collapsed",
        )
        new_sel = notice_labels.index(picked_label)
        if new_sel != sel_idx:
            st.session_state["_boutique_selected_idx"] = new_sel
            st.rerun()

    # 상단 6대 페이지 원클릭 교체 버튼 바 (P1: 3대 모델 통합 / P2: M5 / P3: EGR / P4: LATTICE / P5: 쇼룸 / P6: 문서볼트)
    nav_cols = st.columns(6)
    for p_i, p_label in enumerate(PAGE_MENUS):
        if nav_cols[p_i].button(
            p_label,
            key=f"top_swap_btn_{p_i}",
            type="primary" if cur_p_idx == p_i else "secondary",
            use_container_width=True,
        ):
            st.session_state["_os_page_idx"] = p_i
            st.rerun()

    # =========================================================================
    # [P1] 🔥 3대 AI 모델 통합 지휘소 (기본 첫 화면 — 모든 모델과 15개 예가 번호판이 한눈에!)
    # =========================================================================
    if cur_p_idx == 0:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        st.markdown(build_all_models_command_deck_html(active_prof), unsafe_allow_html=True)
        b_c1, b_c2, b_c3, b_c4 = st.columns(4)
        if b_c1.button("👑 [M5 양자코어] 단독 상세 페이지로 교체 ▶", key="p1_to_m5", type="primary", use_container_width=True):
            st.session_state["_os_page_idx"] = 1
            st.rerun()
        if b_c2.button("🛡️ [EGR 강건방어] 단독 상세 페이지로 교체 ▶", key="p1_to_egr", use_container_width=True):
            st.session_state["_os_page_idx"] = 2
            st.rerun()
        if b_c3.button("⚡ [LATTICE 1365] 단독 상세 페이지로 교체 ▶", key="p1_to_lat", use_container_width=True):
            st.session_state["_os_page_idx"] = 3
            st.rerun()
        if b_c4.button("📂 [시방서·공내역서 규격 볼트] 페이지로 교체 ▶", key="p1_to_doc", use_container_width=True):
            st.session_state["_os_page_idx"] = 5
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P2, P3, P4] 개별 AI 모델 전용 페이지 (M5 / EGR / LATTICE 1-Page 1-Model)
    # =========================================================================
    elif cur_p_idx in (1, 2, 3):
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        model_map = {
            1: "👑 [MODEL 1] M5 양자코어",
            2: "🛡️ [MODEL 2] EGR-BID 강건방어",
            3: "⚡ [MODEL 3] LATTICE-1365 격자",
        }
        chosen_model = model_map[cur_p_idx]
        st.markdown(build_single_model_spotlight_html(active_prof, chosen_model), unsafe_allow_html=True)

        m_b1, m_b2, m_b3, m_b4 = st.columns(4)
        if m_b1.button("🔥 [P1] 3대 모델 동시 비교 상황판으로 복귀", key="back_p1", use_container_width=True):
            st.session_state["_os_page_idx"] = 0
            st.rerun()
        if m_b2.button("👑 M5 양자코어 페이지", key="sw_m1", type="primary" if cur_p_idx == 1 else "secondary", use_container_width=True):
            st.session_state["_os_page_idx"] = 1
            st.rerun()
        if m_b3.button("🛡️ EGR 강건방어 페이지", key="sw_m2", type="primary" if cur_p_idx == 2 else "secondary", use_container_width=True):
            st.session_state["_os_page_idx"] = 2
            st.rerun()
        if m_b4.button("⚡ LATTICE 1365 페이지", key="sw_m3", type="primary" if cur_p_idx == 3 else "secondary", use_container_width=True):
            st.session_state["_os_page_idx"] = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P5] 🛍️ 보물섬 공고 쇼룸 (1페이지 3건씩 무스크롤 진열)
    # =========================================================================
    elif cur_p_idx == 4:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        page_size = 3
        total_pages = max(1, (len(live_bids) + page_size - 1) // page_size)
        cur_page = min(st.session_state["_zs_page"], total_pages - 1)
        start_i = cur_page * page_size
        end_i = min(len(live_bids), start_i + page_size)

        p_c1, p_c2, p_c3 = st.columns([1.1, 2.8, 1.1])
        with p_c1:
            if st.button("◀ 이전 3건 쇼윈도", key="ps_prev_p", disabled=(cur_page <= 0), use_container_width=True):
                st.session_state["_zs_page"] = max(0, cur_page - 1)
                st.rerun()
        with p_c2:
            st.markdown(
                f"<div style='text-align:center;padding:6px;background:rgba(15,23,42,0.9);border:1px solid rgba(251,191,36,0.4);border-radius:10px;font-size:13px;font-weight:900;color:#fde68a;'>💎 TREASURE SHOWCASE — PAGE {cur_page+1} / {total_pages} &nbsp;(공고 #{start_i+1} ~ #{end_i} / 전체 {len(live_bids)}건)</div>",
                unsafe_allow_html=True,
            )
        with p_c3:
            if st.button("다음 3건 쇼윈도 ▶", key="ps_next_p", disabled=(cur_page >= total_pages - 1), use_container_width=True):
                st.session_state["_zs_page"] = min(total_pages - 1, cur_page + 1)
                st.rerun()

        cols = st.columns(3)
        for offset in range(page_size):
            g_idx = start_i + offset
            if g_idx < len(live_bids):
                gn = live_bids[g_idx]
                gprof = analyze_construction_profile(gn, g_idx)
                is_act = (g_idx == sel_idx)
                in_cart = (gprof["nid"] in st.session_state["_boutique_cart_ids"])
                with cols[offset]:
                    st.markdown(build_jewel_showcase_tile_html(gprof, g_idx, is_act, in_cart), unsafe_allow_html=True)
                    b1, b2, b3 = st.columns([1.4, 1.2, 0.8])
                    if b1.button("🔥 3대모델 분석", key=f"ps_all_{g_idx}", type="primary", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["_os_page_idx"] = 0
                        st.rerun()
                    if b2.button("📂 문서볼트", key=f"ps_doc_{g_idx}", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["_os_page_idx"] = 5
                        st.rerun()
                    if b3.button("💖" if not in_cart else "🗑️", key=f"ps_cart_{g_idx}", use_container_width=True):
                        if in_cart:
                            st.session_state["_boutique_cart_ids"].remove(gprof["nid"])
                        else:
                            st.session_state["_boutique_cart_ids"].append(gprof["nid"])
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P6] 📂 프라이빗 문서·시방서 규격 볼트 (1-Page 1-Document 교체 열람)
    # =========================================================================
    elif cur_p_idx == 5:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        doc_html, boq_csv, bid_json, spec_txt = generate_notice_attachments(active_prof)
        zip_bytes, zip_meta = generate_master_zip_bundle(active_prof)

        v_c1, v_c2 = st.columns([2.2, 1.3])
        with v_c1:
            doc_choice = st.radio(
                "📑 화면에 표시할 단일 규격 양식서 선택",
                [
                    "🏗️ [1] 현장 종합 브리핑 도감",
                    "📐 [2] 공사시방서 & AI 전략 규격서",
                    "📊 [3] 표준 공내역서(BoQ) 테이블",
                    "🔐 [4] SHA-256 무결성 검증서",
                ],
                horizontal=True,
                key="_ps_single_doc_choice",
                label_visibility="collapsed",
            )
        with v_c2:
            st.download_button(
                label=f"📦 [1-Click 마스터 번들 ZIP 다운로드] ({active_prof['nid']}.zip · {zip_meta['zip_size_kb']} KB)",
                data=zip_bytes,
                file_name=f"G2B_마스터패키지_{active_prof['nid']}.zip",
                mime="application/zip",
                key=f"ps_dl_zip_{active_prof['nid']}",
                type="primary",
                use_container_width=True,
            )

        if "[1]" in doc_choice:
            st.markdown(build_notice_dossier_html(active_prof), unsafe_allow_html=True)
        elif "[2]" in doc_choice:
            st.markdown(build_spec_sheet_html(active_prof), unsafe_allow_html=True)
        elif "[3]" in doc_choice:
            st.markdown(build_boq_preview_table_html(active_prof), unsafe_allow_html=True)
        else:
            st.markdown(build_manifest_table_html(active_prof, zip_meta), unsafe_allow_html=True)

        d1, d2, d3, d4 = st.columns(4)
        d1.download_button("📄 입찰공고문 (.html)", data=doc_html, file_name=f"입찰공고문_{active_prof['nid']}.html", mime="text/html", key="ps_d1", use_container_width=True)
        d2.download_button("📊 공내역서 (.csv)", data=boq_csv, file_name=f"공내역서_{active_prof['nid']}.csv", mime="text/csv", key="ps_d2", use_container_width=True)
        d3.download_button("📦 G2B 제원 (.json)", data=bid_json, file_name=f"G2B제원_{active_prof['nid']}.json", mime="application/json", key="ps_d3", use_container_width=True)
        d4.download_button("📐 공사시방서 (.txt)", data=spec_txt, file_name=f"공사시방서_{active_prof['nid']}.txt", mime="text/plain", key="ps_d4", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# 하위 호환 별칭
def render_global_zero_scroll_app(live_bids=None):
    return render_full_page_swap_os(live_bids)


def render_sidebar_ui_mode_selector():
    return render_sidebar_master_controller()
