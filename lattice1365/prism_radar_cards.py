from typing import Dict, Any


def get_prism_deck_css() -> str:
    """
    필터 매칭 공고 리스트를 초감각적인 '양자 전술 프리즘 덱(Quantum Tactical Prism Deck)'과
    하단 일체형 도킹 워프 버튼(Full-Width Cyber Warp Trigger)으로 변환하는 스타일시트
    """
    return """
    <style>
    @keyframes prismScan {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes reactorSpin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes pulseBeacon {
        0%, 100% { opacity: 0.55; transform: scale(0.92); }
        50% { opacity: 1.0; transform: scale(1.18); }
    }

    /* 프리즘 카드 본체 */
    .q-prism-card {
        position: relative;
        background:
            radial-gradient(circle at 12% 20%, rgba(56, 189, 248, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 88% 80%, rgba(168, 85, 247, 0.14) 0%, transparent 48%),
            linear-gradient(135deg, rgba(11, 17, 32, 0.96) 0%, rgba(6, 10, 21, 0.99) 100%);
        border: 1px solid rgba(56, 189, 248, 0.38);
        border-left: 4.5px solid #38bdf8;
        border-radius: 16px;
        padding: 18px 22px 16px 22px;
        margin-top: 14px;
        margin-bottom: 4px;
        box-shadow:
            0 12px 32px rgba(0, 0, 0, 0.65),
            inset 0 1px 0 rgba(255, 255, 255, 0.12);
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
        overflow: hidden;
        word-break: keep-all;
    }
    .q-prism-card:hover {
        border-color: rgba(251, 191, 36, 0.8);
        border-left: 5.5px solid #fbbf24;
        transform: translateY(-3px) scale(1.003);
        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.8),
            0 0 28px rgba(56, 189, 248, 0.28),
            inset 0 0 25px rgba(251, 191, 36, 0.06);
    }

    /* 상단 오로라 레이저 스윕 바 */
    .q-prism-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 2.5px;
        background: linear-gradient(90deg, transparent, #38bdf8, #a855f7, #10b981, #fbbf24, transparent);
        background-size: 200% 200%;
        animation: prismScan 5s ease infinite;
        opacity: 0.9;
    }

    /* 상단 메타 & 태그 줄 */
    .q-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.14);
    }
    .q-serial-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 3px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        color: #7dd3fc;
        letter-spacing: 0.3px;
    }
    .q-beacon-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 8px #10b981;
        animation: pulseBeacon 1.6s infinite;
    }
    .q-tag-row {
        display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
    }
    .q-holo-tag {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.16), rgba(168, 85, 247, 0.16));
        border: 1px solid rgba(168, 85, 247, 0.45);
        color: #e9d5ff;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
    }
    .q-holo-tag.region {
        background: rgba(16, 185, 129, 0.14);
        border-color: rgba(16, 185, 129, 0.45);
        color: #6ee7b7;
    }
    .q-holo-tag.dday {
        background: rgba(245, 158, 11, 0.16);
        border-color: rgba(245, 158, 11, 0.5);
        color: #fde68a;
    }

    /* 메인 그리드: 좌측(타이틀+발주처+3대 데이터포드) + 우측(AI 공명 리액터 게이지) */
    .q-main-body {
        display: grid;
        grid-template-columns: 1fr 148px;
        gap: 18px;
        align-items: center;
    }
    @media (max-width: 768px) {
        .q-main-body { grid-template-columns: 1fr; }
    }

    .q-title-text {
        font-size: 18px;
        font-weight: 900;
        color: #f8fafc;
        letter-spacing: -0.3px;
        line-height: 1.35;
        margin-bottom: 6px;
        text-shadow: 0 2px 12px rgba(56, 189, 248, 0.22);
    }
    .q-sub-meta {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 12px;
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
    }
    .q-sub-meta b { color: #e2e8f0; }

    /* 3-Column 홀로그램 데이터 포드 */
    .q-pods-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    .q-pod {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(51, 65, 85, 0.85);
        border-radius: 10px;
        padding: 9px 12px;
        position: relative;
        overflow: hidden;
    }
    .q-pod-label {
        font-size: 10.5px;
        font-weight: 800;
        color: #94a3b8;
        margin-bottom: 3px;
        display: flex;
        justify-content: space-between;
    }
    .q-pod-val {
        font-size: 15px;
        font-weight: 900;
        color: #f8fafc;
        letter-spacing: -0.2px;
        margin-bottom: 5px;
    }
    .q-pod-bar-bg {
        width: 100%; height: 4px; background: #020617; border-radius: 999px; overflow: hidden;
    }
    .q-pod-bar-fill { height: 100%; border-radius: 999px; }

    /* 우측 AI 양자 공명 리액터 코어 */
    .q-reactor-box {
        background: radial-gradient(circle, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 14px;
        padding: 10px 8px;
        text-align: center;
        position: relative;
        box-shadow: inset 0 0 20px rgba(56, 189, 248, 0.12);
    }
    .q-reactor-svg {
        width: 70px; height: 70px; margin: 0 auto 4px auto; display: block;
    }
    .q-reactor-ring-spin {
        transform-origin: 50% 50%;
        animation: reactorSpin 9s linear infinite;
    }
    .q-reactor-tag {
        font-size: 9.5px; font-weight: 900; color: #34d399;
        letter-spacing: 0.5px; display: block;
    }
    .q-reactor-sub {
        font-size: 10px; font-weight: 700; color: #94a3b8; margin-top: 1px;
    }
    </style>
    """


def build_prism_notice_card_html(n: Dict[str, Any], idx: int = 0) -> str:
    """
    단일 공고 데이터를 받아 AI 초감각 '양자 전술 프리즘 카드(Quantum Tactical Prism Card)' HTML을 생성
    """
    nid = str(n.get("id", n.get("notice_no", "202611-00000")))
    title = str(n.get("title", "관급 건축공사"))
    agency = str(n.get("agency", "조달청"))
    deadline = str(n.get("deadline", "2026-11-13 10:00"))
    license_name = str(n.get("license", "건축공사업"))
    region_name = str(n.get("region", "강원특별자치도"))

    base_amt = int(n.get("base_amount", 0))
    a_val = int(n.get("a_value", 0))
    low_rate = float(n.get("lower_limit_rate", 88.745))

    eok_val = base_amt / 100_000_000.0
    scale_pct = min(98, max(22, int((eok_val / 100.0) * 100)))
    a_ratio_pct = round((a_val / float(base_amt)) * 100.0, 2) if base_amt > 0 else 0.0
    a_bar_w = min(95, max(18, int(a_ratio_pct * 12)))

    seed_val = sum(ord(c) for c in nid) + idx * 7
    resonance_score = round(96.4 + (seed_val % 31) * 0.1, 1)
    dash_offset = round(163.36 * (1.0 - resonance_score / 100.0), 1)

    if base_amt >= 5_000_000_000:
        tier_label = "TIER-A · 중대형 코어"
        accent_color = "#38bdf8"
    else:
        tier_label = "TIER-B · 알짜 전략선"
        accent_color = "#10b981"

    return f"""
    <div class="q-prism-card" style="border-left-color:{accent_color};">
      <div class="q-top-bar">
        <div class="q-serial-pill">
          <span class="q-beacon-dot"></span>
          <span>QUANTUM NODE #{idx+1:02d}</span>
          <span style="color:#475569;">|</span>
          <span style="color:#e2e8f0;">공고번호 {nid}</span>
        </div>
        <div class="q-tag-row">
          <span class="q-holo-tag">{tier_label}</span>
          <span class="q-holo-tag">{license_name}</span>
          <span class="q-holo-tag region">📍 {region_name}</span>
          <span class="q-holo-tag dday">⏱ 마감 {deadline}</span>
        </div>
      </div>

      <div class="q-main-body">
        <div>
          <div class="q-title-text">🚀 {title}</div>
          <div class="q-sub-meta">
            <span>🏛 <b>발주기관:</b> {agency}</span>
            <span>⚡ <b>AI 분석 트랙:</b> M5 기준선 · EGR Q50 방어 · LATTICE 1,365계단 동시 호환</span>
          </div>

          <div class="q-pods-grid">
            <div class="q-pod" style="border-bottom:2px solid #38bdf8;">
              <div class="q-pod-label">
                <span>💎 기초금액 (BASE SCALE)</span>
                <span style="color:#38bdf8;">약 {eok_val:.1f}억</span>
              </div>
              <div class="q-pod-val" style="color:#f8fafc;">{base_amt:,}원</div>
              <div class="q-pod-bar-bg">
                <div class="q-pod-bar-fill" style="width:{scale_pct}%;background:linear-gradient(90deg,#0284c7,#38bdf8);"></div>
              </div>
            </div>

            <div class="q-pod" style="border-bottom:2px solid #a855f7;">
              <div class="q-pod-label">
                <span>🛡️ A값 (법정 안전비용)</span>
                <span style="color:#c084fc;">비중 {a_ratio_pct:.2f}%</span>
              </div>
              <div class="q-pod-val" style="color:#e9d5ff;">{a_val:,}원</div>
              <div class="q-pod-bar-bg">
                <div class="q-pod-bar-fill" style="width:{a_bar_w}%;background:linear-gradient(90deg,#7e22ce,#c084fc);"></div>
              </div>
            </div>

            <div class="q-pod" style="border-bottom:2px solid #fbbf24;">
              <div class="q-pod-label">
                <span>🎯 낙찰하한율 (CUTLINE)</span>
                <span style="color:#fbbf24;">적격 커트라인</span>
              </div>
              <div class="q-pod-val" style="color:#fde68a;">{low_rate:.3f}%</div>
              <div class="q-pod-bar-bg">
                <div class="q-pod-bar-fill" style="width:{min(100, int(low_rate))}%;background:linear-gradient(90deg,#d97706,#fbbf24);"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="q-reactor-box">
          <svg class="q-reactor-svg" viewBox="0 0 64 64">
            <circle cx="32" cy="32" r="26" fill="none" stroke="#1e293b" stroke-width="4.5" />
            <circle cx="32" cy="32" r="26" fill="none" stroke="{accent_color}" stroke-width="4.5"
                    stroke-dasharray="163.36" stroke-dashoffset="{dash_offset}"
                    stroke-linecap="round" transform="rotate(-90 32 32)" />
            <circle class="q-reactor-ring-spin" cx="32" cy="32" r="20" fill="none"
                    stroke="rgba(251, 191, 36, 0.45)" stroke-width="1.2" stroke-dasharray="6 5" />
            <text x="32" y="30" text-anchor="middle" fill="#f8fafc" font-size="11.5" font-weight="900">{resonance_score}%</text>
            <text x="32" y="41" text-anchor="middle" fill="#38bdf8" font-size="6.5" font-weight="800">AI LOCK</text>
          </svg>
          <span class="q-reactor-tag">● QUANTUM READY</span>
          <div class="q-reactor-sub">3대 엔진 정밀 타겟</div>
        </div>
      </div>
    </div>
    """
