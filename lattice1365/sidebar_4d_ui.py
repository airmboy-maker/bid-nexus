def get_sidebar_4d_global_css() -> str:
    """
    타이틀 카드(GATEKEEPER STATUS, 4D COMMAND DECK)와 하위 요소들이 절대 겹치지 않도록
    각 컨테이너의 높이 계산과 상하 간격(margin/gap)을 명확히 분리하는 전역 CSS
    """
    return """
    <style>
    /* 1. 좌측 사이드바 배경 및 스크롤바 숨김 유지 */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebarContent"] {
        background:
            radial-gradient(circle at 20% 10%, rgba(244, 63, 94, 0.12) 0%, transparent 38%),
            radial-gradient(circle at 80% 45%, rgba(56, 189, 248, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 30% 88%, rgba(16, 185, 129, 0.12) 0%, transparent 50%),
            linear-gradient(180deg, #030712 0%, #090d16 48%, #020617 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.38) !important;
        box-shadow: 8px 0 30px rgba(0, 0, 0, 0.75) !important;
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
        padding-top: 0.6rem !important;
        padding-bottom: 0.4rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    /* 위젯 간 겹침 방지를 위해 수직 블록 간격을 0.5rem으로 확보하고 각 요소 높이를 자동(auto)으로 강제 */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
        height: auto !important;
        min-height: 0 !important;
        overflow: visible !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.48rem !important;
    }

    /* 2. 상단 ⚡ GATEKEEPER STATUS 헤더 — 아래 배지와 절대 겹치지 않도록 하단 여백(margin-bottom: 8px) 및 독립 블록 보장 */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        display: block !important;
        position: relative !important;
        box-sizing: border-box !important;
        width: 100% !important;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #090d16 100%) !important;
        border: 1.2px solid rgba(251, 191, 36, 0.65) !important;
        border-left: 4px solid #f59e0b !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        margin-top: 0px !important;
        margin-bottom: 8px !important;
        color: #f8fafc !important;
        font-size: 13.5px !important;
        font-weight: 900 !important;
        line-height: 1.3 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
        clear: both !important;
    }
    section[data-testid="stSidebar"] h2::before,
    section[data-testid="stSidebar"] h3::before {
        content: "SECURITY GATEWAY · 4D SHIELD";
        display: block;
        font-size: 8.5px;
        font-weight: 900;
        color: #fbbf24;
        letter-spacing: 0.6px;
        margin-bottom: 3px;
        line-height: 1.1;
    }

    /* 3. ⚠️ 알림 박스(stAlert) 상하 간격 분리 */
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {
        background: linear-gradient(135deg, rgba(69, 10, 10, 0.88) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1.2px solid rgba(244, 63, 94, 0.55) !important;
        border-left: 4px solid #f43f5e !important;
        border-radius: 10px !important;
        padding: 8px 11px !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45) !important;
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
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: keep-all !important;
        line-height: 1.38 !important;
        font-size: 11.5px !important;
        font-weight: 700 !important;
        color: #fecdd3 !important;
    }

    /* 4. 🔐 모바일/외부 접속 보안 PIN 설정 */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 55%, #090d16 100%) !important;
        border: 1.2px solid rgba(168, 85, 247, 0.55) !important;
        border-left: 4px solid #a855f7 !important;
        border-radius: 10px !important;
        margin-top: 2px !important;
        margin-bottom: 4px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
        padding: 7px 11px !important;
        min-height: 34px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
        font-size: 11.5px !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
        white-space: nowrap !important;
    }

    /* 5. 사이드바 체크박스 4종 — 상단 타이틀 박스와 겹치지 않도록 독립 여백 부여 */
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        position: relative !important;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.94) 0%, rgba(17, 24, 39, 0.98) 100%);
        border: 1px solid rgba(51, 65, 85, 0.85);
        border-left: 3.5px solid #10b981;
        border-radius: 9px;
        padding: 6px 9px !important;
        margin-top: 2px !important;
        margin-bottom: 2px !important;
        min-height: 32px !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.35);
        transition: all 0.18s ease;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 11px !important;
        font-weight: 800 !important;
        line-height: 1.25 !important;
        white-space: nowrap !important;
        letter-spacing: -0.35px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {
        border-color: #38bdf8;
        border-left-color: #fbbf24;
        transform: translateX(2px);
    }

    /* 6. 사이드바 구분선(hr) */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #38bdf8, #10b981, transparent) !important;
        margin: 6px 0 !important;
        opacity: 0.65 !important;
    }
    </style>
    """


def build_sidebar_4d_tesseract_html(active_count: int = 4) -> str:
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
  .cmd-card {{
    background: radial-gradient(circle at 50% 38%, #0f172a 0%, #060b14 70%, #020617 100%);
    border: 1.2px solid rgba(56, 189, 248, 0.5);
    border-radius: 12px;
    padding: 9px 11px;
    position: relative;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), inset 0 0 18px rgba(16, 185, 129, 0.08);
  }}
  .scanline {{
    position: absolute; top: 0; left: 0; right: 0; height: 1.5px;
    background: linear-gradient(90deg, transparent, #38bdf8, #fbbf24, transparent);
    animation: scanMove 3.2s linear infinite;
    opacity: 0.7; pointer-events: none;
  }}
  @keyframes scanMove {{
    0% {{ top: 2px; opacity: 0.2; }}
    50% {{ opacity: 0.85; }}
    100% {{ top: 96%; opacity: 0.2; }}
  }}
  .top-row {{
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 5px; margin-bottom: 5px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.15);
  }}
  .badge-4d {{
    background: linear-gradient(90deg, #38bdf8, #10b981);
    color: #020617; font-size: 9px; font-weight: 900;
    padding: 2px 7px; border-radius: 999px; white-space: nowrap;
  }}
  .status-pill {{
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 2px 7px; border-radius: 999px;
    font-size: 9px; color: #34d399; font-weight: 800; white-space: nowrap;
  }}
  .pulse-dot {{
    width: 6px; height: 6px; border-radius: 50%; background: #10b981;
    display: inline-block; box-shadow: 0 0 6px #10b981;
  }}
  .title-block {{
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 6px;
  }}
  .main-title {{ font-size: 11.5px; font-weight: 900; color: #f8fafc; white-space: nowrap; }}
  .sub-title {{ font-size: 9.5px; font-weight: 600; color: #94a3b8; white-space: nowrap; }}
  #tesseractCanvas {{
    width: 100%; height: 78px; display: block;
    background: rgba(2, 6, 23, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 8px;
    margin-bottom: 7px;
  }}
  .telemetry-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px;
  }}
  .t-cell {{
    background: rgba(15, 23, 42, 0.92); border: 1px solid #1e293b;
    border-radius: 7px; padding: 4px 2px; text-align: center; white-space: nowrap;
  }}
  .t-label {{ font-size: 9px; color: #cbd5e1; font-weight: 700; margin-bottom: 1px; }}
  .t-val {{ font-size: 10.5px; font-weight: 900; }}
</style>
</head>
<body>
<div class="cmd-card">
  <div class="scanline"></div>
  <div class="top-row">
    <span class="badge-4d">4D CORE v20.4</span>
    <span class="status-pill"><span class="pulse-dot"></span> {active_count}개 모듈 가동</span>
  </div>
  <div class="title-block">
    <span class="main-title">🪐 QUANTUM MATRIX</span>
    <span class="sub-title">4차원 초입방체 코어</span>
  </div>
  <canvas id="tesseractCanvas"></canvas>
  <div class="telemetry-grid">
    <div class="t-cell" style="border-bottom:2px solid #38bdf8;">
      <div class="t-label">👑 M5 코어</div>
      <div class="t-val" style="color:#38bdf8;">100.09%</div>
    </div>
    <div class="t-cell" style="border-bottom:2px solid #fbbf24;">
      <div class="t-label">🛡️ EGR 방어</div>
      <div class="t-val" style="color:#fbbf24;">Q50 락온</div>
    </div>
    <div class="t-cell" style="border-bottom:2px solid #10b981;">
      <div class="t-label">⚡ LATTICE</div>
      <div class="t-val" style="color:#34d399;">#338 피크</div>
    </div>
  </div>
</div>

<script>
// 상단 GATEKEEPER STATUS 배지와 헤더가 절대 겹치지 않도록 상단 여백(marginTop: 8px) 확보
function cleanAndStyleGatekeeperBadge() {{
  try {{
    const parentDoc = window.parent.document;
    const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
    if (!sidebar) return;

    const allEls = sidebar.querySelectorAll('span, div, p');
    allEls.forEach(el => {{
      const txt = (el.innerText || '').trim();
      if (txt === '🔒 적격 마스터 미등록 (잠김)' || txt === '🔓 적격 마스터 승인 완료') {{
        const hasSameChild = Array.from(el.children).some(
          c => (c.innerText || '').trim() === txt
        );
        if (hasSameChild) {{
          el.style.border = 'none';
          el.style.background = 'transparent';
          el.style.boxShadow = 'none';
          el.style.padding = '0';
          el.style.margin = '0';
        }} else {{
          el.style.display = 'block';
          el.style.position = 'relative';
          el.style.boxSizing = 'border-box';
          el.style.width = '100%';
          el.style.padding = '6px 10px';
          el.style.marginTop = '8px';
          el.style.marginBottom = '4px';
          el.style.borderRadius = '9px';
          el.style.fontWeight = '800';
          el.style.fontSize = '11.5px';
          el.style.textAlign = 'center';
          el.style.whiteSpace = 'nowrap';
          el.style.background = txt.includes('잠김')
            ? 'linear-gradient(135deg, rgba(136, 19, 55, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%)'
            : 'linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%)';
          el.style.border = txt.includes('잠김') ? '1.2px solid #f43f5e' : '1.2px solid #10b981';
          el.style.borderLeft = txt.includes('잠김') ? '4px solid #fb7185' : '4px solid #34d399';
          el.style.color = txt.includes('잠김') ? '#ffe4e6' : '#d1fae5';
          el.style.boxShadow = '0 4px 10px rgba(0,0,0,0.4)';
        }}
      }}
    }});
  }} catch (e) {{}}
}}
cleanAndStyleGatekeeperBadge();
setInterval(cleanAndStyleGatekeeperBadge, 800);

const canvas = document.getElementById('tesseractCanvas');
const ctx = canvas.getContext('2d');
let w, h;
function resize() {{
  const r = canvas.getBoundingClientRect();
  w = canvas.width = r.width * window.devicePixelRatio;
  h = canvas.height = r.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
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
    let diff = i ^ j;
    if ((diff & (diff - 1)) === 0) edges.push([i, j]);
  }}
}}

let angle = 0;
function render4D() {{
  const cw = canvas.width / window.devicePixelRatio;
  const ch = canvas.height / window.devicePixelRatio;
  angle += 0.022;
  ctx.clearRect(0, 0, cw, ch);

  const cx = cw / 2, cy = ch / 2;

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(angle * 0.6);
  ctx.beginPath();
  ctx.ellipse(0, 0, 48, 14, 0, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
  ctx.lineWidth = 1.1;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(-angle * 0.45);
  ctx.beginPath();
  ctx.ellipse(0, 0, 16, 34, 0, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.25)';
  ctx.lineWidth = 1.1;
  ctx.stroke();
  ctx.restore();

  const cosA = Math.cos(angle), sinA = Math.sin(angle);
  const cosB = Math.cos(angle * 0.7), sinB = Math.sin(angle * 0.7);

  const projected2D = vertices4D.map(v => {{
    let x = v[0], y = v[1], z = v[2], w4 = v[3];
    let nx = x * cosA - w4 * sinA, nw = x * sinA + w4 * cosA;
    let ny = y * cosB - z * sinB, nz = y * sinB + z * cosB;
    let fx = nx * cosB - ny * sinB, fy = nx * sinB + ny * cosB;

    const wFactor = 1 / (2.6 - nw * 0.65);
    const x3 = fx * wFactor, y3 = fy * wFactor, z3 = nz * wFactor;
    const zFactor = 1 / (2.4 - z3);
    const scale = 38;
    return {{ x: cx + x3 * zFactor * scale, y: cy + y3 * zFactor * scale, w4: nw }};
  }});

  edges.forEach(e => {{
    const p1 = projected2D[e[0]], p2 = projected2D[e[1]];
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    const isOuter = (p1.w4 + p2.w4) > 0;
    ctx.strokeStyle = isOuter ? 'rgba(56, 189, 248, 0.85)' : 'rgba(251, 191, 36, 0.65)';
    ctx.lineWidth = isOuter ? 1.4 : 0.9;
    ctx.stroke();
  }});

  projected2D.forEach(p => {{
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.w4 > 0 ? 2.1 : 1.4, 0, Math.PI * 2);
    ctx.fillStyle = p.w4 > 0 ? '#38bdf8' : '#fbbf24';
    ctx.fill();
  }});

  requestAnimationFrame(render4D);
}}
requestAnimationFrame(render4D);
</script>
</body>
</html>"""
