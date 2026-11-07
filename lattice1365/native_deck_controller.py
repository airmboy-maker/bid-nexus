import streamlit as st
import streamlit.components.v1 as components

DECK_ZONES = [
    "🌟 [전체 보기] 모든 구역 한눈에 펼치기",
    "📡 [ZONE 1] 나라장터 공고 쇼룸 & 스마트 필터",
    "🎯 [ZONE 2] 핵심 적격심사 & 통합 산출물",
    "⚡ [ZONE 3] 4차원 입체 추론 (M1~M5 왜도·데드존)",
    "🎛️ [ZONE 4] 0.001% 초미세 감도 시뮬레이터",
    "🌌 [ZONE 5] AI ENGINE LAB (5D 우주조감·애니메이션·EGR·LATTICE)",
    "📑 [ZONE 6] 적격 증빙서류 일람표 & 기업 마스터 OCR",
]


def render_master_mode_and_zone_selector() -> tuple:
    if "_ndc_mode" not in st.session_state:
        st.session_state["_ndc_mode"] = "💎 1-Page 캐비닛 집중 모드 (무스크롤)"
    if "_ndc_zone" not in st.session_state:
        st.session_state["_ndc_zone"] = "📡 [ZONE 1] 나라장터 공고 쇼룸 & 스마트 필터"

    with st.sidebar:
        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.22),rgba(15,23,42,0.96));border:1.5px solid #fbbf24;border-radius:10px;padding:8px 11px;margin-top:2px;margin-bottom:6px;box-shadow:0 6px 18px rgba(0,0,0,0.5);">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:11px;font-weight:900;color:#fde68a;">💎 SCREEN MODE SWITCH</span>
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">v3.0 DUAL</span>
</div>
<div style="font-size:9.5px;color:#cbd5e1;font-weight:700;margin-top:2px;">모든 원본 모델·애니메이션 100% 보존</div>
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
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗄️ 캐비닛 구역(Zone) 선택</div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:700;">선택한 구역으로 화면이 즉시 전환됩니다</div>
</div>
""",
                unsafe_allow_html=True,
            )
            zone = st.radio(
                "집중할 캐비닛 구역 선택",
                DECK_ZONES[1:],
                key="_ndc_zone",
                label_visibility="collapsed",
            )
        else:
            zone = DECK_ZONES[0]

    return is_cabinet_mode, zone


def render_top_cabinet_switcher_bar(is_cabinet_mode: bool, current_zone: str) -> None:
    if not is_cabinet_mode:
        return

    tab_idx_map = {
        "ZONE 1": 0,
        "ZONE 2": 1,
        "ZONE 3": 2,
        "ZONE 4": 3,
        "ZONE 5": 2,
        "ZONE 6": 4,
    }
    target_tab_idx = 0
    for k, v in tab_idx_map.items():
        if k in current_zone:
            target_tab_idx = v
            break

    st.markdown(
        f"""
<style>
.block-container {{
    padding-top: 1.2rem !important;
    padding-bottom: 1.0rem !important;
    max-width: 1560px !important;
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
    padding: 9px 16px;
    margin-bottom: 10px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.7);
}}
</style>
<div class="cabinet-focus-ribbon">
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;">💎 CABINET FOCUS MODE</span>
<span style="font-size:14px;font-weight:900;color:#f8fafc;">현재 열린 캐비닛: <span style="color:#38bdf8;">{current_zone}</span></span>
</div>
<div style="font-size:11.5px;color:#6ee7b7;font-weight:800;">
✨ 원본 6대 전체 메뉴 · 4D 애니메이션 · AI ENGINE LAB(5D 우주조감/EGR/LATTICE) 100% 활성 상태
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    components.html(
        f"""
<script>
(function() {{
    const targetIdx = {target_tab_idx};
    setTimeout(() => {{
        try {{
            const parentDoc = window.parent.document;
            const tabs = parentDoc.querySelectorAll('button[data-baseweb="tab"]');
            if (tabs && tabs.length > targetIdx) {{
                tabs[targetIdx].click();
            }}
        }} catch (e) {{}}
    }}, 120);
}})();
</script>
""",
        height=0,
        scrolling=False,
    )
