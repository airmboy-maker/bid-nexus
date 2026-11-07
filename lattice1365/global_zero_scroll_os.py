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
    "🛍️ [P1] 보물섬 공고 쇼룸 (3건)",
    "👑 [P2] M5 양자코어 전용실",
    "🛡️ [P3] EGR 강건방어 전용실",
    "⚡ [P4] LATTICE 격자 전용실",
    "📂 [P5] 문서·시방서 규격 볼트",
    "🎛️ [P6] 레이더 필터 & 보물카트",
]


def get_true_page_swap_css() -> str:
    """
    기존 앱의 불필요한 상하 여백과 헤더를 완전히 숨기고,
    단 한 화면(100vh) 안에서 페이지가 통째로 교체(Page Swap)되도록 고정하는 CSS
    """
    css = """
    <style>
    @keyframes pageSwapFade {
        0% {
            opacity: 0;
            transform: scale(0.99) translateY(8px);
        }
        100% {
            opacity: 1;
            transform: scale(1.0) translateY(0px);
        }
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 1.5rem !important;
    }

    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 0.3rem !important;
        padding-left: 1.6rem !important;
        padding-right: 1.6rem !important;
        max-width: 1560px !important;
    }

    .page-swap-canvas {
        animation: pageSwapFade 0.26s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        word-break: keep-all;
    }

    .swap-top-hud {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        background:
            radial-gradient(circle at 12% 50%, rgba(251, 191, 36, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 88% 50%, rgba(56, 189, 248, 0.18) 0%, transparent 45%),
            linear-gradient(90deg, #060a12 0%, #0f172a 50%, #060a12 100%);
        border: 1.5px solid rgba(251, 191, 36, 0.6);
        border-left: 5px solid #fbbf24;
        border-radius: 13px;
        padding: 9px 16px;
        margin-bottom: 8px;
        box-shadow: 0 10px 26px rgba(0, 0, 0, 0.75);
    }
    </style>
    """
    return "\n".join(line.lstrip() for line in css.splitlines())


def get_default_boutique_notices() -> List[Dict[str, Any]]:
    """
    풀스크린 교체 모드에서 즉시 사용할 9건의 표준 공고 데이터셋
    """
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


def render_sidebar_master_controller() -> str:
    """
    좌측 메인 메뉴(사이드바)에 장착되는:
    1) 화면 작동 방식 선택 (💎 1-Page 화면교체 OS vs 🌌 기존 통합 스크롤 모드)
    2) 6대 전용 페이지 직통 이동 메뉴 (클릭 시 스크롤 없이 화면 전체가 즉시 교체됨)
    """
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
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗂️ 6대 전용 페이지 바로가기</div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:700;">클릭 시 화면 전체가 즉시 교체됩니다</div>
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
    """
    기존의 긴 상단 배너·검색창·6개 탭을 완전히 건너뛰고,
    화면 맨 위부터 오직 선택된 단 1개의 전용 페이지(쇼룸 / M5 전용실 / EGR 전용실 / LATTICE 전용실 / 문서볼트 / 필터&카트)만
    전체 화면 교체(Page Swap)로 보여주는 무스크롤 OS
    """
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

    # 1. 최상단 슬림 HUD 바 (현재 페이지 + 현재 선택된 타겟 공고 + 카트 요약)
    cur_p_idx = st.session_state["_os_page_idx"]
    st.markdown(
        f"""
<div class="swap-top-hud">
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="background:linear-gradient(90deg,#fbbf24,#f59e0b);color:#020617;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:999px;">⚡ BID-NEXUS FULL-PAGE SWAP OS</span>
<span style="font-size:14.5px;font-weight:900;color:#f8fafc;">현재 화면: <span style="color:#fde68a;">{PAGE_MENUS[cur_p_idx]}</span></span>
<span style="color:#475569;">|</span>
<span style="font-size:13.5px;font-weight:800;color:#38bdf8;">🗝️ 타겟 공고: [{active_prof['nid']}] {active_prof['title'][:22]} (기초 {round(active_prof['base_amt']/100000000,1)}억)</span>
</div>
<div style="display:flex;align-items:center;gap:10px;">
<span style="background:rgba(16,185,129,0.16);border:1px solid #10b981;color:#34d399;font-size:11.5px;font-weight:900;padding:3px 10px;border-radius:999px;">🛍️ 카트 {len(cart_profs)}건 (+약 {profit_eok}억)</span>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # 2. 상단 6대 페이지 원클릭 교체 독(Dock) — 모델별로도 아예 페이지를 독립 분리!
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
    # PAGE 1: 🛍️ 보물섬 공고 쇼룸 (한 화면에 딱 3건만 보여주는 무스크롤 쇼케이스)
    # =========================================================================
    if cur_p_idx == 0:
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
                    b1, b2, b3, b4 = st.columns([1.1, 1.1, 1.1, 0.7])
                    if b1.button("👑 M5실행", key=f"ps_m5_{g_idx}", type="primary", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["_os_page_idx"] = 1
                        st.rerun()
                    if b2.button("🛡️ EGR실행", key=f"ps_egr_{g_idx}", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["_os_page_idx"] = 2
                        st.rerun()
                    if b3.button("📂 문서볼트", key=f"ps_doc_{g_idx}", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["_os_page_idx"] = 4
                        st.rerun()
                    if b4.button("💖" if not in_cart else "🗑️", key=f"ps_cart_{g_idx}", use_container_width=True):
                        if in_cart:
                            st.session_state["_boutique_cart_ids"].remove(gprof["nid"])
                        else:
                            st.session_state["_boutique_cart_ids"].append(gprof["nid"])
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # PAGE 2, 3, 4: 각 AI 모델별 독립 전용 페이지 (M5 전용실 / EGR 전용실 / LATTICE 전용실)
    # =========================================================================
    elif cur_p_idx in (1, 2, 3):
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        model_map = {
            1: "👑 [MODEL 1] M5 양자코어",
            2: "🛡️ [MODEL 2] EGR-BID 강건방어",
            3: "⚡ [MODEL 3] LATTICE-1365 격자",
        }
        chosen_model = model_map[cur_p_idx]

        # 상단 바에서 분석 대상 공고 변경 및 다른 모델 페이지로 1클릭 스왑
        c_pick, c_m1, c_m2, c_m3, c_doc = st.columns([2.2, 1.1, 1.1, 1.1, 1.1])
        with c_pick:
            notice_labels = [
                f"#{i+1:02d} [{analyze_construction_profile(x, i)['nid']}] {analyze_construction_profile(x, i)['title'][:18]}"
                for i, x in enumerate(live_bids)
            ]
            picked_label = st.selectbox(
                "🗝️ 타겟 공고 즉시 교체",
                notice_labels,
                index=sel_idx,
                key=f"_ps_picker_{cur_p_idx}",
                label_visibility="collapsed",
            )
            new_sel = notice_labels.index(picked_label)
            if new_sel != sel_idx:
                st.session_state["_boutique_selected_idx"] = new_sel
                st.rerun()
        with c_m1:
            if st.button("👑 M5 페이지로 교체", key="sw_m1", type="primary" if cur_p_idx == 1 else "secondary", use_container_width=True):
                st.session_state["_os_page_idx"] = 1
                st.rerun()
        with c_m2:
            if st.button("🛡️ EGR 페이지로 교체", key="sw_m2", type="primary" if cur_p_idx == 2 else "secondary", use_container_width=True):
                st.session_state["_os_page_idx"] = 2
                st.rerun()
        with c_m3:
            if st.button("⚡ LATTICE 페이지로 교체", key="sw_m3", type="primary" if cur_p_idx == 3 else "secondary", use_container_width=True):
                st.session_state["_os_page_idx"] = 3
                st.rerun()
        with c_doc:
            if st.button("📂 이 공고 문서볼트 ▶", key="sw_doc", use_container_width=True):
                st.session_state["_os_page_idx"] = 4
                st.rerun()

        # 단독 모델 풀스크린 스포트라이트 챔버 렌더링
        st.markdown(build_single_model_spotlight_html(active_prof, chosen_model), unsafe_allow_html=True)

        # 하단에는 해당 공고의 핵심 제원 요약 바만 한 줄로 깔끔하게 배치 (스크롤 제로)
        st.markdown(
            f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px;">
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 14px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">🏛 발주기관 / 마감일시</div>
<div style="font-size:13px;color:#f8fafc;font-weight:900;margin-top:2px;">{active_prof['agency']} ({active_prof['deadline']})</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 14px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">💎 기초금액 / 법정 A값</div>
<div style="font-size:13px;color:#38bdf8;font-weight:900;margin-top:2px;">{active_prof['base_amt']:,}원 / A값 {active_prof['a_val']:,}원</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 14px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">💰 추정 순공사원가 (98% 배제선)</div>
<div style="font-size:13px;color:#fbbf24;font-weight:900;margin-top:2px;">{active_prof['est_net_cost']:,}원 ({int(active_prof['est_net_cost']*0.98):,}원)</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 14px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">⚖️ 다른 두 모델 타점 빠른 비교</div>
<div style="font-size:11.5px;color:#cbd5e1;font-weight:800;margin-top:2px;">M5 {active_prof['bid_m5']:,} | EGR {active_prof['bid_egr']:,}</div>
</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # PAGE 5: 📂 프라이빗 문서·시방서 규격 볼트 (1-Page 1-Document 교체 열람)
    # =========================================================================
    elif cur_p_idx == 4:
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

    # =========================================================================
    # PAGE 6: 🎛️ 레이더 필터 설정 & 보물 카트 체크아웃 전용 페이지
    # =========================================================================
    elif cur_p_idx == 5:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        f_c1, f_c2, f_c3, f_c4 = st.columns([1.4, 1.1, 1.1, 1.1])
        with f_c1:
            st.text_input("🏢 1-Click 기업명·초성 검색", placeholder="예: '선', '태양', '강원'", key="ps_q_comp")
        with f_c2:
            st.selectbox("1️⃣ 보유 면허", ["건축공사업", "토목건축공사업", "전체 면허"], key="ps_lic")
        with f_c3:
            st.selectbox("2️⃣ 관할 지역", ["강원특별자치도", "서울·수도권", "전국 발주"], key="ps_reg")
        with f_c4:
            st.selectbox("3️⃣ 공사 규모", ["전체 규모", "30억~50억", "50억~100억"], key="ps_scale")

        rows_html = ""
        for idx_c, cp in enumerate(cart_profs, start=1):
            est_p = cp["bid_m5"] - cp["est_net_cost"]
            rows_html += f"""
<tr style="border-bottom:1px solid rgba(51,65,85,0.65);">
<td style="padding:9px 12px;font-weight:900;color:#fbbf24;">#0{idx_c}</td>
<td style="padding:9px 12px;font-weight:800;color:#7dd3fc;">{cp['nid']}</td>
<td style="padding:9px 12px;font-weight:900;color:#f8fafc;">{cp['title']}</td>
<td style="padding:9px 12px;text-align:right;font-weight:800;color:#e2e8f0;">{cp['base_amt']:,}원</td>
<td style="padding:9px 12px;text-align:right;font-weight:900;color:#38bdf8;">{cp['bid_m5']:,}원</td>
<td style="padding:9px 12px;text-align:right;font-weight:900;color:#fbbf24;">{cp['bid_egr']:,}원</td>
<td style="padding:9px 12px;text-align:right;font-weight:900;color:#34d399;">+{est_p:,}원</td>
</tr>"""

        if not rows_html:
            rows_html = '<tr><td colspan="7" style="padding:18px;text-align:center;color:#94a3b8;font-weight:800;">카트에 담긴 공고가 없습니다. [P1] 공고 쇼룸에서 💖 버튼을 눌러 담아주세요.</td></tr>'

        cart_html = f"""
<div style="background:rgba(15,23,42,0.92);border:1.5px solid rgba(251,191,36,0.45);border-radius:14px;padding:16px 20px;margin-top:8px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.2);">
<span style="font-size:15.5px;font-weight:900;color:#f8fafc;">🛍️ 나의 보물 카트 포트폴리오 & 3대 모델 투찰가 총괄표 ({len(cart_profs)}건)</span>
<span style="background:rgba(16,185,129,0.18);border:1px solid #10b981;color:#34d399;font-size:11.5px;font-weight:900;padding:3px 10px;border-radius:999px;">합산 기대수익: +{total_cart_profit:,}원 (약 {profit_eok}억 원)</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:12.5px;text-align:left;">
<thead>
<tr style="background:rgba(2,6,23,0.9);border-bottom:2px solid #fbbf24;color:#94a3b8;font-size:11.5px;">
<th style="padding:8px 12px;">순번</th>
<th style="padding:8px 12px;">공고번호</th>
<th style="padding:8px 12px;">공고명</th>
<th style="padding:8px 12px;text-align:right;">기초금액</th>
<th style="padding:8px 12px;text-align:right;">👑 M5 추천가</th>
<th style="padding:8px 12px;text-align:right;">🛡️ EGR 방어가</th>
<th style="padding:8px 12px;text-align:right;">예상 순이익</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>
"""
        st.markdown("\n".join(l.lstrip() for l in cart_html.splitlines() if l.strip()), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
