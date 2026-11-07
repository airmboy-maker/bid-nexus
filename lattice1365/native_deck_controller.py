import streamlit as st
import streamlit.components.v1 as components

DECK_ZONES = [
    "📡 [Z1] 나라장터 공고 쇼룸 (1페이지 3건)",
    "🎯 [Z2] 핵심 적격심사 & 산출물 (tab1)",
    "⚡ [Z3] 4차원 입체 추론 15C4 매핑 (tab_quantum_ai)",
    "🎛️ [Z4] 0.001% 초미세 감도 시뮬레이터 (tab_sim)",
    "🔥 [Z5] 5대 모델 해부 & 3D 홀로그램 (tab4 상단)",
    "🏛️ [Z6] 7-BAY 전술 머신 & 4D 조감도 (tab4 하단)",
    "🛡️ [Z7] 번외 1·2: EGR-BID(M6~M8) & LATTICE(L0~L5)",
    "📑 [Z8] 적격 증빙서류 일람표 & 통합 출력 (tab_dox)",
    "🏢 [Z9] 기업 마스터 스펙 & 기술자 관리 (tab_profile)",
]


def _set_zone_state(z_val: str) -> None:
    st.session_state["_ndc_zone"] = z_val
    st.session_state["_ndc_scroll_trig"] = st.session_state.get("_ndc_scroll_trig", 0) + 1


def make_zone_box(is_cabinet_mode: bool, current_zone: str, *tags: str):
    """
    파이썬 변수(q_auto 등)가 절대 누락되지 않도록 코드는 실행하되,
    현재 선택된 구역(tags)이 아니면 컨테이너 내부에 '.ndc-kill-zone' 마커를 심어
    DOM 래퍼 깊이(depth)와 무관하게 화면에서 100% 즉시 숨김(display: none)!
    """
    c = st.container()
    if is_cabinet_mode and not any(t in current_zone for t in tags):
        with c:
            st.markdown('<span class="ndc-kill-zone" style="display:none;"></span>', unsafe_allow_html=True)
    return c


def route_7_main_tabs(tab_labels: list, is_cabinet_mode: bool, current_zone: str):
    if not is_cabinet_mode:
        return st.tabs(tab_labels)

    c_radar = make_zone_box(is_cabinet_mode, current_zone, "[Z1]")
    c_tab1 = make_zone_box(is_cabinet_mode, current_zone, "[Z2]")
    c_q_ai = make_zone_box(is_cabinet_mode, current_zone, "[Z3]")
    c_sim = make_zone_box(is_cabinet_mode, current_zone, "[Z4]")
    c_dox = make_zone_box(is_cabinet_mode, current_zone, "[Z8]")
    c_prof = make_zone_box(is_cabinet_mode, current_zone, "[Z9]")
    c_tab4 = make_zone_box(is_cabinet_mode, current_zone, "[Z5]", "[Z6]")

    return c_radar, c_tab1, c_q_ai, c_sim, c_dox, c_prof, c_tab4


def render_master_mode_and_zone_selector() -> tuple:
    if "_ndc_mode" not in st.session_state:
        st.session_state["_ndc_mode"] = "💎 1-Page 캐비닛 집중 모드 (무스크롤)"
    if "_ndc_zone" not in st.session_state or st.session_state["_ndc_zone"] not in DECK_ZONES:
        st.session_state["_ndc_zone"] = DECK_ZONES[0]

    # 사이드바 4D 하이엔드 UI CSS 항상 주입 (옛 버전 회귀 방지!)
    try:
        import lattice1365.sidebar_4d_ui as _s4d
        st.markdown(_s4d.get_sidebar_4d_global_css(), unsafe_allow_html=True)
    except Exception:
        pass

    with st.sidebar:
        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.22),rgba(15,23,42,0.96));border:1.5px solid #fbbf24;border-radius:10px;padding:8px 11px;margin-top:2px;margin-bottom:6px;box-shadow:0 6px 18px rgba(0,0,0,0.5);">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:11px;font-weight:900;color:#fde68a;">💎 SCREEN MODE SWITCH</span>
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">v3.0 BOUTIQUE</span>
</div>
<div style="font-size:9.5px;color:#cbd5e1;font-weight:700;margin-top:2px;">1-Page 구역 교체 vs 기존 통합 스크롤</div>
</div>
""",
            unsafe_allow_html=True,
        )
        mode = st.radio(
            "글로벌 화면 작동 모드",
            [
                "💎 1-Page 캐비닛 집중 모드 (무스크롤)",
                "🌌 기존 통합 스크롤 모드 (v20.4 전체 펼침)",
            ],
            key="_ndc_mode",
            label_visibility="collapsed",
        )

        is_cabinet_mode = ("1-Page" in mode)

        if is_cabinet_mode:
            st.markdown(
                """
<div style="background:rgba(56,189,248,0.14);border:1px solid rgba(56,189,248,0.45);border-left:3.5px solid #38bdf8;border-radius:8px;padding:6px 10px;margin-top:4px;margin-bottom:4px;">
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗄️ 9대 독립 캐비닛 즉시 교체</div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:700;">클릭 즉시 해당 구역만 화면에 표시됩니다</div>
</div>
""",
                unsafe_allow_html=True,
            )
            zone = st.radio(
                "집중할 캐비닛 구역 선택",
                DECK_ZONES,
                key="_ndc_zone",
                label_visibility="collapsed",
            )
        else:
            zone = "ALL"

        # 사이드바 하단 4D 양자 테서랙트 홀로그램 & 라이브 텔레메트리 항상 표시
        try:
            import lattice1365.sidebar_4d_ui as _s4d
            components.html(_s4d.build_sidebar_4d_tesseract_html(4), height=230, scrolling=False)
        except Exception:
            pass

    return is_cabinet_mode, zone


def render_top_cabinet_switcher_bar(is_cabinet_mode: bool, current_zone: str) -> None:
    if not is_cabinet_mode:
        return

    # 핵심: 직계 자식(>)을 쓰지 않고, 직속 stVerticalBlock 중 내부에 .ndc-kill-zone을 직접 포함한 블록만 정확히 display:none 처리!
    # (상위 부모 블록까지 숨겨지지 않도록 `:not(:has(div[data-testid="stVerticalBlock"] .ndc-kill-zone))` 조건으로 가장 안쪽 컨테이너만 정확히 타격!)
    st.markdown(
        f"""
<style>
.block-container {{
    padding-top: 0.8rem !important;
    padding-bottom: 0.4rem !important;
    max-width: 1580px !important;
}}
div[data-testid="stVerticalBlock"]:has(.ndc-kill-zone):not(:has(div[data-testid="stVerticalBlock"] .ndc-kill-zone)) {{
    display: none !important;
    height: 0px !important;
    max-height: 0px !important;
    overflow: hidden !important;
    margin: 0px !important;
    padding: 0px !important;
}}
.cabinet-focus-ribbon {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    background: linear-gradient(90deg, #070b14 0%, #0f172a 50%, #070b14 100%);
    border: 1.5px solid #fbbf24;
    border-left: 5px solid #f59e0b;
    border-radius: 13px;
    padding: 8px 16px;
    margin-bottom: 8px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.7);
}}
</style>
<div class="cabinet-focus-ribbon">
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;">💎 1-PAGE CABINET FOCUS</span>
<span style="font-size:14px;font-weight:900;color:#f8fafc;">현재 열린 단독 캐비닛: <span style="color:#38bdf8;">{current_zone}</span></span>
</div>
<div style="font-size:11.5px;color:#6ee7b7;font-weight:800;">
✨ 모든 공통 변수(q_auto 등) 무결성 100% 유지 + 비활성 구역 화면 자동 숨김
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    short_names = [
        "📡 Z1:쇼룸",
        "🎯 Z2:적격",
        "⚡ Z3:4D추론",
        "🎛️ Z4:감도",
        "🔥 Z5:5대모델",
        "🏛️ Z6:7-BAY",
        "🛡️ Z7:번외EGR·격자",
        "📑 Z8:증빙서류",
        "🏢 Z9:기업마스터",
    ]
    cols = st.columns(9)
    for i, z_full in enumerate(DECK_ZONES):
        cols[i].button(
            short_names[i],
            key=f"top_z9_btn_{i}",
            type="primary" if z_full == current_zone else "secondary",
            use_container_width=True,
            on_click=_set_zone_state,
            args=(z_full,),
        )

    trig = st.session_state.get("_ndc_scroll_trig", 0)
    components.html(
        f"""
<script>
// trigger={trig} ({current_zone})
(function() {{
    try {{
        const pWin = window.parent;
        const pDoc = window.parent.document;
        pWin.scrollTo({{ top: 0, behavior: 'instant' }});
        const mainSec = pDoc.querySelector('section.main');
        if (mainSec) mainSec.scrollTo({{ top: 0, behavior: 'instant' }});
        const appView = pDoc.querySelector('[data-testid="stAppViewContainer"]');
        if (appView) appView.scrollTo({{ top: 0, behavior: 'instant' }});
    }} catch (e) {{}}
}})();
</script>
""",
        height=0,
        scrolling=False,
    )
