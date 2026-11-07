def get_sidebar_4d_global_css() -> str:
    """
    상단(ZONE 1: 보안/자격 게이트키퍼)과 하단(ZONE 2: AI 사정 엔진 랩)을 시각적으로 완전히 이원화하고,
    겹치는 가로줄 제거 및 한 줄 가독성을 극대화하는 스마트 UI 스타일시트
    """
    return """
    <style>
    /* 1. 사이드바 베이스: 차분하고 깊이감 있는 프리미엄 다크 슬레이트 */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #07090e 0%, #0b111e 45%, #050a14 100%) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.22) !important;
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
        padding: 0.6rem 0.75rem 0.5rem 0.75rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 6px !important;
    }

    /* =========================================================================
       [ZONE 1 : 상단 보안 게이트키퍼 영역] — 골드/크림슨 시큐리티 테마 (겹침 줄 완전 제거)
       ========================================================================= */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        background: transparent !important;
        border: none !important;
        border-bottom: none !important;
        padding: 0 2px !important;
        margin: 0 0 2px 0 !important;
        color: #f8fafc !important;
        font-size: 13px !important;
        font-weight: 900 !important;
        letter-spacing: 0.4px !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    section[data-testid="stSidebar"] h2::after,
    section[data-testid="stSidebar"] h3::after {
        content: "ZONE 1 · SECURITY";
        font-size: 8.5px;
        font-weight: 900;
        color: #fbbf24;
        background: rgba(245, 158, 11, 0.14);
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 2px 7px;
        border-radius: 999px;
        letter-spacing: 0.4px;
    }

    /* ZONE 1 알림창: 정돈된 소프트 크림슨 카드 */
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: linear-gradient(135deg, rgba(69, 10, 10, 0.55) 0%, rgba(15, 23, 42, 0.85) 100%) !important;
        border: 1px solid rgba(244, 63, 94, 0.35) !important;
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

    /* ZONE 1 보안 PIN Expander: 다크 골드/슬레이트 톤으로 ZONE 1에 귀속 */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-left: 3.5px solid #f59e0b !important;
        border-radius: 9px !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
        padding: 6px 10px !important;
        min-height: 32px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
        font-size: 11.5px !important;
        font-weight: 800 !important;
        color: #fde68a !important;
    }

    /* =========================================================================
       [ZONE 2 : 하단 AI 사정 엔진 랩] — 시안/에메랄드 스마트 iOS 스타일 스위치 타일
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
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(9, 14, 26, 0.95) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.28) !important;
        border-radius: 9px !important;
        padding: 7px 9px !important;
        margin: 0 !important;
        min-height: 38px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.18s ease !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {
        border-color: #38bdf8 !important;
        background: rgba(30, 41, 59, 0.92) !important;
        transform: translateY(-1px);
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 11px !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        color: #e2e8f0 !important;
        white-space: nowrap !important;
        letter-spacing: -0.3px !important;
    }

    /* 기본 hr 구분선 숨김 (커스텀 ZONE 디바이더 사용) */
    section[data-testid="stSidebar"] hr {
        display: none !important;
    }
    </style>
    """


def build_sidebar_4d_tesseract_html(active_count: int = 4) -> str:
    """
    글자가 두 줄로 꺾이거나 밑단이 절대 깨지지 않도록:
    - 상단: 100% 와이드 파노라마 4D 홀로그램 코어 (높이 66px)
    - 하단: 100% 전체 폭을 쓰는 3줄 와이드 텔레메트리 바 (글자 줄바꿈 원천 차단!)
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
    background: linear-gradient(180deg, rgba(12, 19, 34, 0.95) 0%, rgba(6, 10, 19, 0.98) 100%);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 11px;
    padding: 10px 12px 11px 12px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55);
  }}
  .hdr-line {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 7px;
  }}
  .hdr-title {{
    font-size: 11px; font-weight: 900; color: #7dd3fc; letter-spacing: 0.4px;
    white-space: nowrap;
  }}
  .hdr-status {{
    font-size: 9.5px; font-weight: 800; color: #34d399;
    background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 2px 8px; border-radius: 999px; white-space: nowrap;
  }}
  /* 상단 파노라마 4D 홀로그램 뷰어 (전체 폭 사용) */
  #tesseractCanvas {{
    width: 100%; height: 64px; display: block;
    background: radial-gradient(ellipse at 50% 50%, rgba(14, 165, 233, 0.16) 0%, rgba(2, 6, 23, 0.85) 80%);
    border: 1px solid rgba(56, 189, 248, 0.22);
    border-radius: 8px;
    margin-bottom: 8px;
  }}
  /* 하단 3대 트랙 와이드 바: 전체 가로폭을 다 써서 한 줄에 시원하게 배치 (줄바꿈 0%) */
  .wide-bars {{
    display: flex; flex-direction: column; gap: 6px;
  }}
  .w-row {{
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(51, 65, 85, 0.65);
    border-radius: 7px;
    padding: 5px 9px;
  }}
  .w-top {{
    display: flex; justify-content: space-between; align-items: center;
    font-size: 11px; font-weight: 800; margin-bottom: 4px;
    white-space: nowrap;
  }}
  .w-name {{ color: #f1f5f9; white-space: nowrap; }}
  .w-val {{ font-weight: 900; white-space: nowrap; }}
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
        <span class="w-name">👑 트랙 1 · M5 양자코어</span>
        <span class="w-val" style="color:#38bdf8;">100.0907% (#238)</span>
      </div>
      <div class="track-bg"><div class="track-fill" style="width:76%;background:linear-gradient(90deg,#0284c7,#38bdf8);"></div></div>
    </div>
    <div class="w-row" style="border-left:3px solid #fbbf24;">
      <div class="w-top">
        <span class="w-name">🛡️ 트랙 2 · EGR 강건방어</span>
        <span class="w-val" style="color:#fbbf24;">100.1100% (Q50)</span>
      </div>
      <div class="track-bg"><div class="track-fill" style="width:88%;background:linear-gradient(90deg,#d97706,#fbbf24);"></div></div>
    </div>
    <div class="w-row" style="border-left:3px solid #10b981;">
      <div class="w-top">
        <span class="w-name">⚡ 트랙 3 · LATTICE 확률장</span>
        <span class="w-val" style="color:#34d399;">100.0658% (#338)</span>
      </div>
      <div class="track-bg"><div class="track-fill" style="width:66%;background:linear-gradient(90deg,#059669,#34d399);"></div></div>
    </div>
  </div>
</div>

<script>
// ZONE 1 상단 잠금 배지 정돈 (위아래 겹침 선 완전 제거)
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
          el.style.padding = '0';
          el.style.margin = '0';
        }} else {{
          el.style.display = 'block';
          el.style.width = '100%';
          el.style.boxSizing = 'border-box';
          el.style.padding = '6px 10px';
          el.style.marginTop = '2px';
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

const canvas = document.getElementById('tesseractCanvas');
const ctx = canvas.getContext('2d');
let cw = 240, ch = 64;
function resize() {{
  const r = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  cw = r.width || 240;
  ch = 64;
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

  // 배경 사정률 파동 사인파 (파노라마 효과)
  ctx.beginPath();
  for (let x = 0; x <= cw; x += 4) {{
    const y = ch / 2 + Math.sin(x * 0.04 - angle * 2) * 10 * Math.sin(x / cw * Math.PI);
    if (x === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }}
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.28)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // 중심 4D 테서랙트 코어
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
    return {{ x: cx + fx * wf * zf * 26, y: cy + fy * wf * zf * 24, w4: nw }};
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
