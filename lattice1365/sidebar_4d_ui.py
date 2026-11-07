def get_sidebar_4d_global_css() -> str:
    """
    좌측 사이드바(st.sidebar)의 모든 메뉴·버튼·체크박스를 4D 아이소메트릭 홀로그램 카드로 변환하고
    한글 어절 단락(word-break: keep-all) 및 줄간격을 정돈하는 전역 CSS
    """
    return """
    <style>
    /* 1. 좌측 사이드바 전체 배경 및 한글 단락 가독성(keep-all) 적용 */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 20% 15%, rgba(56, 189, 248, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 80% 85%, rgba(16, 185, 129, 0.14) 0%, transparent 50%),
            linear-gradient(180deg, #030712 0%, #090d16 48%, #020617 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.38) !important;
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.75), inset -1px 0 18px rgba(56, 189, 248, 0.15) !important;
        word-break: keep-all !important;
        line-height: 1.5 !important;
    }

    section[data-testid="stSidebar"] .block-container {
        perspective: 900px;
    }

    /* 2. 사이드바 버튼 4D 아이소메트릭 네온 부양 효과 */
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.85) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 11px !important;
        color: #f8fafc !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px !important;
        padding: 11px 14px !important;
        margin-top: 4px !important;
        margin-bottom: 6px !important;
        word-break: keep-all !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
        transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: #fbbf24 !important;
        border-left: 4px solid #f59e0b !important;
        color: #fef08a !important;
        transform: translateY(-3px) scale(1.02) rotateX(4deg) rotateY(-3deg) !important;
        box-shadow: -4px 10px 24px rgba(245, 158, 11, 0.35), 0 0 15px rgba(56, 189, 248, 0.4) !important;
    }

    /* 3. 사이드바 Expander 4D 홀로그램 챔버 스타일 */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(9, 13, 22, 0.95)) !important;
        border: 1px solid rgba(168, 85, 247, 0.45) !important;
        border-left: 3.5px solid #a855f7 !important;
        border-radius: 12px !important;
        margin-top: 6px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45), inset 0 0 15px rgba(168, 85, 247, 0.08) !important;
        transition: all 0.25s ease !important;
    }

    /* 4. 사이드바 체크박스(모듈 선택 스위치) 단락 간격 및 가독성 강화 */
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(17, 24, 39, 0.96) 100%);
        border: 1px solid rgba(51, 65, 85, 0.85);
        border-left: 3.5px solid #10b981;
        border-radius: 11px;
        padding: 10px 12px;
        margin-bottom: 9px;
        word-break: keep-all !important;
        line-height: 1.45 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: all 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 12.5px !important;
        font-weight: 700 !important;
        line-height: 1.45 !important;
        word-break: keep-all !important;
        letter-spacing: -0.1px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {
        border-color: #38bdf8;
        border-left-width: 5px;
        border-left-color: #fbbf24;
        transform: translateX(4px) translateY(-2px) scale(1.015);
        box-shadow: -3px 6px 18px rgba(56, 189, 248, 0.28);
    }

    /* 5. 사이드바 구분선(hr) 여백 확장 */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        height: 1.5px !important;
        background: linear-gradient(90deg, transparent, #38bdf8, #10b981, transparent) !important;
        margin: 18px 0 !important;
        opacity: 0.75 !important;
    }
    </style>
    """


def build_sidebar_4d_tesseract_html(active_count: int = 4) -> str:
    """
    상단 배지·타이틀·서브타이틀·캔버스·하단 3대 지표 간격을 여유 있게 띄워 배치한 4D 홀로그램 코어
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
  body {{ background: transparent; color: #f8fafc; overflow: hidden; padding: 2px; }}
  .cmd-card {{
    background: radial-gradient(circle at 50% 38%, #0f172a 0%, #060b14 70%, #020617 100%);
    border: 1.5px solid rgba(56, 189, 248, 0.55);
    border-radius: 15px;
    padding: 15px 14px 14px 14px;
    position: relative;
    box-shadow: 0 0 24px rgba(56, 189, 248, 0.22), inset 0 0 25px rgba(16, 185, 129, 0.1);
  }}
  .scanline {{
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, #fbbf24, transparent);
    animation: scanMove 3.2s linear infinite;
    opacity: 0.75; pointer-events: none;
  }}
  @keyframes scanMove {{
    0% {{ top: 4px; opacity: 0.2; }}
    50% {{ opacity: 0.9; }}
    100% {{ top: 96%; opacity: 0.2; }}
  }}
  /* 상단 배지 줄바꿈 방지 및 양끝 깔끔 정렬 */
  .top-row {{
    display: flex; justify-content: space-between; align-items: center;
    gap: 6px; padding-bottom: 10px; margin-bottom: 10px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.18);
  }}
  .badge-4d {{
    background: linear-gradient(90deg, #38bdf8, #10b981);
    color: #020617; font-size: 10px; font-weight: 900;
    padding: 4px 9px; border-radius: 999px; letter-spacing: 0.4px;
    white-space: nowrap; flex-shrink: 0;
  }}
  .status-pill {{
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 3px 8px; border-radius: 999px;
    font-size: 10px; color: #34d399; font-weight: 800;
    white-space: nowrap; flex-shrink: 0;
  }}
  .pulse-dot {{
    width: 7px; height: 7px; border-radius: 50%; background: #10b981;
    display: inline-block; box-shadow: 0 0 8px #10b981;
    animation: pulseGlow 1.4s infinite alternate;
  }}
  @keyframes pulseGlow {{
    from {{ transform: scale(0.85); opacity: 0.6; }}
    to {{ transform: scale(1.25); opacity: 1.0; }}
  }}
  /* 타이틀 및 한글 설명 단락 띄워 배치 */
  .title-block {{
    margin-bottom: 11px; padding: 0 2px;
  }}
  .main-title {{
    font-size: 13.5px; font-weight: 900; color: #f8fafc;
    letter-spacing: 0.2px; line-height: 1.35; margin-bottom: 3px;
    white-space: nowrap;
  }}
  .sub-title {{
    font-size: 11px; font-weight: 600; color: #94a3b8;
    letter-spacing: -0.1px; line-height: 1.4;
  }}
  #tesseractCanvas {{
    width: 100%; height: 136px; display: block;
    background: rgba(2, 6, 23, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 11px;
    margin-bottom: 11px;
  }}
  /* 하단 3대 코어 요약 카드 간격 및 줄간격 확대 */
  .telemetry-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px;
  }}
  .t-cell {{
    background: rgba(15, 23, 42, 0.92); border: 1px solid #1e293b;
    border-radius: 9px; padding: 8px 4px 7px 4px; text-align: center;
    white-space: nowrap;
  }}
  .t-label {{
    font-size: 10px; color: #cbd5e1; font-weight: 700;
    margin-bottom: 4px; letter-spacing: -0.2px;
  }}
  .t-val {{
    font-size: 11.5px; font-weight: 900; letter-spacing: -0.2px;
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
    <div class="main-title">🪐 QUANTUM COMMAND MATRIX</div>
    <div class="sub-title">4차원 초입방체 실시간 사정 연산 코어</div>
  </div>
  <canvas id="tesseractCanvas"></canvas>
  <div class="telemetry-grid">
    <div class="t-cell" style="border-bottom:2.5px solid #38bdf8;">
      <div class="t-label">👑 M5 코어</div>
      <div class="t-val" style="color:#38bdf8;">100.09%</div>
    </div>
    <div class="t-cell" style="border-bottom:2.5px solid #fbbf24;">
      <div class="t-label">🛡️ EGR 방어</div>
      <div class="t-val" style="color:#fbbf24;">Q50 락온</div>
    </div>
    <div class="t-cell" style="border-bottom:2.5px solid #10b981;">
      <div class="t-label">⚡ LATTICE</div>
      <div class="t-val" style="color:#34d399;">#338 피크</div>
    </div>
  </div>
</div>

<script>
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
  vertices4D.push([
    (i & 1) ? 1 : -1,
    (i & 2) ? 1 : -1,
    (i & 4) ? 1 : -1,
    (i & 8) ? 1 : -1
  ]);
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
  ctx.ellipse(0, 0, 62, 22, 0, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
  ctx.lineWidth = 1.2;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(-angle * 0.45);
  ctx.beginPath();
  ctx.ellipse(0, 0, 24, 58, 0, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.25)';
  ctx.lineWidth = 1.2;
  ctx.stroke();
  ctx.restore();

  const cosA = Math.cos(angle);
  const sinA = Math.sin(angle);
  const cosB = Math.cos(angle * 0.7);
  const sinB = Math.sin(angle * 0.7);

  const projected2D = vertices4D.map(v => {{
    let x = v[0], y = v[1], z = v[2], w4 = v[3];
    let nx = x * cosA - w4 * sinA;
    let nw = x * sinA + w4 * cosA;
    let ny = y * cosB - z * sinB;
    let nz = y * sinB + z * cosB;
    let fx = nx * cosB - ny * sinB;
    let fy = nx * sinB + ny * cosB;

    const distance4D = 2.6;
    const wFactor = 1 / (distance4D - nw * 0.65);
    const x3 = fx * wFactor;
    const y3 = fy * wFactor;
    const z3 = nz * wFactor;

    const distance3D = 2.4;
    const zFactor = 1 / (distance3D - z3);
    const scale = 64;
    return {{
      x: cx + x3 * zFactor * scale,
      y: cy + y3 * zFactor * scale,
      w4: nw
    }};
  }});

  edges.forEach(e => {{
    const p1 = projected2D[e[0]];
    const p2 = projected2D[e[1]];
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    const isOuter = (p1.w4 + p2.w4) > 0;
    ctx.strokeStyle = isOuter ? 'rgba(56, 189, 248, 0.85)' : 'rgba(251, 191, 36, 0.65)';
    ctx.lineWidth = isOuter ? 1.5 : 1.0;
    ctx.stroke();
  }});

  projected2D.forEach(p => {{
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.w4 > 0 ? 2.5 : 1.8, 0, Math.PI * 2);
    ctx.fillStyle = p.w4 > 0 ? '#38bdf8' : '#fbbf24';
    ctx.fill();
  }});

  requestAnimationFrame(render4D);
}}
requestAnimationFrame(render4D);
</script>
</body>
</html>"""
