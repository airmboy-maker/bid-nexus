import streamlit as st


class _HiddenZoneContext:
    """
    선택되지 않은 구역(Tab/Section)의 위젯들이 화면 높이와 스크롤을 차지하지 않도록
    렌더링을 깔끔하게 건너뛰거나 숨겨주는 컨텍스트 매니저
    """
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return None
        return _noop


DECK_ZONES = [
    "📡 [ZONE 1] 나라장터 공고 쇼룸 & 스마트 필터",
    "🎯 [ZONE 2] 핵심 적격심사 & 통합 산출물",
    "⚡ [ZONE 3] 5대 AI 모델 해부 (레거시·저격·특이점·판도라X10·앙상블)",
    "🕹️ [ZONE 4] 3D 60FPS 홀로그램 애니메이션 (KP-01~03 & 4D LAB)",
    "🎛️ [ZONE 5] 0.001% 초미세 감도 시뮬레이터",
    "📑 [ZONE 6] 적격 증빙서류 일람표 & 기업 마스터 OCR",
]


def render_master_mode_and_zone_selector() -> tuple:
    if "_ndc_mode" not in st.session_state:
        st.session_state["_ndc_mode"] = "💎 1-Page 캐비닛 집중 모드 (무스크롤)"
    if "_ndc_zone" not in st.session_state:
        st.session_state["_ndc_zone"] = DECK_ZONES[0]

    with st.sidebar:
        st.markdown(
            """
<div style="background:linear-gradient(135deg,rgba(251,191,36,0.22),rgba(15,23,42,0.96));border:1.5px solid #fbbf24;border-radius:10px;padding:8px 11px;margin-top:2px;margin-bottom:6px;box-shadow:0 6px 18px rgba(0,0,0,0.5);">
<div style="display:flex;justify-content:space-between;align-items:center;">
<span style="font-size:11px;font-weight:900;color:#fde68a;">💎 SCREEN MODE SWITCH</span>
<span style="background:#fbbf24;color:#020617;font-size:8.5px;font-weight:900;padding:1px 6px;border-radius:999px;">PYTHON NATIVE</span>
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
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗄️ 1-Page 구역(Zone) 즉시 교체</div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:700;">클릭 즉시 해당 구역만 단독 표시됩니다</div>
</div>
""",
                unsafe_allow_html=True,
            )
            if st.session_state.get("_ndc_zone") not in DECK_ZONES:
                st.session_state["_ndc_zone"] = DECK_ZONES[0]
            zone = st.radio(
                "집중할 캐비닛 구역 선택",
                DECK_ZONES,
                key="_ndc_zone",
                label_visibility="collapsed",
            )
        else:
            zone = "ALL"

    return is_cabinet_mode, zone


def _set_zone_cb(z_label: str) -> None:
    st.session_state["_ndc_zone"] = z_label


def render_top_cabinet_switcher_bar(is_cabinet_mode: bool, current_zone: str) -> None:
    """
    상단에서도 6개 ZONE을 원클릭 버튼으로 즉시 교체할 수 있는 네이티브 도킹 바
    """
    if not is_cabinet_mode:
        return


    # ZONE 3(5대 모델 해부) vs ZONE 4(3D 홀로그램 애니메이션) 선택 시 탭3 내부도 스크롤 없이 깔끔하게 포커싱
    zone_specific_css = ""
    if "ZONE 1" not in current_zone:
        # ZONE 2~6을 볼 때는 상단 마감 D-5 4칸 요약 배너를 슬림하게 숨겨서 모델과 애니메이션이 화면 맨 위로 바로 올라오게 처리!
        zone_specific_css += """
        div:has(> #ndc-top-banner-anchor) { display: none !important; }
        """

    st.markdown(
        f"""
<style>
.block-container {{
    padding-top: 1.0rem !important;
    padding-bottom: 0.5rem !important;
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
<div class="cabinet-focus-ribbon">
<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;">💎 1-PAGE NATIVE SWAP</span>
<span style="font-size:14px;font-weight:900;color:#f8fafc;">현재 단독 활성 페이지: <span style="color:#38bdf8;">{current_zone}</span></span>
</div>
<div style="font-size:11.5px;color:#fde68a;font-weight:800;">
⚡ 선택한 구역만 한 화면에 단독 렌더링되어 세로 스크롤을 최소화합니다
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    short_labels = [
        "📡 [Z1] 공고쇼룸·필터",
        "🎯 [Z2] 적격심사·산출물",
        "⚡ [Z3] 5대 모델 해부",
        "🕹️ [Z4] 3D 홀로그램·LAB",
        "🎛️ [Z5] 0.001% 감도",
        "📑 [Z6] 증빙서류·기업OCR",
    ]
    cols = st.columns(6)
    for i, z_full in enumerate(DECK_ZONES):
        is_act = (z_full == current_zone)
        cols[i].button(
            short_labels[i],
            key=f"top_z_btn_{i}",
            type="primary" if is_act else "secondary",
            use_container_width=True,
            on_click=_set_zone_cb,
            args=(z_full,),
        )


def create_zone_tabs(tab_labels: list, is_cabinet_mode: bool, current_zone: str):
    """
    기존 통합 스크롤 모드일 때는 원래의 st.tabs(tab_labels)를 그대로 반환하고,
    1-Page 캐비닛 집중 모드일 때는 오직 선택된 ZONE에 해당하는 탭만 실제 st.container()를 주고
    나머지 5개 탭은 화면 밖 숨김 컨테이너로 분리하여, 좌측 사이드바나 상단 버튼 클릭 시 100% 즉시 해당 탭만 단독 표시되게 만듦!
    """
    if not is_cabinet_mode:
        return st.tabs(tab_labels)

    # 1-Page 캐비닛 집중 모드일 때: 어떤 탭 인덱스를 활성화할지 결정
    # tab1(0): 레이더, tab2(1): 적격분석, tab3(2): 4차원 입체추론(5대모델 & 3D홀로그램), tab4(3): 0.001% 시뮬레이터, tab5(4): 증빙서류, tab6(5): 기업 마스터
    active_indices = [0]
    if "ZONE 1" in current_zone:
        active_indices = [0]
    elif "ZONE 2" in current_zone:
        active_indices = [1]
    elif "ZONE 3" in current_zone or "ZONE 4" in current_zone:
        active_indices = [2]
    elif "ZONE 5" in current_zone:
        active_indices = [3]
    elif "ZONE 6" in current_zone:
        active_indices = [4, 5]

    # 화면에 실제로 보일 메인 스테이지 컨테이너 생성
    main_stage = st.container()

    # 선택되지 않은 탭의 위젯들은 높이 0px 숨김 영역 안에 렌더링하여 세션 상태와 변수는 100% 유지하되 화면에는 절대 보이지 않게 차단!
    st.markdown(
        """
<style>
div[data-testid="stExpander"].ndc-hidden-expander,
div:has(> div > #ndc-hidden-vault-anchor) {
    display: none !important;
    height: 0px !important;
    overflow: hidden !important;
    margin: 0px !important;
    padding: 0px !important;
}
</style>
""",
        unsafe_allow_html=True,
    )
    hidden_Wrapper = st.container()
    with hidden_Wrapper:
        st.markdown('<div id="ndc-hidden-vault-anchor"></div>', unsafe_allow_html=True)

    result_containers = []
    for idx in range(len(tab_labels)):
        if idx in active_indices:
            result_containers.append(main_stage)
        else:
            result_containers.append(hidden_Wrapper)

    return result_containers
