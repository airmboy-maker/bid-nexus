import streamlit as st

DECK_ZONES = [
    "📡 [Z1] 나라장터 공고 쇼룸 & 필터 (tab_radar)",
    "🎯 [Z2] 핵심 적격심사 & 산출물 (tab1)",
    "⚡ [Z3] 4차원 입체 추론 15C4 매핑 (tab_quantum_ai)",
    "🎛️ [Z4] 0.001% 초미세 감도 시뮬레이터 (tab_sim)",
    "🔥 [Z5] 5대 모델 해부 · 3D 홀로그램 · 7-BAY (tab4)",
    "🛡️ [Z6] 번외 1·2: EGR-BID(M6~M8) & LATTICE(L0~L5)",
    "📑 [Z7] 적격 증빙서류 일람표 & 통합 출력 (tab_dox)",
    "🏢 [Z8] 기업 마스터 스펙 & 기술자 관리 (tab_profile)",
]


def _set_zone_state(z_val: str) -> None:
    st.session_state["_ndc_zone"] = z_val


def render_master_mode_and_zone_selector() -> tuple:
    if "_ndc_mode" not in st.session_state:
        st.session_state["_ndc_mode"] = "💎 1-Page 캐비닛 집중 모드 (무스크롤)"
    if "_ndc_zone" not in st.session_state or st.session_state["_ndc_zone"] not in DECK_ZONES:
        st.session_state["_ndc_zone"] = DECK_ZONES[0]

    with st.sidebar:
        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.22),rgba(15,23,42,0.96));border:1.5px solid #fbbf24;border-radius:10px;padding:8px 11px;margin-top:2px;margin-bottom:6px;box-shadow:0 6px 18px rgba(0,0,0,0.5);">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:11px;font-weight:900;color:#fde68a;">💎 SCREEN MODE SWITCH</span>
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">EXACT BIND</span>
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
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗄️ 8대 전용 페이지 즉시 교체</div>
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

    return is_cabinet_mode, zone


def render_top_cabinet_switcher_bar(is_cabinet_mode: bool, current_zone: str) -> None:
    if not is_cabinet_mode:
        return

    # Z1이 아닐 때는 상단 '기업 적격심사 마스터 스펙' 및 '마감 D-5 4칸 요약 배너'도 숨겨서 선택한 메뉴가 화면 최상단에 바로 뜨도록 CSS 제어
    hide_top_summary_css = ""
    if "[Z1]" not in current_zone:
        hide_top_summary_css = """
        div[data-testid="stVerticalBlock"]:has(> div > #ndc-top-summary-marker) {
            display: none !important;
        }
        """

    st.markdown(
        f"""
<style>
.block-container {{
    padding-top: 0.9rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 1580px !important;
}}
/* 선택되지 않은 숨김 구역(ndc-hidden-zone-marker를 가진 컨테이너)을 화면에서 100% 제거하여 스크롤 원천 차단 */
div[data-testid="stVerticalBlock"]:has(> div > #ndc-hidden-zone-marker),
div[data-testid="stVerticalBlock"]:has(> div > div > #ndc-hidden-zone-marker) {{
    display: none !important;
    height: 0px !important;
    max-height: 0px !important;
    overflow: hidden !important;
    margin: 0px !important;
    padding: 0px !important;
}}
{hide_top_summary_css}
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
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;">💎 1-PAGE NATIVE SWAP</span>
<span style="font-size:14px;font-weight:900;color:#f8fafc;">현재 열린 단독 캐비닛: <span style="color:#38bdf8;">{current_zone}</span></span>
</div>
<div style="font-size:11.5px;color:#fde68a;font-weight:800;">
⚡ 아래 8개 버튼 클릭 시 선택한 1개 구역만 즉시 화면에 나타나며 나머지 7개 구역은 숨겨집니다
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    short_names = [
        "📡 Z1: 공고쇼룸",
        "🎯 Z2: 적격·산출물",
        "⚡ Z3: 4차원추론",
        "🎛️ Z4: 0.001%감도",
        "🔥 Z5: 5대모델·3D",
        "🛡️ Z6: 번외EGR·격자",
        "📑 Z7: 증빙서류",
        "🏢 Z8: 기업마스터",
    ]
    cols = st.columns(8)
    for i, z_full in enumerate(DECK_ZONES):
        cols[i].button(
            short_names[i],
            key=f"top_z8_btn_{i}",
            type="primary" if z_full == current_zone else "secondary",
            use_container_width=True,
            on_click=_set_zone_state,
            args=(z_full,),
        )


def make_zone_container(is_cabinet_mode: bool, current_zone: str, target_tag: str):
    """
    현재 선택된 구역(target_tag, 예: '[Z4]')이면 화면에 보이는 st.container()를 반환하고,
    선택되지 않은 구역이면 CSS로 100% 숨겨지는(display:none) 숨김 컨테이너를 반환!
    """
    c = st.container()
    if is_cabinet_mode and (target_tag not in current_zone):
        with c:
            st.markdown('<div id="ndc-hidden-zone-marker" style="display:none;"></div>', unsafe_allow_html=True)
    return c


def route_7_main_tabs(tab_labels: list, is_cabinet_mode: bool, current_zone: str):
    """
    line 1793의 `tab_radar, tab1, tab_quantum_ai, tab_sim, tab_dox, tab_profile, tab4 = st.tabs([...])`를 대체!
    - 기존 통합 스크롤 모드일 때: 원래의 st.tabs(tab_labels) 7개 탭 그대로 반환
    - 1-Page 캐비닛 집중 모드일 때: 각 탭 변수에 `make_zone_container`를 매핑하여
      탭 바를 거치지 않고 내가 선택한 Z1~Z8 구역만 화면 최상단에 단독 표시!
    """
    if not is_cabinet_mode:
        return st.tabs(tab_labels)

    c_radar = make_zone_container(is_cabinet_mode, current_zone, "[Z1]")
    c_tab1 = make_zone_container(is_cabinet_mode, current_zone, "[Z2]")
    c_q_ai = make_zone_container(is_cabinet_mode, current_zone, "[Z3]")
    c_sim = make_zone_container(is_cabinet_mode, current_zone, "[Z4]")
    c_dox = make_zone_container(is_cabinet_mode, current_zone, "[Z7]")
    c_prof = make_zone_container(is_cabinet_mode, current_zone, "[Z8]")
    c_tab4 = make_zone_container(is_cabinet_mode, current_zone, "[Z5]")

    return c_radar, c_tab1, c_q_ai, c_sim, c_dox, c_prof, c_tab4
