import streamlit as st

DECK_ZONES = [
    "📡 [Z1] 나라장터 공고 쇼룸 (3건)",
    "🎯 [Z2] 적격심사 & 5대 모델·3D 홀로그램",
    "⚡ [Z3] 4차원 입체 추론 (15C4)",
    "🎛️ [Z4] 0.001% 감도 시뮬레이터",
    "🔥 [Z5] 5대 모델 해부 & 3D 홀로그램 집중뷰",
    "🏛️ [Z6] 7-BAY 전술 머신 & 4D 조감도",
    "🛡️ [Z7] 번외 1·2: EGR-BID & LATTICE",
    "📑 [Z8] 적격 증빙서류 & 통합 출력",
    "🏢 [Z9] 기업 마스터 스펙 & 투찰원장",
]


def _set_zone_state(z_val: str) -> None:
    st.session_state["_ndc_zone"] = z_val


def make_zone_box(is_cabinet_mode: bool, current_zone: str, *tags: str):
    """
    닫힌 expander(_ndc_hidden_vault_)를 쓰지 않고 100% 순정 st.container()를 사용하여
    좌측 사이드바(AI ENGINE LAB / TELEMETRY)와 내부 3D 홀로그램이 절대 누락되지 않게 보장!
    비활성 구역일 때만 직속 마크다운 자식 span.ndc-hide-me 를 심어 표준 CSS로 정확히 해당 컨테이너만 숨김!
    """
    c = st.container()
    if is_cabinet_mode and not any(t in current_zone for t in tags):
        with c:
            st.markdown('<span class="ndc-hide-me" style="display:none;"></span>', unsafe_allow_html=True)
    return c


def route_7_main_tabs(tab_labels: list, is_cabinet_mode: bool, current_zone: str):
    if not is_cabinet_mode:
        return st.tabs(tab_labels)

    # [핵심]: 5대 모델(레거시~AI앙상블) + 표준 사정 명세표 + KP-01~03 3D 60FPS 홀로그램 링은 `tab1` 안에 들어있으므로,
    # [Z2]와 [Z5] 어느 쪽을 눌러도 `c_tab1`이 즉시 화면에 열리도록 연결!
    # 그리고 `tab4`(투찰원장 & 7-BAY 조감도)는 [Z6] 및 [Z9]에서 열리도록 정확히 배정!
    c_radar = make_zone_box(is_cabinet_mode, current_zone, "[Z1]")
    c_tab1 = make_zone_box(is_cabinet_mode, current_zone, "[Z2]", "[Z5]")
    c_q_ai = make_zone_box(is_cabinet_mode, current_zone, "[Z3]")
    c_sim = make_zone_box(is_cabinet_mode, current_zone, "[Z4]")
    c_dox = make_zone_box(is_cabinet_mode, current_zone, "[Z8]")
    c_prof = make_zone_box(is_cabinet_mode, current_zone, "[Z9]")
    c_tab4 = make_zone_box(is_cabinet_mode, current_zone, "[Z6]", "[Z9]")

    return c_radar, c_tab1, c_q_ai, c_sim, c_dox, c_prof, c_tab4


def get_sidebar_spacing_override_css() -> str:
    return """
<style>
html body section[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    gap: 7px !important;
    margin-top: 6px !important;
    margin-bottom: 10px !important;
    padding: 2px 2px !important;
}

html body section[data-testid="stSidebar"] div[role="radiogroup"] > label,
html body section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.88) 0%, rgba(9, 14, 28, 0.95) 100%) !important;
    border: 1px solid rgba(71, 85, 105, 0.55) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin: 0px !important;
    min-height: 38px !important;
    display: flex !important;
    align-items: center !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.38) !important;
    transition: all 0.18s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

html body section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
html body section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    border-color: rgba(56, 189, 248, 0.75) !important;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%) !important;
    transform: translateX(3px) !important;
}

html body section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked),
html body section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.22) 0%, rgba(15, 23, 42, 0.98) 100%) !important;
    border: 1.5px solid #38bdf8 !important;
    box-shadow: 0 4px 14px rgba(56, 189, 248, 0.28), inset 0 0 8px rgba(56, 189, 248, 0.12) !important;
}

html body section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    margin-right: 8px !important;
}

html body section[data-testid="stSidebar"] div[role="radiogroup"] > label p,
html body section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] p {
    font-size: 12.2px !important;
    font-weight: 800 !important;
    line-height: 1.45 !important;
    letter-spacing: -0.15px !important;
    color: #e2e8f0 !important;
    margin: 0px !important;
    white-space: nowrap !important;
}

html body section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #fef08a !important;
    font-weight: 900 !important;
}
</style>
"""


def render_master_mode_and_zone_selector() -> tuple:
    if "_ndc_mode" not in st.session_state:
        st.session_state["_ndc_mode"] = "💎 1-Page 캐비닛 집중 모드 (무스크롤)"
    if "_ndc_zone" not in st.session_state or st.session_state["_ndc_zone"] not in DECK_ZONES:
        old_z = str(st.session_state.get("_ndc_zone", ""))
        matched = DECK_ZONES[0]
        for dz in DECK_ZONES:
            tag = dz.split("]")[0] + "]"
            if tag in old_z:
                matched = dz
                break
        st.session_state["_ndc_zone"] = matched

    with st.sidebar:
        st.markdown(get_sidebar_spacing_override_css(), unsafe_allow_html=True)

        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.20),rgba(15,23,42,0.96));border:1.5px solid #fbbf24;border-radius:12px;padding:12px 14px;margin-top:8px;margin-bottom:10px;box-shadow:0 6px 18px rgba(0,0,0,0.45);">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="font-size:11.5px;font-weight:900;color:#fde68a;letter-spacing:0.3px;">💎 SCREEN MODE SWITCH</span>
<span style="background:#fbbf24;color:#020617;font-size:9px;font-weight:900;padding:2px 8px;border-radius:999px;">v3.0 BOUTIQUE</span>
</div>
<div style="font-size:10.5px;color:#cbd5e1;font-weight:700;line-height:1.4;">1-Page 구역 교체 vs 기존 통합 스크롤</div>
</div>
""",
            unsafe_allow_html=True,
        )
        mode = st.radio(
            "글로벌 화면 작동 모드",
            [
                "💎 1-Page 캐비닛 집중 모드 (무스크롤)",
                "🌌 기존 통합 스크롤 모드 (전체 펼침)",
            ],
            key="_ndc_mode",
            label_visibility="collapsed",
        )

        is_cabinet_mode = ("1-Page" in mode)

        if is_cabinet_mode:
            st.markdown(
                """
<div style="background:linear-gradient(135deg,rgba(14,165,233,0.18),rgba(15,23,42,0.95));border:1.5px solid rgba(56,189,248,0.55);border-left:4px solid #38bdf8;border-radius:12px;padding:11px 14px;margin-top:14px;margin-bottom:10px;box-shadow:0 6px 16px rgba(0,0,0,0.4);">
<div style="font-size:11.5px;font-weight:900;color:#7dd3fc;margin-bottom:4px;">🗄️ 9대 독립 캐비닛 즉시 교체</div>
<div style="font-size:10px;color:#94a3b8;font-weight:700;line-height:1.4;">클릭 즉시 해당 구역만 단독 표시됩니다</div>
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
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        else:
            zone = "ALL"

    return is_cabinet_mode, zone


def render_top_cabinet_switcher_bar(is_cabinet_mode: bool, current_zone: str) -> None:
    if not is_cabinet_mode:
        return

    st.markdown(get_sidebar_spacing_override_css(), unsafe_allow_html=True)

    # [표준 W3C CSS 선택자]
    # 비표준 :contains() 를 제거하고, 자신의 첫 번째 직속 자식(> div:first-child)에 span.ndc-hide-me 마커를 가진 stVerticalBlock만 정확히 display:none 처리!
    st.markdown(
        f"""
<style>
.block-container {{
    padding-top: 2.3rem !important;
    padding-bottom: 0.6rem !important;
    max-width: 1580px !important;
}}
header[data-testid="stHeader"] {{
    background: transparent !important;
}}
div[data-testid="stVerticalBlock"]:has(> div:first-child span.ndc-hide-me) {{
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
✨ 5대 모델 해부 · 3D 60FPS 홀로그램 링(KP-01~03) · 좌측 AI ENGINE LAB 100% 활성 상태
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    short_names = [
        "📡 Z1:쇼룸",
        "🎯 Z2:적격·모델",
        "⚡ Z3:4D추론",
        "🎛️ Z4:감도",
        "🔥 Z5:5대모델·3D",
        "🏛️ Z6:7-BAY",
        "🛡️ Z7:번외EGR·격자",
        "📑 Z8:증빙서류",
        "🏢 Z9:기업·원장",
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
