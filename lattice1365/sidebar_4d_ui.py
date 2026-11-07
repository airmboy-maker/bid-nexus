def get_sidebar_4d_global_css() -> str:
    """
    Streamlit의 margin 무시 버그를 물리적 padding/min-height로 완전히 우회하여
    타이틀 겹침 0%, 글자 말줄임(...) 0%, 상하단 ZONE 1/2 완전 이원화를 구현하는 CSS
    """
    return """
    <style>
    /* 1. 사이드바 베이스 */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #090a10 0%, #0a101d 48%, #040811 100%) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.25) !important;
        word-break: keep-all !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        scrollbar-width: none !important;
    }
    section[data-testid="stSidebar"] *::-webkit-scrollbar {
        display: none !important;
    }

    section[data-testid="stSidebar"] .block-container,
    section[data-testid="stSidebarUserContent"] {
        padding: 0.65rem 0.75rem 0.5rem 0.75rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 8px !important;
    }

    /* =========================================================================
       [ZONE 1 : 상단 보안 게이트키퍼] — 물리적 padding-bottom(12px)으로 아래 배지와 겹침 완전 차단!
       ========================================================================= */
    section[data-testid="stSidebar"] div[data-testid="stHeadingWithActionElements"],
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        background: transparent !important;
        border: none !important;
        padding: 2px 2px 12px 2px !important;
        margin: 0 !important;
        min-height: 36px !important;
        color: #fef3c7 !important;
        font-size: 13px !important;
        font-weight: 900 !important;
        letter-spacing: 0.3px !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    /* 액션 링크 아이콘 숨김 (레이아웃 깨짐 방지) */
    section[data-testid="stSidebar"] h2 a,
    section[data-testid="stSidebar"] h3 a,
    section[data-testid="stSidebar"] [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] h2::after,
    section[data-testid="stSidebar"] h3::after {
        content: "ZONE 1 · SECURITY";
        font-size: 8.5px;
        font-weight: 900;
        color: #fbbf24;
        background: rgba(245, 158, 11, 0.16);
        border: 1px solid rgba(245, 158, 11, 0.45);
        padding: 2px 7px;
        border-radius: 999px;
        letter-spacing: 0.3px;
        flex-shrink: 0;
    }

    /* ZONE 1 알림창: 앰버/크림슨 보안 경고 카드 */
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: linear-gradient(135deg, rgba(80, 12, 20, 0.5) 0%, rgba(20, 14, 24, 0.9) 100%) !important;
        border: 1px solid rgba(244, 63, 94, 0.38) !important;
        border-left: 3.5px solid #f43f5e !important;
        border-radius: 9px !important;
        padding: 8px 11px !important;
        margin: 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stAlert"] div[role="alert"],
    section[data-testid="stSidebar"] div[data-testid="stAlert"] div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stAlert"] p {
        font-size: 11.5px !important;
        font-weight: 700 !important;
        line-height: 1.4 !important;
        color: #fecdd3 !important;
        white-space: normal !important;
        word-break: keep-all !important;
    }

    /* ZONE 1 보안 PIN Expander */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: linear-gradient(135deg, rgba(35, 22, 12, 0.65) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.38) !important;
        border-left: 3.5px solid #f59e0b !important;
        border-radius: 9px !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
        padding: 6px 10px !important;
        min-height: 33px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
        font-size: 11.5px !important;
        font-weight: 800 !important;
        color: #fde68a !important;
    }

    /* =========================================================================
       [ZONE 2 : 하단 AI 사정 엔진 랩] — 시안/에메랄드 2x2 택티컬 타일 (말줄임 ... 완전 제거!)
       ========================================================================= */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        gap: 6px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="column"] {
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: linear-gradient(145deg, rgba(8, 28, 48, 0.85) 0%, rgba(6, 15, 30, 0.95) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.32) !important;
        border-left: 3px solid #38bdf8 !important;
        border-radius: 8px !important;
        padding: 6px 7px !important;
        margin: 0 !important;
        min-height: 36px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.18s ease !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {
        border-color: #34d399 !important;
        border-left-color: #10b981 !important;
        background: rgba(14, 38, 64, 0.95) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 10.8px !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        color: #ecfeff !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        letter-spacing: -0.35px !important;
    }

    section[data-testid="stSidebar"] hr {
        display: none !important;
    }
    </style>
    """


def build_sidebar_4d_tesseract_html(active_count: int = 4) -> str:
    """
    하단 텔레메트리 카드:
    - 라벨과 퍼센트 수치가 절대 붙지 않도록 justify-content: space-between + 간결한 트랙명 적용
    - 상단 잠금 배지도 GATEKEEPER STATUS 타이틀과 겹치지 않도록 상단 여백 보장
    """
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {{
    box-sizing: border-box; margin: 0; padding: 0;
    font-family: 'Pretendard', -apple-system, 'Malgun Gothic', sans-serif;
  }}
  body {{ background: transparent; color: #f8fafc; overflow: hidden; padding: 1px; }}
  .lab-card {{
    width: 100%;
    background: linear-gradient(180deg, rgba(8, 24, 44, 0.92) 0%, rgba(5, 12, 24, 0.98) 100%);
    border: 1px solid rgba(56, 189, 248, 0.38);
    border-radius: 11px;
    padding: 10px 11px 11px 11px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55);
  }}
  .hdr-line {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 7px;
  }}
  .hdr-title {{
    font-size: 11px; font-weight: 900; color: #7dd3fc; letter-spacing: 0.3px;
    white-space: nowrap;
  }}
  .hdr-status {{
    font-size: 9px; font-weight: 800; color: #34d399;
    background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(16, 185, 129, 0.45);
    padding: 2px 7px; border-radius: 999px; white-space: nowrap;
  }}
  #tesseractCanvas {{
    width: 100%; height: 60px; display: block;
    background: radial-gradient(ellipse at 50% 50%, rgba(14, 165, 233, 0.18) 0%, rgba(2, 6, 23, 0.88) 80%);
    border: 1px solid rgba(56, 189, 248, 0.24);
    border-radius: 8px;
    margin-bottom: 8px;
  }}
  .wide-bars {{
    display: flex; flex-direction: column; gap: 6px;
  }}
  .w-row {{
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid rgba(51, 65, 85, 0.65);
    border-radius: 7px;
    padding: 5px 9px;
  }}
  .w-top {{
    display: flex; justify-content: space-between; align-items: center;
    gap: 8px;
    font-size: 10.5px; font-weight: 800; margin-bottom: 4px;
    white-space: nowrap;
  }}
  .w-name {{ color: #f1f5f9; white-space: nowrap; flex-shrink: 0; }}
  .w-val {{ font-weight: 900; white-space: nowrap; text-align: right; }}
  .track-bg {{
    width: 100%; height: 4px; background: #020617; border-radius: 999px; overflow: hidden;
  }}
  .track-fill {{ height: 100%; border-radius: 999px; }}
</style>
</head>
<body>
<div class="lab-card">
  <div class="hdr-line">
    <span class="hdr-title">🪐 LIVE QUANTUM TELEMETRY</span>
    <span class="hdr-status">● {active_count}/4 ACTIVE</span>
  </div>
  <canvas id="tesseractCanvas"></canvas>
  <div class="wide-bars">
    <div class="w-row" style="border-left:3px solid #38bdf8;">
      <div class="w-top">
        <span class="w-name">👑 M5 양자코어</span>
        <span class="w-val" style="color:#38bdf8;">100.0907% (#238)</span>
      </div>
      <div class="track-bg"><div class="track-fill" style="width:76%;background:linear-gradient(90deg,#0284c7,#38bdf8);"></div></div>
    </div>
    <div class="w-row" style="border-left:3px solid #fbbf24;">
      <div class="w-top">
        <span class="w-name">🛡️ EGR 강건방어</span>
        <span class="w-val" style="color:#fbbf24;">100.1100% (Q50)</span>
      </div>
      <div class="track-bg"><div class="track-fill" style="width:88%;background:linear-gradient(90deg,#d97706,#fbbf24);"></div></div>
    </div>
    <div class="w-row" style="border-left:3px solid #10b981;">
      <div class="w-top">
        <span class="w-name">⚡ LATTICE 격자</span>
        <span class="w-val" style="color:#34d399;">100.0658% (#338)</span>
      </div>
      <div class="track-bg"><div class="track-fill" style="width:66%;background:linear-gradient(90deg,#059669,#34d399);"></div></div>
    </div>
  </div>
</div>

<script>
// 상단 잠금 배지가 위쪽 GATEKEEPER STATUS 글자와 절대 겹치지 않도록 부모/자식 여백 정돈
function styleZone1Badge() {{
  try {{
    const parentDoc = window.parent.document;
    const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
    if (!sidebar) return;

    const allEls = sidebar.querySelectorAll('span, div, p');
    allEls.forEach(el => {{
      const txt = (el.innerText || '').trim();
      if (txt === '🔒 적격 마스터 미등록 (잠김)' || txt === '🔓 적격 마스터 승인 완료') {{
        const hasSameChild = Array.from(el.children).some(c => (c.innerText || '').trim() === txt);
        if (hasSameChild) {{
          el.style.border = 'none';
          el.style.background = 'transparent';
          el.style.boxShadow = 'none';
          el.style.padding = '4px 0 0 0';
          el.style.margin = '0';
        }} else {{
          el.style.display = 'block';
          el.style.width = '100%';
          el.style.boxSizing = 'border-box';
          el.style.padding = '6px 10px';
          el.style.marginTop = '4px';
          el.style.marginBottom = '2px';
          el.style.borderRadius = '8px';
          el.style.fontWeight = '800';
          el.style.fontSize = '11.5px';
          el.style.textAlign = 'center';
          el.style.background = txt.includes('잠김') ? 'rgba(244, 63, 94, 0.14)' : 'rgba(16, 185, 129, 0.14)';
          el.style.border = txt.includes('잠김') ? '1px solid rgba(244, 63, 94, 0.4)' : '1px solid rgba(16, 185, 129, 0.4)';
          el.style.color = txt.includes('잠김') ? '#fecdd3' : '#a7f3d0';
          el.style.boxShadow = 'none';
        }}
      }}
    }});
  }} catch (e) {{}}
}}
styleZone1Badge();
setInterval(styleZone1Badge, 700);

// ============================================================================
// 🌌 [QUANTUM PRISM MORPHER] 우측 본문의 기존 공고 리스트를 100% 자동 감지하여 초감각 프리즘 덱으로 변환
// ============================================================================
function morphNoticeCardsToQuantumPrism() {
  try {
    const parentDoc = window.parent.document;
    if (!parentDoc) return;

    // 1) 부모 창 head에 프리즘 덱 전용 CSS 주입 (1회)
    if (!parentDoc.getElementById('quantum-prism-injected-css')) {
      const styleEl = parentDoc.createElement('style');
      styleEl.id = 'quantum-prism-injected-css';
      styleEl.innerHTML = `
        @keyframes qPrismSweep {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        @keyframes qReactorSpin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .q-prism-morphed {
          position: relative !important;
          background:
            radial-gradient(circle at 10% 15%, rgba(56, 189, 248, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 90% 85%, rgba(168, 85, 247, 0.16) 0%, transparent 48%),
            linear-gradient(135deg, #0b1120 0%, #060a15 100%) !important;
          border: 1.5px solid rgba(56, 189, 248, 0.42) !important;
          border-left: 5px solid #38bdf8 !important;
          border-radius: 16px !important;
          padding: 18px 22px 16px 22px !important;
          margin-top: 12px !important;
          margin-bottom: 4px !important;
          box-shadow: 0 14px 34px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
          transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1) !important;
          overflow: hidden !important;
        }
        .q-prism-morphed:hover {
          border-color: #fbbf24 !important;
          border-left-color: #f59e0b !important;
          transform: translateY(-4px) scale(1.004) !important;
          box-shadow: 0 20px 44px rgba(0, 0, 0, 0.85), 0 0 30px rgba(56, 189, 248, 0.3) !important;
        }
        .q-prism-morphed::before {
          content: "";
          position: absolute; top: 0; left: 0; right: 0; height: 3px;
          background: linear-gradient(90deg, transparent, #38bdf8, #a855f7, #10b981, #fbbf24, transparent);
          background-size: 200% 200%;
          animation: qPrismSweep 4.5s ease infinite;
        }
        /* 바로 아래 '이 공고 즉시 분석 및 투찰 전환' 버튼을 사이버 도킹 런처 바로 변신 */
        .q-warp-btn-styled button {
          width: 100% !important;
          background: linear-gradient(90deg, #0ea5e9 0%, #6366f1 50%, #10b981 100%) !important;
          background-size: 200% auto !important;
          color: #ffffff !important;
          border: 1px solid rgba(56, 189, 248, 0.6) !important;
          border-radius: 10px !important;
          padding: 9px 18px !important;
          font-size: 13px !important;
          font-weight: 900 !important;
          letter-spacing: 0.4px !important;
          box-shadow: 0 6px 20px rgba(14, 165, 233, 0.35) !important;
          transition: all 0.25s ease !important;
        }
        .q-warp-btn-styled button:hover {
          transform: translateY(-2px) !important;
          box-shadow: 0 10px 28px rgba(16, 185, 129, 0.55) !important;
          border-color: #fbbf24 !important;
        }
      `;
      parentDoc.head.appendChild(styleEl);
    }

    // 2) 본문에서 '공고번호:'와 '기초금액:'과 '낙찰하한율:'을 포함한 원본 카드 블록 탐색
    const mdBlocks = parentDoc.querySelectorAll('div[data-testid="stMarkdownContainer"]');
    let cardSeq = 0;

    mdBlocks.forEach(md => {
      const rawTxt = md.innerText || '';
      if (!rawTxt.includes('공고번호:') || !rawTxt.includes('기초금액:') || !rawTxt.includes('낙찰하한율:')) return;

      cardSeq++;
      const targetBox = md.firstElementChild || md;
      if (targetBox.getAttribute('data-prism-morphed') === '1') return;

      // 텍스트에서 데이터 정밀 추출
      const lines = rawTxt.split('\n').map(s => s.trim()).filter(Boolean);
      const rawTitle = (lines[0] || '관급 공사').replace(/^📌\s*/, '').trim();

      const idMatch = rawTxt.match(/공고번호:\s*([^\s|]+)/);
      const agMatch = rawTxt.match(/발주처:\s*([^|]+?)(?=\s*\|\s*마감:|$)/);
      const dlMatch = rawTxt.match(/마감:\s*([^\n|]+)/);
      const bsMatch = rawTxt.match(/기초금액:\s*([0-9,]+)원/);
      const avMatch = rawTxt.match(/A값:\s*([0-9,]+)원/);
      const lwMatch = rawTxt.match(/낙찰하한율:\s*([0-9.]+)%/);

      const nId = idMatch ? idMatch[1].trim() : '202611-0000';
      const agency = agMatch ? agMatch[1].trim() : '조달청';
      const deadline = dlMatch ? dlMatch[1].trim() : '2026-11-13 10:00';
      const baseStr = bsMatch ? bsMatch[1].trim() : '0';
      const aValStr = avMatch ? avMatch[1].trim() : '0';
      const lowStr = lwMatch ? lwMatch[1].trim() : '88.745';

      const baseNum = parseInt(baseStr.replace(/,/g, ''), 10) || 0;
      const aValNum = parseInt(aValStr.replace(/,/g, ''), 10) || 0;
      const lowNum = parseFloat(lowStr) || 88.745;

      const eokVal = (baseNum / 100000000).toFixed(1);
      const scalePct = Math.min(98, Math.max(24, Math.round((baseNum / 9500000000) * 100)));
      const aRatio = baseNum > 0 ? ((aValNum / baseNum) * 100).toFixed(2) : '0.00';
      const aBarW = Math.min(95, Math.max(20, Math.round(parseFloat(aRatio) * 12)));

      const isTierA = baseNum >= 5000000000;
      const accent = isTierA ? '#38bdf8' : '#10b981';
      const tierBadge = isTierA ? 'TIER-A · 중대형 주력' : 'TIER-B · 고수익 전략';
      const resonance = (96.8 + ((cardSeq * 7) % 27) * 0.1).toFixed(1);
      const dashOff = (163.36 * (1 - parseFloat(resonance) / 100)).toFixed(1);

      targetBox.setAttribute('data-prism-morphed', '1');
      targetBox.className = 'q-prism-morphed';
      targetBox.style.borderLeftColor = accent;

      targetBox.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.16);">
          <div style="display:inline-flex;align-items:center;gap:7px;background:rgba(15,23,42,0.92);border:1px solid ${accent};padding:3px 11px;border-radius:999px;font-size:11px;font-weight:900;color:#7dd3fc;">
            <span style="width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;display:inline-block;"></span>
            <span>QUANTUM NODE #0${cardSeq}</span>
            <span style="color:#475569;">|</span>
            <span style="color:#f8fafc;">공고번호 ${nId}</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
            <span style="background:rgba(56,189,248,0.15);border:1px solid ${accent};color:#bae6fd;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800;">${tierBadge}</span>
            <span style="background:rgba(168,85,247,0.16);border:1px solid rgba(168,85,247,0.45);color:#e9d5ff;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800;">건축공사업 · 강원</span>
            <span style="background:rgba(245,158,11,0.16);border:1px solid rgba(245,158,11,0.5);color:#fde68a;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:800;">⏱ 마감 ${deadline}</span>
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 142px;gap:18px;align-items:center;">
          <div>
            <div style="font-size:18px;font-weight:900;color:#f8fafc;letter-spacing:-0.3px;margin-bottom:5px;text-shadow:0 2px 12px rgba(56,189,248,0.25);">
              🚀 ${rawTitle}
            </div>
            <div style="font-size:12px;color:#94a3b8;font-weight:600;margin-bottom:12px;display:flex;gap:14px;flex-wrap:wrap;">
              <span>🏛 <b style="color:#e2e8f0;">발주처:</b> ${agency}</span>
              <span>⚡ <b style="color:#34d399;">AI 트랙 동기화:</b> M5 코어 · EGR 방어 · LATTICE 1,365계단 즉시 가동 가능</span>
            </div>

            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
              <div style="background:rgba(15,23,42,0.86);border:1px solid #334155;border-bottom:2.5px solid #38bdf8;border-radius:10px;padding:9px 12px;">
                <div style="display:flex;justify-content:space-between;font-size:10.5px;font-weight:800;color:#94a3b8;margin-bottom:3px;">
                  <span>💎 기초금액 스케일</span>
                  <span style="color:#38bdf8;">약 ${eokVal}억</span>
                </div>
                <div style="font-size:15px;font-weight:900;color:#f8fafc;margin-bottom:5px;">${baseStr}원</div>
                <div style="width:100%;height:4px;background:#020617;border-radius:999px;overflow:hidden;">
                  <div style="width:${scalePct}%;height:100%;background:linear-gradient(90deg,#0284c7,#38bdf8);"></div>
                </div>
              </div>

              <div style="background:rgba(15,23,42,0.86);border:1px solid #334155;border-bottom:2.5px solid #a855f7;border-radius:10px;padding:9px 12px;">
                <div style="display:flex;justify-content:space-between;font-size:10.5px;font-weight:800;color:#94a3b8;margin-bottom:3px;">
                  <span>🛡️ A값 (안전비용)</span>
                  <span style="color:#c084fc;">비중 ${aRatio}%</span>
                </div>
                <div style="font-size:15px;font-weight:900;color:#e9d5ff;margin-bottom:5px;">${aValStr}원</div>
                <div style="width:100%;height:4px;background:#020617;border-radius:999px;overflow:hidden;">
                  <div style="width:${aBarW}%;height:100%;background:linear-gradient(90deg,#7e22ce,#c084fc);"></div>
                </div>
              </div>

              <div style="background:rgba(15,23,42,0.86);border:1px solid #334155;border-bottom:2.5px solid #fbbf24;border-radius:10px;padding:9px 12px;">
                <div style="display:flex;justify-content:space-between;font-size:10.5px;font-weight:800;color:#94a3b8;margin-bottom:3px;">
                  <span>🎯 낙찰하한율</span>
                  <span style="color:#fbbf24;">커트라인</span>
                </div>
                <div style="font-size:15px;font-weight:900;color:#fde68a;margin-bottom:5px;">${lowNum.toFixed(3)}%</div>
                <div style="width:100%;height:4px;background:#020617;border-radius:999px;overflow:hidden;">
                  <div style="width:${Math.min(100, Math.round(lowNum))}%;height:100%;background:linear-gradient(90deg,#d97706,#fbbf24);"></div>
                </div>
              </div>
            </div>
          </div>

          <div style="background:radial-gradient(circle,rgba(15,23,42,0.95) 0%,rgba(2,6,23,0.98) 100%);border:1px solid rgba(56,189,248,0.38);border-radius:14px;padding:10px 8px;text-align:center;box-shadow:inset 0 0 20px rgba(56,189,248,0.12);">
            <svg style="width:68px;height:68px;margin:0 auto 4px auto;display:block;" viewBox="0 0 64 64">
              <circle cx="32" cy="32" r="26" fill="none" stroke="#1e293b" stroke-width="4.5" />
              <circle cx="32" cy="32" r="26" fill="none" stroke="${accent}" stroke-width="4.5"
                      stroke-dasharray="163.36" stroke-dashoffset="${dashOff}"
                      stroke-linecap="round" transform="rotate(-90 32 32)" />
              <circle style="transform-origin:50% 50%;animation:qReactorSpin 8s linear infinite;" cx="32" cy="32" r="20" fill="none"
                      stroke="rgba(251,191,36,0.5)" stroke-width="1.3" stroke-dasharray="6 5" />
              <text x="32" y="30" text-anchor="middle" fill="#f8fafc" font-size="11.5" font-weight="900">${resonance}%</text>
              <text x="32" y="41" text-anchor="middle" fill="#38bdf8" font-size="6.5" font-weight="800">AI LOCK</text>
            </svg>
            <span style="font-size:9.5px;font-weight:900;color:#34d399;letter-spacing:0.4px;display:block;">● QUANTUM READY</span>
            <div style="font-size:10px;font-weight:700;color:#94a3b8;margin-top:1px;">타겟 공명도 1등급</div>
          </div>
        </div>
      `;
    });

    // 3) '이 공고 즉시 분석 및 투찰 전환' 버튼들도 사이버 도킹 런처 스타일 부여
    const allBtns = parentDoc.querySelectorAll('div.stButton');
    allBtns.forEach(bDiv => {
      if ((bDiv.innerText || '').includes('이 공고 즉시 분석 및 투찰 전환')) {
        bDiv.classList.add('q-warp-btn-styled');
      }
    });
  } catch (e) {}
}
morphNoticeCardsToQuantumPrism();
setInterval(morphNoticeCardsToQuantumPrism, 500);


const canvas = document.getElementById('tesseractCanvas');
const ctx = canvas.getContext('2d');
let cw = 240, ch = 60;
function resize() {{
  const r = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  cw = r.width || 240;
  ch = 60;
  canvas.width = cw * dpr;
  canvas.height = ch * dpr;
  ctx.scale(dpr, dpr);
}}
window.addEventListener('resize', resize);
resize();

const vertices4D = [];
for (let i = 0; i < 16; i++) {{
  vertices4D.push([(i & 1) ? 1 : -1, (i & 2) ? 1 : -1, (i & 4) ? 1 : -1, (i & 8) ? 1 : -1]);
}}
const edges = [];
for (let i = 0; i < 16; i++) {{
  for (let j = i + 1; j < 16; j++) {{
    let d = i ^ j;
    if ((d & (d - 1)) === 0) edges.push([i, j]);
  }}
}}

let angle = 0;
function renderPanorama() {{
  angle += 0.025;
  ctx.clearRect(0, 0, cw, ch);

  ctx.beginPath();
  for (let x = 0; x <= cw; x += 4) {{
    const y = ch / 2 + Math.sin(x * 0.04 - angle * 2) * 9 * Math.sin(x / cw * Math.PI);
    if (x === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }}
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  const cx = cw / 2, cy = ch / 2;
  const cosA = Math.cos(angle), sinA = Math.sin(angle);
  const cosB = Math.cos(angle * 0.7), sinB = Math.sin(angle * 0.7);

  const pts = vertices4D.map(v => {{
    let x = v[0], y = v[1], z = v[2], w4 = v[3];
    let nx = x * cosA - w4 * sinA, nw = x * sinA + w4 * cosA;
    let ny = y * cosB - z * sinB, nz = y * sinB + z * cosB;
    let fx = nx * cosB - ny * sinB, fy = nx * sinB + ny * cosB;
    const wf = 1 / (2.6 - nw * 0.65);
    const zf = 1 / (2.4 - nz * wf);
    return {{ x: cx + fx * wf * zf * 24, y: cy + fy * wf * zf * 22, w4: nw }};
  }});

  edges.forEach(e => {{
    const p1 = pts[e[0]], p2 = pts[e[1]];
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.strokeStyle = (p1.w4 + p2.w4) > 0 ? 'rgba(56, 189, 248, 0.9)' : 'rgba(251, 191, 36, 0.7)';
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }});

  requestAnimationFrame(renderPanorama);
}}
requestAnimationFrame(renderPanorama);
</script>
</body>
</html>"""
