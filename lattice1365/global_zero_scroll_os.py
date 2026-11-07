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


def get_fullscreen_os_css() -> str:
    """
    브라우저 세로 스크롤바 발생을 억제하고, 작업 전환 시 부드러운 3D 슬라이드/페이드인 트랜지션을 부여하는 CSS
    """
    css = """
    <style>
    @keyframes stageMorphIn {
        0% {
            opacity: 0;
            transform: translateY(12px) scale(0.992);
            filter: blur(3px);
        }
        100% {
            opacity: 1;
            transform: translateY(0px) scale(1.0);
            filter: blur(0px);
        }
    }

    
    /* 제로스크롤 OS 활성화 시 상단 중복 안내문/여백을 최소화 */
    div[data-testid="stVerticalBlock"] > div {
        margin-bottom: 0px !important;
    }

    /* 전체 페이지 상하 패딩을 극한으로 압축하여 한 화면(One-Viewport)에 쏙 들어오도록 고정 */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 0.4rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 1520px !important;
    }

    /* 스테이지 전환 애니메이션 래퍼 */
    .os-stage-viewport {
        animation: stageMorphIn 0.34s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        word-break: keep-all;
    }

    /* 상단 슬림 OS 커맨드 헤더 */
    .os-top-ribbon {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        background:
            radial-gradient(circle at 10% 50%, rgba(251, 191, 36, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 90% 50%, rgba(56, 189, 248, 0.16) 0%, transparent 45%),
            linear-gradient(90deg, #070b14 0%, #0f172a 50%, #070b14 100%);
        border: 1.5px solid rgba(251, 191, 36, 0.55);
        border-left: 5px solid #fbbf24;
        border-radius: 14px;
        padding: 10px 18px;
        margin-bottom: 10px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.72);
    }

    /* 단일 작업 캐비닛 프레임 */
    .os-cabinet-frame {
        background:
            radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.11) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(16, 185, 129, 0.10) 0%, transparent 45%),
            linear-gradient(155deg, #090e1c 0%, #050811 100%);
        border: 1.5px solid rgba(56, 189, 248, 0.38);
        border-radius: 18px;
        padding: 18px 22px;
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    </style>
    """
    return "\n".join(line.lstrip() for line in css.splitlines())


def render_sidebar_ui_mode_selector() -> str:
    """
    좌측 메인 메뉴(사이드바)에서 전체 앱의 작동 모드(1-Page 제로스크롤 부티크 OS vs 기존 통합 스크롤 모드)와
    현재 열린 캐비닛 메뉴를 직접 선택할 수 있는 컨트롤러
    """
    with st.sidebar:
        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.18),rgba(15,23,42,0.95));border:1.5px solid #fbbf24;border-radius:10px;padding:8px 11px;margin-top:4px;margin-bottom:6px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;">
<span style="font-size:11px;font-weight:900;color:#fde68a;">💎 UI ARCHITECTURE MODE</span>
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">v3.0 OS</span>
</div>
<div style="font-size:10px;color:#cbd5e1;font-weight:700;">한 화면 1작업(Zero-Scroll) vs 기존 방식</div>
</div>
""",
            unsafe_allow_html=True,
        )
        ui_mode = st.radio(
            "글로벌 화면 모드 선택",
            [
                "💎 1-Page 제로스크롤 부티크 OS",
                "🌌 기존 통합 스크롤 모드 (v20.4)",
            ],
            index=0,
            key="_global_app_ui_mode",
            label_visibility="collapsed",
        )
    return ui_mode


def render_global_zero_scroll_app(live_bids: List[Dict[str, Any]]) -> None:
    """
    [💎 1-Page 제로스크롤 부티크 OS] 선택 시 전체 화면을 장악하여,
    스크롤 없이 5대 독립 캐비닛(레이더 필터 / 3건 쇼룸 / 단일 AI 모델 실행실 / 단일 문서 볼트 / 원클릭 투찰 요약)을
    한 화면 안에서 자연스럽게 전환하며 처리하는 마스터 워크스페이스
    """
    st.markdown(get_boutique_vault_css(), unsafe_allow_html=True)
    st.markdown(get_fullscreen_os_css(), unsafe_allow_html=True)

    if not live_bids:
        st.warning("조건에 부합하는 실시간 공고가 없습니다.")
        return

    if "_os_active_menu" not in st.session_state:
        st.session_state["_os_active_menu"] = "M2_SHOWROOM"
    if "_zs_page" not in st.session_state:
        st.session_state["_zs_page"] = 0
    if "_boutique_selected_idx" not in st.session_state:
        st.session_state["_boutique_selected_idx"] = 0
    if "_boutique_cart_ids" not in st.session_state:
        first_nid = analyze_construction_profile(live_bids[0], 0)["nid"]
        st.session_state["_boutique_cart_ids"] = [first_nid]

    # 필터 상태 기본값 유지
    if "_os_f_lic" not in st.session_state:
        st.session_state["_os_f_lic"] = "건축공사업"
    if "_os_f_reg" not in st.session_state:
        st.session_state["_os_f_reg"] = "강원특별자치도"
    if "_os_f_scale" not in st.session_state:
        st.session_state["_os_f_scale"] = "전체 규모"

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

    # 1. 최상단 슬림 OS 상태 리본 (현재 열린 공고 + 위시리스트 카트 수익 + 무스크롤 상태 표시)
    st.markdown(
        f"""
<div class="os-top-ribbon">
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
<span style="background:linear-gradient(90deg,#fbbf24,#f59e0b);color:#020617;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:999px;letter-spacing:0.4px;">💎 1-PAGE ZERO-SCROLL OS</span>
<span style="font-size:15px;font-weight:900;color:#f8fafc;">🗝️ 타겟 캐비닛: <span style="color:#38bdf8;">[{active_prof['nid']}] {active_prof['title']}</span></span>
<span style="background:rgba(16,185,129,0.16);border:1px solid rgba(16,185,129,0.45);color:#6ee7b7;font-size:11px;font-weight:800;padding:2px 9px;border-radius:999px;">기초 {round(active_prof['base_amt']/100000000,1)}억 · 하한 {active_prof['low_rate']:.3f}%</span>
</div>
<div style="display:flex;align-items:center;gap:12px;">
<span style="font-size:12px;font-weight:800;color:#fde68a;">🛍️ 보물 카트 {len(cart_profs)}건 담김 (합산 기대수익 +약 {profit_eok}억 원)</span>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # 2. 5대 독립 작업 캐비닛 네비게이터 (클릭 즉시 한 화면 안에서 자연스럽게 전환)
    m_c1, m_c2, m_c3, m_c4, m_c5 = st.columns(5)
    cur_m = st.session_state["_os_active_menu"]

    if m_c1.button(
        "🎛️ [1] 스마트 검색·필터 금고",
        key="os_btn_m1",
        type="primary" if cur_m == "M1_FILTER" else "secondary",
        use_container_width=True,
    ):
        st.session_state["_os_active_menu"] = "M1_FILTER"
        st.rerun()

    if m_c2.button(
        f"🛍️ [2] 보물섬 공고 쇼룸 ({len(live_bids)}건)",
        key="os_btn_m2",
        type="primary" if cur_m == "M2_SHOWROOM" else "secondary",
        use_container_width=True,
    ):
        st.session_state["_os_active_menu"] = "M2_SHOWROOM"
        st.rerun()

    if m_c3.button(
        "👑 [3] 단일 AI 모델 집중 실행실",
        key="os_btn_m3",
        type="primary" if cur_m == "M3_SINGLE_MODEL" else "secondary",
        use_container_width=True,
    ):
        st.session_state["_os_active_menu"] = "M3_SINGLE_MODEL"
        st.rerun()

    if m_c4.button(
        "📂 [4] 프라이빗 문서·시방서 볼트",
        key="os_btn_m4",
        type="primary" if cur_m == "M4_DOC_VAULT" else "secondary",
        use_container_width=True,
    ):
        st.session_state["_os_active_menu"] = "M4_DOC_VAULT"
        st.rerun()

    if m_c5.button(
        "🏆 [5] 나의 보물 카트 & 결재 패키지",
        key="os_btn_m5",
        type="primary" if cur_m == "M5_CART_SUMMARY" else "secondary",
        use_container_width=True,
    ):
        st.session_state["_os_active_menu"] = "M5_CART_SUMMARY"
        st.rerun()

    # =========================================================================
    # MENU 1: 🎛️ 스마트 검색·필터 금고 (평소에는 숨겨져 있다가 선택 시에만 단독 오픈)
    # =========================================================================
    if cur_m == "M1_FILTER":
        st.markdown('<div class="os-stage-viewport os-cabinet-frame">', unsafe_allow_html=True)
        st.markdown(
            """
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(56,189,248,0.25);">
<span style="font-size:17px;font-weight:900;color:#f8fafc;">🎛️ [CABINET 01] 나라장터 5차원 인크리멘탈 레이더 & 기업 스펙 금고</span>
<span style="background:rgba(56,189,248,0.16);border:1px solid #38bdf8;color:#7dd3fc;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;">조건 변경 후 [보물섬 쇼룸 열기] 클릭</span>
</div>
""",
            unsafe_allow_html=True,
        )
        f_col1, f_col2 = st.columns([1.4, 2.0])
        with f_col1:
            q_comp = st.text_input(
                "🏢 1-Click 기업명·대표자 초성 퀵 체인지",
                value=st.session_state.get("_os_q_comp", ""),
                placeholder="예: '선', '태양', 'ㄱㅇ', '강원' 입력 시 실적 즉시 동기화",
                key="_os_q_comp_input",
            )
            st.session_state["_os_q_comp"] = q_comp
        with f_col2:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.session_state["_os_f_lic"] = st.selectbox(
                    "1️⃣ 보유 공종 및 면허",
                    ["건축공사업", "토목건축공사업", "실내건축공사업", "전체 면허"],
                    index=0,
                    key="_os_sb_lic",
                )
            with c2:
                st.session_state["_os_f_reg"] = st.selectbox(
                    "2️⃣ 관할 지역제한",
                    ["강원특별자치도", "서울·수도권", "전국 발주", "전체 지역"],
                    index=0,
                    key="_os_sb_reg",
                )
            with c3:
                st.session_state["_os_f_scale"] = st.selectbox(
                    "3️⃣ 공사 추정금액 규모",
                    ["전체 규모", "30억 ~ 50억 미만", "50억 ~ 100억 미만", "100억 이상 중대형"],
                    index=0,
                    key="_os_sb_scale",
                )

        st.markdown(
            f"""
<div style="background:rgba(15,23,42,0.9);border:1px solid rgba(16,185,129,0.4);border-left:4px solid #10b981;border-radius:12px;padding:12px 16px;margin-top:8px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
<span style="font-size:13px;font-weight:800;color:#e2e8f0;">📡 <b>현재 레이더 포착 공고:</b> [{st.session_state['_os_f_lic']} · {st.session_state['_os_f_reg']} · {st.session_state['_os_f_scale']}] 총 <b style="color:#34d399;font-size:15px;">{len(live_bids)}건</b> 실시간 매칭 완료</span>
<span style="font-size:11.5px;color:#fde68a;font-weight:800;">⚡ M5 · EGR · LATTICE 3대 엔진 동시 대기중</span>
</div>
""",
            unsafe_allow_html=True,
        )
        if st.button("✨ 조건 적용 완료 ➔ [2] 보물섬 공고 쇼룸 캐비닛 즉시 열기", key="os_go_showroom_btn", type="primary", use_container_width=True):
            st.session_state["_os_active_menu"] = "M2_SHOWROOM"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # MENU 2: 🛍️ 보물섬 공고 쇼룸 (한 화면에 딱 3건만 보여주는 무스크롤 쇼케이스)
    # =========================================================================
    elif cur_m == "M2_SHOWROOM":
        st.markdown('<div class="os-stage-viewport">', unsafe_allow_html=True)
        page_size = 3
        total_pages = max(1, (len(live_bids) + page_size - 1) // page_size)
        cur_page = min(st.session_state["_zs_page"], total_pages - 1)
        start_i = cur_page * page_size
        end_i = min(len(live_bids), start_i + page_size)

        p_c1, p_c2, p_c3 = st.columns([1.1, 2.8, 1.1])
        with p_c1:
            if st.button("◀ 이전 3건 쇼케이스", key="os_prev_p", disabled=(cur_page <= 0), use_container_width=True):
                st.session_state["_zs_page"] = max(0, cur_page - 1)
                st.rerun()
        with p_c2:
            st.markdown(
                f"<div style='text-align:center;padding:6px;background:rgba(15,23,42,0.85);border:1px solid rgba(251,191,36,0.35);border-radius:10px;font-size:13px;font-weight:900;color:#fde68a;'>💎 TREASURE SHOWCASE — PAGE {cur_page+1} / {total_pages} &nbsp;(공고 #{start_i+1} ~ #{end_i} / 총 {len(live_bids)}건)</div>",
                unsafe_allow_html=True,
            )
        with p_c3:
            if st.button("다음 3건 쇼케이스 ▶", key="os_next_p", disabled=(cur_page >= total_pages - 1), use_container_width=True):
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
                    b1, b2, b3 = st.columns([1.35, 1.25, 0.85])
                    if b1.button("👑 AI 모델실행", key=f"os_run_m_{g_idx}", type="primary", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["selected_notice"] = gn
                        st.session_state["auto_base_amt"] = gprof["base_amt"]
                        st.session_state["auto_a_val"] = gprof["a_val"]
                        st.session_state["auto_low_rate"] = gprof["low_rate"]
                        st.session_state["_os_active_menu"] = "M3_SINGLE_MODEL"
                        st.rerun()
                    if b2.button("📂 문서볼트", key=f"os_open_v_{g_idx}", use_container_width=True):
                        st.session_state["_boutique_selected_idx"] = g_idx
                        st.session_state["_os_active_menu"] = "M4_DOC_VAULT"
                        st.rerun()
                    if b3.button("💖" if not in_cart else "🗑️", key=f"os_cart_{g_idx}", use_container_width=True):
                        if in_cart:
                            st.session_state["_boutique_cart_ids"].remove(gprof["nid"])
                        else:
                            st.session_state["_boutique_cart_ids"].append(gprof["nid"])
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # MENU 3: 👑 단일 AI 모델 집중 실행실 (1-Page 1-Model)
    # =========================================================================
    elif cur_m == "M3_SINGLE_MODEL":
        st.markdown('<div class="os-stage-viewport">', unsafe_allow_html=True)
        top_m1, top_m2, top_m3 = st.columns([1.3, 2.2, 1.1])
        with top_m1:
            notice_labels = [f"#{i+1:02d} [{analyze_construction_profile(x, i)['nid']}] {analyze_construction_profile(x, i)['title'][:14]}" for i, x in enumerate(live_bids)]
            picked_label = st.selectbox(
                "🗝️ 분석할 타겟 공고 즉시 변경",
                notice_labels,
                index=sel_idx,
                key="_os_model_notice_picker",
            )
            new_sel = notice_labels.index(picked_label)
            if new_sel != sel_idx:
                st.session_state["_boutique_selected_idx"] = new_sel
                st.rerun()
        with top_m2:
            chosen_model = st.radio(
                "🔬 단독 가동할 AI 사정 모델 선택 (한 화면 1개 모델 집중 조명)",
                [
                    "👑 [MODEL 1] M5 양자코어",
                    "🛡️ [MODEL 2] EGR-BID 강건방어",
                    "⚡ [MODEL 3] LATTICE-1365 격자",
                ],
                horizontal=True,
                key="_os_single_model_radio",
            )
        with top_m3:
            st.write("")
            if st.button("📂 이 공고 문서·시방서 열람 ▶", key="os_to_doc_from_m", use_container_width=True):
                st.session_state["_os_active_menu"] = "M4_DOC_VAULT"
                st.rerun()

        st.markdown(build_single_model_spotlight_html(active_prof, chosen_model), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # MENU 4: 📂 프라이빗 문서·시방서 볼트 (1-Page 1-Document)
    # =========================================================================
    elif cur_m == "M4_DOC_VAULT":
        st.markdown('<div class="os-stage-viewport">', unsafe_allow_html=True)
        doc_html, boq_csv, bid_json, spec_txt = generate_notice_attachments(active_prof)
        zip_bytes, zip_meta = generate_master_zip_bundle(active_prof)

        v_c1, v_c2 = st.columns([2.1, 1.4])
        with v_c1:
            doc_choice = st.radio(
                "📑 단일 화면에 펼칠 규격 양식서 선택",
                [
                    "🏗️ [1] 현장 종합 브리핑 도감",
                    "📐 [2] 공사시방서 & AI 전략 규격서",
                    "📊 [3] 표준 공내역서(BoQ) 테이블",
                    "🔐 [4] SHA-256 무결성 검증서",
                ],
                horizontal=True,
                key="_os_single_doc_choice",
            )
        with v_c2:
            st.download_button(
                label=f"📦 [1-Click 마스터 번들 ZIP] ({active_prof['nid']}.zip · {zip_meta['zip_size_kb']} KB)",
                data=zip_bytes,
                file_name=f"G2B_마스터패키지_{active_prof['nid']}.zip",
                mime="application/zip",
                key=f"os_dl_zip_{active_prof['nid']}",
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
        d1.download_button("📄 입찰공고문 (.html)", data=doc_html, file_name=f"입찰공고문_{active_prof['nid']}.html", mime="text/html", key="os_d1", use_container_width=True)
        d2.download_button("📊 공내역서 (.csv)", data=boq_csv, file_name=f"공내역서_{active_prof['nid']}.csv", mime="text/csv", key="os_d2", use_container_width=True)
        d3.download_button("📦 G2B 제원 (.json)", data=bid_json, file_name=f"G2B제원_{active_prof['nid']}.json", mime="application/json", key="os_d3", use_container_width=True)
        d4.download_button("📐 공사시방서 (.txt)", data=spec_txt, file_name=f"공사시방서_{active_prof['nid']}.txt", mime="text/plain", key="os_d4", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # MENU 5: 🏆 나의 보물 카트 & 결재 패키지 (쇼핑몰 장바구니 최종 체크아웃 화면)
    # =========================================================================
    elif cur_m == "M5_CART_SUMMARY":
        st.markdown('<div class="os-stage-viewport os-cabinet-frame">', unsafe_allow_html=True)
        rows_html = ""
        for idx_c, cp in enumerate(cart_profs, start=1):
            est_p = cp["bid_m5"] - cp["est_net_cost"]
            rows_html += f"""
<tr style="border-bottom:1px solid rgba(51,65,85,0.65);">
<td style="padding:10px 12px;font-weight:900;color:#fbbf24;">#0{idx_c}</td>
<td style="padding:10px 12px;font-weight:800;color:#7dd3fc;">{cp['nid']}</td>
<td style="padding:10px 12px;font-weight:900;color:#f8fafc;">{cp['title']}</td>
<td style="padding:10px 12px;text-align:right;font-weight:800;color:#e2e8f0;">{cp['base_amt']:,}원</td>
<td style="padding:10px 12px;text-align:right;font-weight:900;color:#38bdf8;">{cp['bid_m5']:,}원</td>
<td style="padding:10px 12px;text-align:right;font-weight:900;color:#34d399;">+{est_p:,}원</td>
<td style="padding:10px 12px;text-align:center;"><span style="background:rgba(56,189,248,0.18);border:1px solid #38bdf8;color:#bae6fd;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:900;">2번 + 12번</span></td>
</tr>"""

        if not rows_html:
            rows_html = '<tr><td colspan="7" style="padding:20px;text-align:center;color:#94a3b8;font-weight:800;">아직 카트에 담긴 보물 공고가 없습니다. [2] 보물섬 공고 쇼룸에서 💖 버튼을 눌러 담아주세요.</td></tr>'

        cart_table_html = f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid rgba(251,191,36,0.35);">
<span style="font-size:17px;font-weight:900;color:#f8fafc;">🏆 [CABINET 05] 나의 보물 공고 포트폴리오 & 최종 투찰 체크아웃 ({len(cart_profs)}건)</span>
<span style="background:rgba(16,185,129,0.18);border:1px solid #10b981;color:#34d399;font-size:12px;font-weight:900;padding:3px 12px;border-radius:999px;">포트폴리오 합산 기대수익: +{total_cart_profit:,}원 (약 {profit_eok}억 원)</span>
</div>
<table style="width:100%;border-collapse:collapse;font-size:12.5px;text-align:left;">
<thead>
<tr style="background:rgba(15,23,42,0.95);border-bottom:2px solid #fbbf24;color:#94a3b8;font-size:11.5px;">
<th style="padding:9px 12px;">순번</th>
<th style="padding:9px 12px;">공고번호</th>
<th style="padding:9px 12px;">보물 공고명</th>
<th style="padding:9px 12px;text-align:right;">기초금액</th>
<th style="padding:9px 12px;text-align:right;">👑 M5 추천 투찰가</th>
<th style="padding:9px 12px;text-align:right;">예상 순이익</th>
<th style="padding:9px 12px;text-align:center;">추천 2픽</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
"""
        st.markdown("\n".join(l.lstrip() for l in cart_table_html.splitlines() if l.strip()), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
