def get_sidebar_4d_global_css() -> str:
    """
    좌측 사이드바 전체가 마우스 스크롤 없이 한 화면(100vh)에 모두 들어오도록
    간격·패딩을 초슬림화하고 스크롤바를 완전히 숨기는 4D 아이소메트릭 전역 CSS
    """
    return """
    <style>
    /* 1. 좌측 사이드바 전체 배경 및 스크롤바 완전 제거 (Zero-Scroll) */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebarContent"] {
        background:
            radial-gradient(circle at 20% 10%, rgba(244, 63, 94, 0.14) 0%, transparent 38%),
            radial-gradient(circle at 80% 45%, rgba(56, 189, 248, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 30% 88%, rgba(16, 185, 129, 0.14) 0%, transparent 50%),
            linear-gradient(180deg, #030712 0%, #090d16 48%, #020617 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.42) !important;
        box-shadow: 10px 0 36px rgba(0, 0, 0, 0.8), inset -1px 0 20px rgba(56, 189, 248, 0.15) !important;
        word-break: keep-all !important;
        overflow-y: hidden !important;
        overflow-x: hidden !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    section[data-testid="stSidebar"] *::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* 사이드바 상하단 기본 여백 최소화 */
    section[data-testid="stSidebar"] .block-container,
    section[data-testid="stSidebarUserContent"] {
        perspective: 1000px;
        padding-top: 0.35rem !important;
        padding-bottom: 0.25rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.28rem !important;
    }

    /* 2. 상단 ⚡ GATEKEEPER STATUS 타이틀 슬림 4D 카드화 */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 55%, #090d16 100%) !important;
        border: 1.5px solid rgba(251, 191, 36, 0.65) !important;
        border-left: 4.5px solid #f59e0b !important;
        border-radius: 10px !important;
        padding: 6px 11px !important;
        margin-top: 0px !important;
        margin-bottom: 4px !important;
        color: #f8fafc !important;
        font-size: 13.5px !important;
        font-weight: 900 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6), 0 0 14px rgba(245, 158, 11, 0.22) !important;
        transition: all 0.25s ease !important;
    }
    section[data-testid="stSidebar"] h2::before,
    section[data-testid="stSidebar"] h3::before {
        content: "SECURITY GATEWAY · 4D SHIELD";
        display: block;
        font-size: 8.5px;
        font-weight: 900;
        color: #fbbf24;
        letter-spacing: 0.7px;
        margin-bottom: 1px;
    }

    /* 3. ⚠️ 기업 마스터 적격 스펙 알림 박스(stAlert) 슬림 4D 입체화 + 말줄임(...) 해제 */
    section[data-testid="stSidebar"] div[data-testid="stAlert"],
    section[data-testid="stSidebar"] div[role="alert"] {
        background: linear-gradient(135deg, rgba(69, 10, 10, 0.92) 0%, rgba(15, 23, 42, 0.96) 100%) !important;
        border: 1.2px solid rgba(244, 63, 94, 0.65) !important;
        border-left: 4.5px solid #f43f5e !important;
        border-radius: 10px !important;
        padding: 6px 10px !important;
        margin-top: 2px !important;
        margin-bottom: 4px !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.55), 0 0 14px rgba(244, 63, 94, 0.2) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stAlert"] p,
    section[data-testid="stSidebar"] div[data-testid="stAlert"] div,
    section[data-testid="stSidebar"] div[role="alert"] p,
    section[data-testid="stSidebar"] div[role="alert"] span {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: keep-all !important;
        line-height: 1.32 !important;
        font-size: 11.5px !important;
        font-weight: 800 !important;
        color: #fecdd3 !important;
    }

    /* 4. 🔐 모바일/외부 접속 보안 PIN 설정 (stExpander) 슬림 4D 볼트 카드화 */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #090d16 100%) !important;
        border: 1.2px solid rgba(168, 85, 247, 0.65) !important;
        border-left: 4.5px solid #a855f7 !important;
        border-radius: 10px !important;
        margin-top: 2px !important;
        margin-bottom: 4px !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.55), 0 0 14px rgba(168, 85, 247, 0.22) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
        padding: 6px 10px !important;
        min-height: 32px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
        font-size: 12px !important;
        font-weight: 900 !important;
        color: #f8fafc !important;
    }

    /* 5. 사이드바 버튼 슬림 4D 입체화 */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #090d16 100%) !important;
        border: 1.2px solid rgba(56, 189, 248, 0.55) !important;
        border-left: 4.5px solid #38bdf8 !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        font-weight: 800 !important;
        font-size: 12px !important;
        padding: 6px 11px !important;
        min-height: 34px !important;
        margin-top: 2px !important;
        margin-bottom: 3px !important;
        box-shadow: 0 5px 14px rgba(0, 0, 0, 0.5) !important;
    }

    /* 6. 사이드바 체크박스(4개 모듈 스위치) 한 줄 슬림 4D 캡슐화 */
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.94) 0%, rgba(17, 24, 39, 0.98) 100%);
        border: 1.2px solid rgba(51, 65, 85, 0.9);
        border-left: 4px solid #10b981;
        border-radius: 9px;
        padding: 5px 10px !important;
        margin-bottom: 3px !important;
        min-height: 32px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 11.5px !important;
        font-weight: 800 !important;
        line-height: 1.25 !important;
        word-break: keep-all !important;
        letter-spacing: -0.2px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {
        border-color: #38bdf8;
        border-left-color: #fbbf24;
        transform: translateX(3px);
    }

    /* 7. 사이드바 구분선(hr) 여백 초슬림화 */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #38bdf8, #10b981, transparent) !important;
        margin: 5px 0 !important;
        opacity: 0.7 !important;
    }
    </style>
    """


def build_sidebar_4d_tesseract_html(active_count: int = 4) -> str:
    """
    스크롤 없이 한 화면에 쏙 들어오도록 높이(205px)를 정밀 압축한 4D 초입방체(Tesseract) 홀로그램 코어
    """
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {{
    box-sizing: border-box; margin: 0; padding: 0;
    font-family: 'Pretendard', -apple-system, 'Malgun Gothic', sans-serif;
    word-break: keep-all;
  }}
  body {{ background: transparent; color: #f8fafc; overflow: hidden; padding: 1px; }}
  .cmd-card {{
    background: radial-gradient(circle at 50% 38%, #0f172a 0%, #060b14 70%, #020617 100%);
    border: 1.5px solid rgba(56, 189, 248, 0.55);
    border-radius: 12px;
    padding: 9px 11px 9px 11px;
    position: relative;
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.2), inset 0 0 20px rgba(16, 185, 129, 0.08);
  }}
  .scanline {{
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, #fbbf24, transparent);
    animation: scanMove 3.2s linear infinite;
    opacity: 0.75; pointer-events: none;
  }}
  @keyframes scanMove {{
    0% {{ top: 2px; opacity: 0.2; }}
    50% {{ opacity: 0.9; }}
    100% {{ top: 96%; opacity: 0.2; }}
  }}
  .top-row {{
    display: flex; justify-content: space-between; align-items: center;
    gap: 4px; padding-bottom: 5px; margin-bottom: 5px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.16);
  }}
  .badge-4d {{
    background: linear-gradient(90deg, #38bdf8, #10b981);
    color: #020617; font-size: 9.5px; font-weight: 900;
    padding: 2px 8px; border-radius: 999px; letter-spacing: 0.3px;
    white-space: nowrap;
  }}
  .status-pill {{
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 2px 7px; border-radius: 999px;
    font-size: 9.5px; color: #34d399; font-weight: 800;
    white-space: nowrap;
  }}
  .pulse-dot {{
    width: 6px; height: 6px; border-radius: 50%; background: #10b981;
    display: inline-block; box-shadow: 0 0 6px #10b981;
  }}
  .title-block {{
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 6px;
  }}
  .main-title {{
    font-size: 12px; font-weight: 900; color: #f8fafc;
    letter-spacing: 0.1px; white-space: nowrap;
  }}
  .sub-title {{
    font-size: 9.5px; font-weight: 600; color: #94a3b8; white-space: nowrap;
  }}
  #tesseractCanvas {{
    width: 100%; height: 86px; display: block;
    background: rgba(2, 6, 23, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 9px;
    margin-bottom: 7px;
  }}
  .telemetry-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px;
  }}
  .t-cell {{
    background: rgba(15, 23, 42, 0.92); border: 1px solid #1e293b;
    border-radius: 7px; padding: 4px 3px; text-align: center;
    white-space: nowrap;
  }}
  .t-label {{
    font-size: 9px; color: #cbd5e1; font-weight: 700; margin-bottom: 1px;
  }}
  .t-val {{
    font-size: 10.5px; font-weight: 900;
  }}
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
function upgradeParentGatekeeperTo4D() {{
  try {{
    const parentDoc = window.parent.document;
    const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
    if (!sidebar) return;

    const allEls = sidebar.querySelectorAll('span, div, p');
    allEls.forEach(el => {{
      const txt = (el.innerText || '').trim();
      if (txt === '🔒 적격 마스터 미등록 (잠김)' || txt === '🔓 적격 마스터 승인 완료') {{
        el.style.display = 'block';
        el.style.width = '100%';
        el.style.padding = '5px 10px';
        el.style.marginTop = '2px';
        el.style.marginBottom = '3px';
        el.style.borderRadius = '9px';
        el.style.fontWeight = '900';
        el.style.fontSize = '11.5px';
        el.style.textAlign = 'center';
        el.style.background = txt.includes('잠김')
          ? 'linear-gradient(135deg, rgba(136, 19, 55, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)'
          : 'linear-gradient(135deg, rgba(6, 78, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%)';
        el.style.border = txt.includes('잠김') ? '1.2px solid #f43f5e' : '1.2px solid #10b981';
        el.style.borderLeft = txt.includes('잠김') ? '4.5px solid #fb7185' : '4.5px solid #34d399';
        el.style.color = txt.includes('잠김') ? '#ffe4e6' : '#d1fae5';
      }}
    }});
  }} catch (e) {{}}
}}
upgradeParentGatekeeperTo4D();
setInterval(upgradeParentGatekeeperTo4D, 1200);

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

  const cx = cw / 2;
  const cy = ch / 2;

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(angle * 0.6);
  ctx.beginPath();
  ctx.ellipse(0, 0, 52, 16, 0, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
  ctx.lineWidth = 1.1;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(-angle * 0.45);
  ctx.beginPath();
  ctx.ellipse(0, 0, 18, 38, 0, 0, Math.PI * 2);
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
    const scale = 42;
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
    ctx.arc(p.x, p.y, p.w4 > 0 ? 2.2 : 1.5, 0, Math.PI * 2);
    ctx.fillStyle = p.w4 > 0 ? '#38bdf8' : '#fbbf24';
    ctx.fill();
  }});

  requestAnimationFrame(render4D);
}}
requestAnimationFrame(render4D);
</script>
</body>
</html>"""
