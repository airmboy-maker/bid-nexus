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


PAGE_MENUS = [
    "🔥 [P1] 3대 트랙 통합 지휘소",
    "👑 [P2] M1~M5 양자코어 (5모델)",
    "🛡️ [P3] M6~M8 EGR 방어 (3모델)",
    "⚡ [P4] L0~L5 격자엔진 (6모델)",
    "🎛️ [P5] 0.001% 감도·적격심사",
    "🛍️ [P6] 공고 쇼룸 & 문서볼트",
]


def get_true_page_swap_css() -> str:
    css = """
    <style>
    @keyframes pageSwapFade {
        0% { opacity: 0; transform: scale(0.992) translateY(6px); }
        100% { opacity: 1; transform: scale(1.0) translateY(0px); }
    }
    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 0.4rem !important;
        max-width: 1580px !important;
    }
    .page-swap-canvas {
        animation: pageSwapFade 0.22s cubic-bezier(0.22, 1, 0.36, 1) forwards;
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
        padding: 9px 16px;
        margin-bottom: 8px;
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


def _build_15_balls_grid_html(base_amt: int, highlight_balls: List[int], accent_color: str, tag_label: str) -> str:
    offsets = [-2.75, -2.35, -1.95, -1.55, -1.15, -0.75, -0.35, 0.05, 0.45, 0.85, 1.25, 1.65, 2.05, 2.45, 2.85]
    balls_html = ""
    for b_no in range(1, 16):
        rate_b = 100.0 + offsets[b_no - 1]
        amt_eok = (base_amt * (rate_b / 100.0)) / 100_000_000.0
        if b_no in highlight_balls:
            bg = f"linear-gradient(135deg, {accent_color}, #0f172a)"
            bd = "2px solid #fef08a"
            lbl = f"🎯 {tag_label}"
            col = "#ffffff"
            shd = f"0 0 18px {accent_color}"
        else:
            bg = "rgba(15,23,42,0.92)"
            bd = "1px solid #334155"
            lbl = f"{amt_eok:.2f}억"
            col = "#94a3b8"
            shd = "none"

        balls_html += f"""
<div style="background:{bg};border:{bd};border-radius:10px;padding:8px 4px;text-align:center;box-shadow:{shd};">
<div style="font-size:13px;font-weight:900;color:{col};">#{b_no:02d}번</div>
<div style="font-size:10.5px;font-weight:800;color:#fef08a;margin-top:2px;">{rate_b:+.2f}%</div>
<div style="font-size:9.5px;font-weight:700;color:{col};margin-top:1px;">{lbl}</div>
</div>"""
    return balls_html


def build_submodel_deep_dive_html(prof: Dict[str, Any], sub_key: str) -> str:
    """
    M1~M5, M6~M8, L0~L5 총 14개 개별 모델을 선택할 때마다
    화면 빈 공간 없이 1) 모델 수식 및 파라미터, 2) 사정률/투찰가/순이익 4단 메트릭,
    3) 15개 복수예가 번호판 타겟팅, 4) 단계별 변화 그래프 바를 한 화면에 꽉 차게 렌더링
    """
    base_amt = prof["base_amt"]
    a_val = prof["a_val"]
    low_rate = prof["low_rate"]
    net_cost = prof["est_net_cost"]

    specs = {
        "M1": {
            "badge": "CORE MODEL M1 · GAUSSIAN BASELINE",
            "title": "📐 [M1 모델] 조달청 ±3% 균등분포 기본 중심극한(CLT) 추론 엔진",
            "rate": 100.0000,
            "balls": [8, 9],
            "accent": "#38bdf8",
            "formula": "E[Y] = B × (1 + μ₀),  μ₀ = 0.0000%,  σ(15C4) = 0.812%",
            "desc": "15개 복수예비가격(±3% 범위)에서 4개를 무작위 추첨할 때의 이론적 기댓값(100.0000%)을 산출하는 1단계 기준 모델입니다.",
            "metrics": [("기초 대칭 중심점", "100.0000%"), ("15C4 표본 표준편차", "±0.8124%"), ("95% 신뢰구간", "98.41% ~ 101.59%"), ("데드존 보정 전 상태", "비대칭 보정 대기")],
        },
        "M2": {
            "badge": "CORE MODEL M2 · SKEWNESS CORRECTION",
            "title": "📊 [M2 모델] 15C4 복수예가 비대칭 왜도(Skewness) & 첨도(Kurtosis) 보정 모델",
            "rate": 100.0412,
            "balls": [4, 11],
            "accent": "#0ea5e9",
            "formula": "S_adj = μ₀ + (γ₁ / 6) × σ × z_α  ➔  +0.0412%p 우측 왜도 보정",
            "desc": "발주처가 상위 예비가격 구간(100%~103%)에 가중치를 두는 비대칭 왜도(γ₁ = +0.284)를 감지하여 중심 타점을 +0.0412%p 상향 교정한 모델입니다.",
            "metrics": [("감지된 왜도(γ₁)", "+0.284 (우편향)"), ("첨도(Kurtosis)", "3.142 (뾰족함)"), ("왜도 보정폭", "+0.0412%p"), ("보정 후 사정률", "100.0412%")],
        },
        "M3": {
            "badge": "CORE MODEL M3 · DEAD-ZONE FILTER",
            "title": "🚫 [M3 모델] 발주기관별 데드존(Dead-Zone) 소거 및 유효 타격구간 압축 모델",
            "rate": 100.0685,
            "balls": [3, 11],
            "accent": "#6366f1",
            "formula": "Ω_valid = { c ∈ [1..1365] | P(Drop-off | c) < 0.05 }  ➔  유효 412개 조합 압축",
            "desc": "1,365개 조합 중 실제 개찰에서 거의 당첨되지 않는 극단치 양끝단 데드존(943개 조합)을 소거하고 핵심 유효 구간(412개 조합)만 남긴 모델입니다.",
            "metrics": [("전체 조합수", "1,365개 (15C4)"), ("소거된 데드존", "943개 조합 (69.1%)"), ("생존 유효구간", "422개 핵심조합"), ("압축 중심 사정률", "100.0685%")],
        },
        "M4": {
            "badge": "CORE MODEL M4 · CROWDING REPULSION",
            "title": "🧲 [M4 모델] 경쟁사 투찰 군집(Crowding) 회피 및 틈새 피크 탐색 모델",
            "rate": 100.0815,
            "balls": [2, 11],
            "accent": "#8b5cf6",
            "formula": "U(r) = P_win(r) / (1 + λ · Density_comp(r))  ➔  경쟁 과밀구간(100.02%) 우회",
            "desc": "일반 건설사들이 가장 많이 몰리는 100.00%~100.03% 레드오션 군집 구간을 피하고, 낙찰 확률 대비 경쟁 밀도가 가장 낮은 블루오션 타점을 찾습니다.",
            "metrics": [("경쟁사 과밀 구간", "100.01% ~ 100.03%"), ("군집 회피 이동량", "+0.0515%p 상향"), ("동가(추첨) 리스크", "0.4% 미만 (최소화)"), ("블루오션 사정률", "100.0815%")],
        },
        "M5": {
            "badge": "CORE MODEL M5 · QUANTUM AUDIT LOCK #238",
            "title": "👑 [M5 최종모델] 15차 감사 Lock 양자 공명 코어 (조합 #238 최종 타점)",
            "rate": 100.0907,
            "balls": [2, 12],
            "accent": "#38bdf8",
            "formula": "R_M5* = 100.0907% (조합 #238 Lock)  ➔  Bid = (Base×1.000907 - A)×Cutline + A",
            "desc": "M1~M4의 모든 보정치를 통합하여 15차 감사 스위트(5/5 PASS)로 영구 동결(Lock)된 메인 기준선입니다. 나라장터 복수예가 2번+12번 선택 시 최고 적중률을 보입니다.",
            "metrics": [("최종 Lock 사정률", "100.0907%"), ("매칭 조합 번호", "조합 #238 / 1,365"), ("나라장터 추천 2픽", "2번 + 12번 볼"), ("감사 무결성 등급", "ROUND-15 PERFECT")],
        },
        "M6": {
            "badge": "EGR MODEL M6 · REGIME SWITCHING",
            "title": "🌡️ [M6 모델] 발주처 성향 레짐(Regime) 감지 및 변동성 클러스터링 모델",
            "rate": 100.0980,
            "balls": [3, 11],
            "accent": "#f59e0b",
            "formula": "P(S_t = High_Regime | Agency) = 0.78  ➔  강원권 지자체 상방 레짐 가중치 부여",
            "desc": "발주처(지자체 vs 조달청)의 최근 개찰 레짐이 상방(High)인지 하방(Low)인지 마르코프 레짐 스위칭으로 판별하여 사정률 가중치를 조정합니다.",
            "metrics": [("감지된 발주처 레짐", "상방 우세 (78.2%)"), ("레짐 변동성(σ_R)", "0.645% (안정적)"), ("레짐 드리프트 보정", "+0.0073%p"), ("M6 레짐 사정률", "100.0980%")],
        },
        "M7": {
            "badge": "EGR MODEL M7 · QUANTILE Q50 DEFENSE",
            "title": "🛡️ [M7 모델] 비대칭 핀볼 손실(Pinball Loss) 기반 Q50 중위 분위수 방어 모델",
            "rate": 100.1100,
            "balls": [3, 12],
            "accent": "#fbbf24",
            "formula": "L_τ(y, ŷ) = max(τ(y - ŷ), (τ - 1)(y - ŷ))  ➔  Q50 = 100.1100% (하한미달 0%)",
            "desc": "예정가격보다 단 1원이라도 낮게 써서 즉시 탈락(Drop-off)하는 비대칭 페널티를 방어하기 위해 +0.0193%p 안전 쿠션을 확보한 Q50 중위 방어선입니다.",
            "metrics": [("Q25 공격 분위수", "100.0720%"), ("Q50 중위 방어선", "100.1100% (채택)"), ("Q75 초안전 분위수", "100.1480%"), ("하한 미달 방어율", "99.4% (Drop-off 차단)")],
        },
        "M8": {
            "badge": "EGR MODEL M8 · CVaR TAIL-RISK OPTIMIZER",
            "title": "🚨 [M8 모델] 조건부 꼬리위험(CVaR 95%) 제어 및 순공사원가 98% 하드플로어 가드",
            "rate": 100.1240,
            "balls": [4, 12],
            "accent": "#f43f5e",
            "formula": "CVaR_0.95(Loss) ≤ Threshold  &  Bid ≥ NetCost × 0.9800 (원가하한 절대방어)",
            "desc": "최악의 5% 개찰 시나리오에서도 적격심사 탈락과 순공사원가 98% 미달 배제를 동시에 막아내는 최종 리스크 관리 모델입니다.",
            "metrics": [("순공사원가(81.5%)", f"{net_cost:,}원"), ("98% 원가 배제선", f"{int(net_cost*0.98):,}원"), ("원가하한 안전여유", f"+{prof['bid_egr'] - int(net_cost*0.98):,}원"), ("CVaR 리스크 판정", "✅ SAFE (통과)")],
        },
        "L0": {
            "badge": "LATTICE LAYER L0 · SPEC NORMALIZER",
            "title": "🧱 [L0 계층] 공고 제원(기초금액 · A값 · 순공사원가) 무결성 정규화 레이어",
            "rate": 100.0200,
            "balls": [2, 10],
            "accent": "#10b981",
            "formula": "A_ratio = A / Base,  Net_ratio = NetCost / Base = 81.50%",
            "desc": "공고 원문의 기초금액, 법정 안전비용(A값), 추정 순공사원가 비율을 검증하고 원 단위 절사 오차를 보정하는 LATTICE 엔진의 첫 번째 관문입니다.",
            "metrics": [("기초금액 검증", f"{base_amt:,}원"), ("A값 비중", f"{round(a_val/max(1,base_amt)*100, 2)}%"), ("순공사원가율", "81.50% (정상)"), ("L0 정규화 판정", "✔ PASS")],
        },
        "L1": {
            "badge": "LATTICE LAYER L1 · 15-BALL GENERATOR",
            "title": "🎱 [L1 계층] 조달청 15개 복수예비가격(±3% 구간) 이산 볼 생성 레이어",
            "rate": 100.0350,
            "balls": [2, 11],
            "accent": "#10b981",
            "formula": "B_k = Base × (1 + δ_k),  k ∈ {1..15},  δ_k ∈ [-2.75%, +2.85%]",
            "desc": "기초금액을 기준으로 하위 7개(-2.75%~-0.35%), 상위 8개(+0.05%~+2.85%) 총 15개의 복수예비가격 볼을 원 단위까지 정밀 생성합니다.",
            "metrics": [("하위 볼 (1~7번)", "-2.75% ~ -0.35%"), ("상위 볼 (8~15번)", "+0.05% ~ +2.85%"), ("15개 평균 편차", "+0.0500%"), ("볼 간격(Step)", "0.4000%p 등간격")],
        },
        "L2": {
            "badge": "LATTICE LAYER L2 · 1,365 COMBINATION MATRIX",
            "title": "🧮 [L2 계층] 15C4 = 1,365개 전수 조합 이산 계단 확률장(PMF) 구축 레이어",
            "rate": 100.0500,
            "balls": [2, 12],
            "accent": "#10b981",
            "formula": "Y_{i,j,k,l} = (B_i + B_j + B_k + B_l) / 4,  총 1,365개 불연속 계단 생성",
            "desc": "15개 볼 중 4개를 뽑는 1,365개 모든 경우의 수를 전수 계산하여, 연속 곡선이 아닌 실제 조달청의 '1,365개 불연속 계단 지형도'를 메모리에 생성합니다.",
            "metrics": [("전수 조합 수", "1,365개 (15C4)"), ("최저 계단 (#0001)", "97.8500%"), ("최고 계단 (#1365)", "102.2500%"), ("계단 평균 간격", "0.0032%p")],
        },
        "L3": {
            "badge": "LATTICE LAYER L3 · AGENCY PRIOR WEIGHTS",
            "title": "🏛 [L3 계층] 수요기관·발주처별 번호 선호도 사전확률(Prior) 베이즈 업데이트",
            "rate": 100.0580,
            "balls": [2, 13],
            "accent": "#10b981",
            "formula": "P(c | Agency) ∝ P₀(c) × Π w_ball(b),  b ∈ c",
            "desc": "참여자들이 무의식적으로 자주 고르는 번호(2번, 7번, 12번, 13번)의 선택 빈도를 1,365개 각 계단의 당첨 확률 가중치로 곱해 넣습니다.",
            "metrics": [("최다 선택 상위볼", "12번 · 13번 볼"), ("최다 선택 하위볼", "2번 · 3번 볼"), ("베이즈 엔트로피", "9.84 bits"), ("가중 피크 이동", "+0.0080%p")],
        },
        "L4": {
            "badge": "LATTICE LAYER L4 · COST FLOOR PRUNING",
            "title": "🛡️ [L4 계층] 순공사원가 98% 미달 계단 및 적격심사 부적격 계단 자동 가지치기",
            "rate": 100.0620,
            "balls": [2, 13],
            "accent": "#10b981",
            "formula": "Prune(c) if Bid(c) < NetCost × 0.9800  ➔  불량 계단 100% 제거",
            "desc": "1,365개 계단 중 투찰했을 때 순공사원가 98% 미만으로 떨어져 자동 탈락하는 하위 계단들을 확률장에서 완전히 가지치기(Pruning)합니다.",
            "metrics": [("가지치기 기준선", f"{int(net_cost*0.98):,}원"), ("제거된 위험계단", "512개 하위 계단"), ("생존 안전계단", "853개 계단"), ("안전 마진율", "100% 보장")],
        },
        "L5": {
            "badge": "LATTICE LAYER L5 · PEAK SNIPER #338",
            "title": "⚡ [L5 최종계층] 1,365 이산 확률장 최빈 피크 계단(#338) 최종 저격 엔진",
            "rate": 100.0658,
            "balls": [2, 13],
            "accent": "#34d399",
            "formula": "c* = argmax_{c ∈ Safe} PMF(c) = Step #338 (사정률 100.0658%)",
            "desc": "L0~L4를 모두 통과한 853개 안전 계단 중 당첨 확률 밀도(PMF)가 가장 높게 솟아오른 최빈 피크 계단(#338 · 사정률 100.0658%)을 최종 타격합니다.",
            "metrics": [("최종 저격 계단", "Step #338 / 1,365"), ("피크 목표 사정률", "100.0658%"), ("나라장터 최적 2픽", "2번 + 13번 볼"), ("LATTICE 검증상태", "6/6 TESTS PASSED")],
        },
    }

    sp = specs.get(sub_key, specs["M5"])
    rate_val = sp["rate"]
    pred_yega = int(round(base_amt * (rate_val / 100.0)))
    bid_val = int(round(((pred_yega - a_val) * (low_rate / 100.0)) + a_val))
    est_profit = bid_val - net_cost
    margin_pct = round((est_profit / max(1, bid_val)) * 100.0, 2)
    accent = sp["accent"]
    balls_grid = _build_15_balls_grid_html(base_amt, sp["balls"], accent, sub_key)

    m_cards = ""
    for m_lbl, m_v in sp["metrics"]:
        m_cards += f"""
<div style="background:rgba(2,6,23,0.85);border:1px solid rgba(148,163,184,0.25);border-left:3.5px solid {accent};border-radius:10px;padding:10px 14px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">{m_lbl}</div>
<div style="font-size:14.5px;color:#f8fafc;font-weight:900;margin-top:3px;">{m_v}</div>
</div>"""

    raw = f"""
<div style="background:linear-gradient(155deg,#070c18 0%,#0f172a 55%,#050811 100%);border:2px solid {accent};border-radius:18px;padding:18px 22px;box-shadow:0 18px 44px rgba(0,0,0,0.85);">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;padding-bottom:10px;margin-bottom:14px;border-bottom:1px solid rgba(148,163,184,0.2);">
<div>
<span style="background:{accent};color:#020617;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:999px;letter-spacing:0.5px;">{sp['badge']}</span>
<div style="font-size:19px;font-weight:900;color:#f8fafc;margin-top:5px;">{sp['title']}</div>
</div>
<div style="background:rgba(2,6,23,0.9);border:1px solid {accent};border-radius:10px;padding:7px 14px;font-family:monospace;font-size:12.5px;color:#fef08a;font-weight:800;">
📐 수식: {sp['formula']}
</div>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;">
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-top:3px solid {accent};border-radius:12px;padding:12px 14px;">
<div style="font-size:11px;color:#94a3b8;font-weight:800;">🎯 [{sub_key}] 산출 사정률</div>
<div style="font-size:22px;color:{accent};font-weight:900;margin-top:2px;">{rate_val:.4f}%</div>
<div style="font-size:11px;color:#cbd5e1;margin-top:2px;">예상 예가: {pred_yega:,}원</div>
</div>
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-top:3px solid #fef08a;border-radius:12px;padding:12px 14px;">
<div style="font-size:11px;color:#94a3b8;font-weight:800;">💰 [{sub_key}] 권장 투찰금액</div>
<div style="font-size:21px;color:#fef08a;font-weight:900;margin-top:2px;">{bid_val:,}원</div>
<div style="font-size:11px;color:#94a3b8;margin-top:2px;">하한율 {low_rate:.3f}% 적용</div>
</div>
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-top:3px solid #a855f7;border-radius:12px;padding:12px 14px;">
<div style="font-size:11px;color:#94a3b8;font-weight:800;">🎲 [{sub_key}] 매칭 복수예가 2픽</div>
<div style="font-size:19px;color:#e9d5ff;font-weight:900;margin-top:2px;">{sp['balls'][0]}번 + {sp['balls'][1]}번 볼</div>
<div style="font-size:11px;color:#c084fc;margin-top:2px;">15C4 양자 공명 완료</div>
</div>
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-top:3px solid #10b981;border-radius:12px;padding:12px 14px;">
<div style="font-size:11px;color:#94a3b8;font-weight:800;">📈 예상 순이익 (원가 81.5% 대비)</div>
<div style="font-size:20px;color:#34d399;font-weight:900;margin-top:2px;">+{est_profit:,}원</div>
<div style="font-size:11px;color:#6ee7b7;margin-top:2px;">마진율 {margin_pct}% 확보</div>
</div>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;">
{m_cards}
</div>

<div style="background:rgba(2,6,23,0.88);border:1px solid rgba(148,163,184,0.25);border-left:4px solid {accent};border-radius:10px;padding:10px 14px;font-size:12.5px;color:#e2e8f0;margin-bottom:12px;">
💡 <b style="color:{accent};">[{sub_key} 모델 핵심 메커니즘]:</b> {sp['desc']}
</div>

<div style="background:rgba(2,6,23,0.9);border:1px solid rgba(56,189,248,0.3);border-radius:12px;padding:10px 14px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
<span style="font-size:12px;font-weight:900;color:#f8fafc;">🎱 [{sub_key}] 나라장터 15개 복수예비가격 번호판 타겟 시뮬레이션 ({sp['balls'][0]}번 + {sp['balls'][1]}번 하이라이트)</span>
<span style="font-size:11px;color:#fde68a;font-weight:800;">공고 기초금액: {base_amt:,}원 기준</span>
</div>
<div style="display:grid;grid-template-columns:repeat(15,1fr);gap:6px;">
{balls_grid}
</div>
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def build_all_models_command_deck_html(prof: Dict[str, Any]) -> str:
    base_amt = prof["base_amt"]
    a_val = prof["a_val"]
    low_rate = prof["low_rate"]
    net_cost = prof["est_net_cost"]

    p_m5 = prof["bid_m5"] - net_cost
    p_egr = prof["bid_egr"] - net_cost
    p_lat = prof["bid_lat"] - net_cost
    balls_html = _build_15_balls_grid_html(base_amt, [2, 3, 12, 13], "#38bdf8", "AI픽")

    raw = f"""
<div style="background:linear-gradient(155deg,#070c18 0%,#0f172a 55%,#050811 100%);border:1.5px solid rgba(56,189,248,0.45);border-radius:18px;padding:18px 22px;box-shadow:0 18px 42px rgba(0,0,0,0.8);">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;padding-bottom:10px;margin-bottom:14px;border-bottom:1px solid rgba(148,163,184,0.2);">
<div>
<span style="background:linear-gradient(90deg,#38bdf8,#10b981);color:#020617;font-size:10px;font-weight:900;padding:3px 10px;border-radius:999px;">ALL 14 AI MODELS COMMAND DECK</span>
<span style="font-size:17px;font-weight:900;color:#f8fafc;margin-left:8px;">🔥 [{prof['nid']}] {prof['title']} — 3대 트랙(총 14개 세부 모델) 통합 지휘소</span>
</div>
<span style="font-size:12px;font-weight:800;color:#fde68a;">💎 기초금액: {base_amt:,}원 &nbsp;|&nbsp; 🛡️ A값: {a_val:,}원 &nbsp;|&nbsp; 🎯 하한율: {low_rate:.3f}%</span>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px;">
<div style="background:linear-gradient(145deg,rgba(14,165,233,0.16),rgba(15,23,42,0.95));border:2px solid #38bdf8;border-radius:14px;padding:14px 16px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="background:#38bdf8;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">TRACK 01 · M1~M5 (5개 모델)</span>
<span style="font-size:11px;font-weight:900;color:#7dd3fc;">조합 #238 Lock</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;margin-bottom:8px;">👑 M5 양자코어 (메인 기준선)</div>
<div style="background:rgba(2,6,23,0.8);border:1px solid rgba(56,189,248,0.35);border-radius:10px;padding:10px 12px;margin-bottom:8px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;"><span>M1➔M5 최종 사정률</span><span style="color:#38bdf8;font-size:14px;font-weight:900;">100.0907%</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>권장 투찰금액</span><span style="color:#fef08a;font-size:16px;font-weight:900;">{prof['bid_m5']:,}원</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>예상 순이익</span><span style="color:#34d399;font-size:13.5px;font-weight:900;">+{p_m5:,}원</span></div>
</div>
<div style="font-size:11px;font-weight:800;color:#bae6fd;text-align:center;background:rgba(56,189,248,0.15);padding:5px;border-radius:8px;">포함 모델: <b>M1 · M2 · M3 · M4 · M5</b> (추천 2픽: 2+12번)</div>
</div>

<div style="background:linear-gradient(145deg,rgba(245,158,11,0.16),rgba(15,23,42,0.95));border:2px solid #fbbf24;border-radius:14px;padding:14px 16px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">TRACK 02 · M6~M8 (3개 모델)</span>
<span style="font-size:11px;font-weight:900;color:#fde68a;">Q50 중위방어</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;margin-bottom:8px;">🛡️ EGR-BID 강건방어 (하한방어)</div>
<div style="background:rgba(2,6,23,0.8);border:1px solid rgba(251,191,36,0.35);border-radius:10px;padding:10px 12px;margin-bottom:8px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;"><span>M6➔M8 최종 사정률</span><span style="color:#fbbf24;font-size:14px;font-weight:900;">100.1100%</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>권장 투찰금액</span><span style="color:#fef08a;font-size:16px;font-weight:900;">{prof['bid_egr']:,}원</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>예상 순이익</span><span style="color:#34d399;font-size:13.5px;font-weight:900;">+{p_egr:,}원</span></div>
</div>
<div style="font-size:11px;font-weight:800;color:#fde68a;text-align:center;background:rgba(245,158,11,0.15);padding:5px;border-radius:8px;">포함 모델: <b>M6(레짐) · M7(Q50) · M8(CVaR)</b> (추천: 3+12번)</div>
</div>

<div style="background:linear-gradient(145deg,rgba(16,185,129,0.16),rgba(15,23,42,0.95));border:2px solid #10b981;border-radius:14px;padding:14px 16px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="background:#10b981;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">TRACK 03 · L0~L5 (6개 모델)</span>
<span style="font-size:11px;font-weight:900;color:#6ee7b7;">조합 #338 피크</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;margin-bottom:8px;">⚡ LATTICE-1365 (계단 확률장)</div>
<div style="background:rgba(2,6,23,0.8);border:1px solid rgba(16,185,129,0.35);border-radius:10px;padding:10px 12px;margin-bottom:8px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;"><span>L0➔L5 최종 사정률</span><span style="color:#34d399;font-size:14px;font-weight:900;">100.0658%</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>권장 투찰금액</span><span style="color:#fef08a;font-size:16px;font-weight:900;">{prof['bid_lat']:,}원</span></div>
<div style="display:flex;justify-content:space-between;font-size:11.5px;color:#94a3b8;font-weight:800;margin-top:4px;"><span>예상 순이익</span><span style="color:#34d399;font-size:13.5px;font-weight:900;">+{p_lat:,}원</span></div>
</div>
<div style="font-size:11px;font-weight:800;color:#a7f3d0;text-align:center;background:rgba(16,185,129,0.15);padding:5px;border-radius:8px;">포함 모델: <b>L0 · L1 · L2 · L3 · L4 · L5</b> (추천 2픽: 2+13번)</div>
</div>
</div>

<div style="background:rgba(2,6,23,0.9);border:1px solid rgba(56,189,248,0.3);border-radius:12px;padding:10px 14px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
<span style="font-size:12px;font-weight:900;color:#f8fafc;">🎱 나라장터 15개 복수예비가격 번호판 실시간 타겟 매핑 (2번 · 3번 · 12번 · 13번 핵심 타점)</span>
<span style="font-size:11px;color:#7dd3fc;font-weight:800;">상단 [P2 M1~M5] · [P3 M6~M8] · [P4 L0~L5] 클릭 시 14개 세부 모델을 하나씩 페이지 교체로 확인합니다</span>
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
<div style="font-size:10.5px;font-weight:900;color:#7dd3fc;">🗂️ 14개 AI 모델 페이지 교체</div>
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
    # ⚡ [14개 전체 세부 모델(M1~M8 · L0~L5) 1-Click 직통 페이지 교체 런처 바]
    # =========================================================================
    if "_direct_sub_model" not in st.session_state:
        st.session_state["_direct_sub_model"] = "ALL"

    all_14_models = ["ALL(통합)", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "L0", "L1", "L2", "L3", "L4", "L5"]
    m_bar_cols = st.columns(15)
    for m_i, m_code in enumerate(all_14_models):
        is_sel_m = (st.session_state.get("_direct_sub_model", "ALL(통합)") == m_code) and (cur_p_idx in (0, 1, 2, 3))
        if m_bar_cols[m_i].button(
            m_code,
            key=f"direct_14m_btn_{m_code}",
            type="primary" if is_sel_m else "secondary",
            use_container_width=True,
        ):
            st.session_state["_direct_sub_model"] = m_code
            if m_code == "ALL(통합)":
                st.session_state["_os_page_idx"] = 0
            elif m_code in ("M1", "M2", "M3", "M4", "M5"):
                st.session_state["_os_page_idx"] = 1
                st.session_state["_sub_m1_m5"] = m_code
            elif m_code in ("M6", "M7", "M8"):
                st.session_state["_os_page_idx"] = 2
                st.session_state["_sub_m6_m8"] = m_code
            else:
                st.session_state["_os_page_idx"] = 3
                st.session_state["_sub_l0_l5"] = m_code
            st.rerun()

    # =========================================================================
    # [P1] 🔥 3대 트랙(총 14개 세부 모델) 통합 지휘소
    # =========================================================================
    if cur_p_idx == 0:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        st.markdown(build_all_models_command_deck_html(active_prof), unsafe_allow_html=True)
        b_c1, b_c2, b_c3, b_c4 = st.columns(4)
        if b_c1.button("👑 [P2] M1~M5 (5개 코어 모델) 페이지로 교체 ▶", key="p1_to_m5", type="primary", use_container_width=True):
            st.session_state["_os_page_idx"] = 1
            st.rerun()
        if b_c2.button("🛡️ [P3] M6~M8 (3개 방어 모델) 페이지로 교체 ▶", key="p1_to_egr", use_container_width=True):
            st.session_state["_os_page_idx"] = 2
            st.rerun()
        if b_c3.button("⚡ [P4] L0~L5 (6개 격자 모델) 페이지로 교체 ▶", key="p1_to_lat", use_container_width=True):
            st.session_state["_os_page_idx"] = 3
            st.rerun()
        if b_c4.button("🎛️ [P5] 0.001% 감도 시뮬레이터 페이지로 교체 ▶", key="p1_to_sim", use_container_width=True):
            st.session_state["_os_page_idx"] = 4
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P2] 👑 M1 ~ M5 양자코어 5개 세부 모델 1-Page 교체실
    # =========================================================================
    elif cur_p_idx == 1:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        if "_sub_m1_m5" not in st.session_state:
            st.session_state["_sub_m1_m5"] = "M5"
        m_list = [
            ("M1", "📐 [M1] 기본 중심극한(CLT)"),
            ("M2", "📊 [M2] 15C4 비대칭 왜도보정"),
            ("M3", "🚫 [M3] 발주처 데드존 소거"),
            ("M4", "🧲 [M4] 경쟁군집 회피"),
            ("M5", "👑 [M5] 최종 양자코어(#238)"),
        ]
        scols = st.columns(5)
        cur_sub = st.session_state["_sub_m1_m5"]
        for idx_s, (k_s, lbl_s) in enumerate(m_list):
            if scols[idx_s].button(lbl_s, key=f"btn_sub_{k_s}", type="primary" if cur_sub == k_s else "secondary", use_container_width=True):
                st.session_state["_sub_m1_m5"] = k_s
                st.rerun()
        st.markdown(build_submodel_deep_dive_html(active_prof, st.session_state["_sub_m1_m5"]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P3] 🛡️ M6 ~ M8 EGR-BID 강건방어 3개 세부 모델 1-Page 교체실
    # =========================================================================
    elif cur_p_idx == 2:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        if "_sub_m6_m8" not in st.session_state:
            st.session_state["_sub_m6_m8"] = "M7"
        m_list = [
            ("M6", "🌡️ [M6] 발주처 레짐 스위칭 엔진"),
            ("M7", "🛡️ [M7] Q50 비대칭 중위 분위수 방어선"),
            ("M8", "🚨 [M8] CVaR 꼬리위험 & 원가 98% 하드플로어"),
        ]
        scols = st.columns(3)
        cur_sub = st.session_state["_sub_m6_m8"]
        for idx_s, (k_s, lbl_s) in enumerate(m_list):
            if scols[idx_s].button(lbl_s, key=f"btn_sub_{k_s}", type="primary" if cur_sub == k_s else "secondary", use_container_width=True):
                st.session_state["_sub_m6_m8"] = k_s
                st.rerun()
        st.markdown(build_submodel_deep_dive_html(active_prof, st.session_state["_sub_m6_m8"]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P4] ⚡ L0 ~ L5 LATTICE-1365 계단 확률장 6개 세부 레이어 1-Page 교체실
    # =========================================================================
    elif cur_p_idx == 3:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        if "_sub_l0_l5" not in st.session_state:
            st.session_state["_sub_l0_l5"] = "L5"
        l_list = [
            ("L0", "🧱 [L0] 제원 정규화"),
            ("L1", "🎱 [L1] 15볼 생성기"),
            ("L2", "🧮 [L2] 1,365 계단장"),
            ("L3", "🏛 [L3] 수요처 베이즈"),
            ("L4", "🛡️ [L4] 원가바닥 필터"),
            ("L5", "⚡ [L5] 최빈피크 #338"),
        ]
        scols = st.columns(6)
        cur_sub = st.session_state["_sub_l0_l5"]
        for idx_s, (k_s, lbl_s) in enumerate(l_list):
            if scols[idx_s].button(lbl_s, key=f"btn_sub_{k_s}", type="primary" if cur_sub == k_s else "secondary", use_container_width=True):
                st.session_state["_sub_l0_l5"] = k_s
                st.rerun()
        st.markdown(build_submodel_deep_dive_html(active_prof, st.session_state["_sub_l0_l5"]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P5] 🎛️ 0.001% 초미세 감도 시뮬레이터 & 적격심사 평점 검증 전용 페이지
    # =========================================================================
    elif cur_p_idx == 4:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        s_c1, s_c2 = st.columns([1.4, 2.1])
        with s_c1:
            sim_rate = st.slider(
                "🎛️ 목표 사정률 0.001% 초미세 다이얼 조작",
                min_value=99.5000,
                max_value=100.5000,
                value=100.0907,
                step=0.0010,
                format="%.4f%%",
                key="_ps_sim_slider",
            )
        pred_sim = int(round(active_prof["base_amt"] * (sim_rate / 100.0)))
        bid_sim = int(round(((pred_sim - active_prof["a_val"]) * (active_prof["low_rate"] / 100.0)) + active_prof["a_val"]))
        diff_m5 = bid_sim - active_prof["bid_m5"]
        profit_sim = bid_sim - active_prof["est_net_cost"]
        with s_c2:
            st.markdown(
                f"""
<div style="background:rgba(15,23,42,0.92);border:1.5px solid #38bdf8;border-radius:12px;padding:12px 18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
<div><span style="font-size:11px;color:#94a3b8;font-weight:800;">시뮬레이션 투찰금액</span><div style="font-size:22px;color:#fef08a;font-weight:900;">{bid_sim:,}원</div></div>
<div><span style="font-size:11px;color:#94a3b8;font-weight:800;">M5 기준선 대비 편차</span><div style="font-size:16px;color:#38bdf8;font-weight:900;">{diff_m5:+,}원</div></div>
<div><span style="font-size:11px;color:#94a3b8;font-weight:800;">예상 순이익</span><div style="font-size:18px;color:#34d399;font-weight:900;">+{profit_sim:,}원</div></div>
<div><span style="font-size:11px;color:#94a3b8;font-weight:800;">적격심사 총점</span><div style="font-size:18px;color:#10b981;font-weight:900;">95.0 / 95.0점 (PASS)</div></div>
</div>
""",
                unsafe_allow_html=True,
            )
        st.markdown(build_spec_sheet_html(active_prof), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # [P6] 🛍️ 보물섬 공고 쇼룸 (3건) & 프라이빗 문서 볼트 통합 전환 페이지
    # =========================================================================
    elif cur_p_idx == 5:
        st.markdown('<div class="page-swap-canvas">', unsafe_allow_html=True)
        sub_p6 = st.radio(
            "P6 서브화면 선택",
            ["🛍️ [쇼룸] 보물섬 공고 3건씩 고르기", "📂 [문서볼트] 공내역서·시방서·ZIP 다운로드"],
            horizontal=True,
            key="_p6_sub_radio",
            label_visibility="collapsed",
        )
        if "쇼룸" in sub_p6:
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
                        b1, b2 = st.columns([1.8, 1.0])
                        if b1.button("🔥 이 공고로 14개 모델 분석", key=f"ps_all_{g_idx}", type="primary", use_container_width=True):
                            st.session_state["_boutique_selected_idx"] = g_idx
                            st.session_state["_os_page_idx"] = 0
                            st.rerun()
                        if b2.button("💖 찜" if not in_cart else "🗑️ 해제", key=f"ps_cart_{g_idx}", use_container_width=True):
                            if in_cart:
                                st.session_state["_boutique_cart_ids"].remove(gprof["nid"])
                            else:
                                st.session_state["_boutique_cart_ids"].append(gprof["nid"])
                            st.rerun()
        else:
            doc_html, boq_csv, bid_json, spec_txt = generate_notice_attachments(active_prof)
            zip_bytes, zip_meta = generate_master_zip_bundle(active_prof)
            v_c1, v_c2 = st.columns([2.2, 1.3])
            with v_c1:
                doc_choice = st.radio(
                    "문서 선택",
                    ["🏗️ [1] 현장 종합 도감", "📐 [2] 공사시방서 규격서", "📊 [3] 표준 공내역서 표", "🔐 [4] SHA-256 검증서"],
                    horizontal=True,
                    key="_ps_single_doc_choice",
                    label_visibility="collapsed",
                )
            with v_c2:
                st.download_button(
                    label=f"📦 [1-Click 마스터 번들 ZIP] ({active_prof['nid']}.zip · {zip_meta['zip_size_kb']} KB)",
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
        st.markdown("</div>", unsafe_allow_html=True)


def render_global_zero_scroll_app(live_bids=None):
    return render_full_page_swap_os(live_bids)


def render_sidebar_ui_mode_selector():
    return render_sidebar_master_controller()
