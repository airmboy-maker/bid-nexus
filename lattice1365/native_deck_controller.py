import streamlit as st
import streamlit.components.v1 as components

DECK_ZONES = [
    "📡 [Z1] 나라장터 공고 쇼룸 (1페이지 3건)",
    "🎯 [Z2] 핵심 적격심사 & 산출물 (tab1)",
    "⚡ [Z3] 4차원 입체 추론 15C4 매핑 (tab_quantum_ai)",
    "🎛️ [Z4] 0.001% 초미세 감도 시뮬레이터 (tab_sim)",
    "🔥 [Z5] 5대 모델 해부 & 3D 홀로그램 (tab4 상단)",
    "🏛️ [Z6] 7-BAY 전술 머신 & 4D 조감도 (tab4 하단)",
    "🛡️ [Z7] 번외 1: 제미나이 EGR-BID (M6·M7·M8)",
    "⚡ [Z8] 번외 2: 젠스파크 LATTICE-1365 (L0~L5)",
    "📑 [Z9] 적격 증빙서류 & 기업 마스터 스펙",
]


def _set_zone_state(z_val: str) -> None:
    st.session_state["_ndc_zone"] = z_val
    st.session_state["_ndc_scroll_trig"] = st.session_state.get("_ndc_scroll_trig", 0) + 1


def should_run_zone(is_cabinet_mode: bool, current_zone: str, *tags: str) -> bool:
    """
    기존 통합 스크롤 모드(not is_cabinet_mode)이면 무조건 True(전체 실행),
    1-Page 캐비닛 집중 모드이면 현재 선택된 구역(tags 중 하나)일 때만 True를 반환하여
    선택되지 않은 구역은 파이썬이 아예 한 줄도 실행하지 않게 차단!
    """
    if not is_cabinet_mode:
        return True
    return any(t in current_zone for t in tags)


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
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">PYTHON IF-GATE</span>
</div>
<div style="font-size:9.5px;color:#cbd5e1;font-weight:700;margin-top:2px;">파이썬 레벨 단일 구역 실행 (나머지 구역 미실행)</div>
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
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗄️ 9대 독립 페이지 즉시 교체</div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:700;">선택한 1개 구역만 파이썬에서 실행됩니다</div>
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

    st.markdown(
        f"""
<style>
.block-container {{
    padding-top: 0.8rem !important;
    padding-bottom: 0.4rem !important;
    max-width: 1580px !important;
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
<div id="ndc-top-focus-anchor"></div>
<div class="cabinet-focus-ribbon">
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;">💎 PYTHON IF-GATE ACTIVE</span>
<span style="font-size:14px;font-weight:900;color:#f8fafc;">현재 단독 실행 페이지: <span style="color:#38bdf8;">{current_zone}</span></span>
</div>
<div style="font-size:11.5px;color:#6ee7b7;font-weight:800;">
⚡ 선택되지 않은 나머지 8개 구역은 파이썬에서 아예 실행되지 않아 아래쪽에 잔상이 남지 않습니다
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
        "🛡️ Z7:번외EGR",
        "⚡ Z8:번외격자",
        "📑 Z9:증빙·스펙",
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

    # 구역 전환 시 무조건 화면 맨 위(top:0)로 스크롤 포커스를 즉시 이동시키는 스크립트
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
