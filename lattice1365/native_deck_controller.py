import streamlit as st
import streamlit.components.v1 as components

DECK_ZONES = [
    "📡 [Z1] 나라장터 공고 쇼룸 (3건)",
    "🎯 [Z2] 핵심 적격심사 & 산출물",
    "⚡ [Z3] 5대 모델 해부 & 3D 홀로그램",
    "🎛️ [Z4] 0.001% 감도 시뮬레이터",
    "🔥 [Z5] 4D 입체 추론 & 투찰 원장",
    "🏛️ [Z6] 7-BAY 전술 머신 & 4D 조감도",
    "🛡️ [Z7] 번외 1·2: EGR-BID & LATTICE",
    "📑 [Z8] 적격 증빙서류 & 통합 출력",
    "🏢 [Z9] 기업 마스터 스펙 & OCR",
]


def _set_zone_state(z_val: str) -> None:
    st.session_state["_ndc_zone"] = z_val
    st.session_state["_ndc_scroll_trig"] = st.session_state.get("_ndc_scroll_trig", 0) + 1


def make_zone_box(is_cabinet_mode: bool, current_zone: str, *tags: str):
    """
    선택되지 않은 구역 컨테이너에만 정확히 '.ndc-kill-zone' 마커를 주입하되,
    부모 컨테이너(tab4 등)가 자식의 마커 때문에 통째로 숨겨지는 연쇄 소거 버그를 원천 차단!
    """
    c = st.container()
    if is_cabinet_mode and not any(t in current_zone for t in tags):
        with c:
            st.markdown('<span class="ndc-kill-zone" style="display:none;"></span>', unsafe_allow_html=True)
    return c


def route_7_main_tabs(tab_labels: list, is_cabinet_mode: bool, current_zone: str):
    if not is_cabinet_mode:
        return st.tabs(tab_labels)

    # [핵심 복원]
    # - tab_quantum_ai 에 들어있는 '5대 모델 해부 & KP-01~03 3D 60FPS 홀로그램 애니메이션'이 [Z3] 및 [Z5]에서 100% 표시되도록 연결!
    # - tab4 에 들어있는 '투찰 원장 + 심층 모델 + 7-BAY 조감도'가 [Z5] 및 [Z6]에서 부모 컨테이너 소거 없이 정상 표시되도록 연결!
    c_radar = make_zone_box(is_cabinet_mode, current_zone, "[Z1]")
    c_tab1 = make_zone_box(is_cabinet_mode, current_zone, "[Z2]")
    c_q_ai = make_zone_box(is_cabinet_mode, current_zone, "[Z3]", "[Z5]")
    c_sim = make_zone_box(is_cabinet_mode, current_zone, "[Z4]")
    c_dox = make_zone_box(is_cabinet_mode, current_zone, "[Z8]")
    c_prof = make_zone_box(is_cabinet_mode, current_zone, "[Z9]")
    c_tab4 = make_zone_box(is_cabinet_mode, current_zone, "[Z5]", "[Z6]")

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

    # [핵심 수정]
    # 기존 `:has(.ndc-kill-zone)` 는 부모 stVerticalBlock(예: tab4 전체)까지 숨겨버려서 내부의 그래프와 3D 홀로그램이 사라졌음!
    # 이제 `> div[data-testid="stElementContainer"]:has(.ndc-kill-zone)` 또는 `> div:has(> div > div > .ndc-kill-zone)` 처럼
    # 마커를 '직접 자식(Direct Child)'으로 가진 컨테이너만 정확히 숨겨서, 부모 탭(tab4, tab_quantum_ai)의 그래프·모델·3D 홀로그램이 100% 살아나도록 수정!
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
/* 마커(.ndc-kill-zone)를 자신의 첫 번째 직속 엘리먼트로 가진 stVerticalBlock만 정확히 숨김 (부모 블록 연쇄 소거 방지!) */
div[data-testid="stVerticalBlock"]:has(> div:first-child .ndc-kill-zone),
div[data-testid="stVerticalBlock"]:has(> div:nth-child(2) .ndc-kill-zone) {{
    display: none !important;
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
✨ 5대 모델 · 3D 60FPS 홀로그램 · 그래프 렌더링 100% 활성 상태
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    short_names = [
        "📡 Z1:쇼룸",
        "🎯 Z2:적격",
        "⚡ Z3:5대모델·3D",
        "🎛️ Z4:감도",
        "🔥 Z5:4D추론·원장",
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
