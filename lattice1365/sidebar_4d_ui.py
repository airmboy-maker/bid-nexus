def get_sidebar_4d_global_css() -> str:
    """
    상단(ZONE 1: 보안 게이트키퍼)과 하단(ZONE 2: AI 엔진 랩) 완전 이원화 및 겹침/말줄임 방지 CSS
    """
    return """
    <style>
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

    /* [ZONE 1 : 상단 보안 게이트키퍼] */
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

    /* [ZONE 2 : 하단 AI 사정 엔진 랩 2x2 그리드] */
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
    html_tpl = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {
    box-sizing: border-box; margin: 0; padding: 0;
    font-family: 'Pretendard', -apple-system, 'Malgun Gothic', sans-serif;
  }
  body { background: transparent; color: #f8fafc; overflow: hidden; padding: 1px; }
  .lab-card {
    width: 100%;
    background: linear-gradient(180deg, rgba(8, 24, 44, 0.92) 0%, rgba(5, 12, 24, 0.98) 100%);
    border: 1px solid rgba(56, 189, 248, 0.38);
    border-radius: 11px;
    padding: 10px 11px 11px 11px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55);
  }
  .hdr-line {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 7px;
  }
  .hdr-title {
    font-size: 11px; font-weight: 900; color: #7dd3fc; letter-spacing: 0.3px;
    white-space: nowrap;
  }
  .hdr-status {
    font-size: 9px; font-weight: 800; color: #34d399;
    background: rgba(16, 185, 129, 0.16); border: 1px solid rgba(16, 185, 129, 0.45);
    padding: 2px 7px; border-radius: 999px; white-space: nowrap;
  }
  #tesseractCanvas {
    width: 100%; height: 60px; display: block;
    background: radial-gradient(ellipse at 50% 50%, rgba(14, 165, 233, 0.18) 0%, rgba(2, 6, 23, 0.88) 80%);
    border: 1px solid rgba(56, 189, 248, 0.24);
    border-radius: 8px;
    margin-bottom: 8px;
  }
  .wide-bars {
    display: flex; flex-direction: column; gap: 6px;
  }
  .w-row {
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid rgba(51, 65, 85, 0.65);
    border-radius: 7px;
    padding: 5px 9px;
  }
  .w-top {
    display: flex; justify-content: space-between; align-items: center;
    gap: 8px;
    font-size: 10.5px; font-weight: 800; margin-bottom: 4px;
    white-space: nowrap;
  }
  .w-name { color: #f1f5f9; white-space: nowrap; flex-shrink: 0; }
  .w-val { font-weight: 900; white-space: nowrap; text-align: right; }
  .track-bg {
    width: 100%; height: 4px; background: #020617; border-radius: 999px; overflow: hidden;
  }
  .track-fill { height: 100%; border-radius: 999px; }
</style>
</head>
<body>
<div class="lab-card">
  <div class="hdr-line">
    <span class="hdr-title">🪐 LIVE QUANTUM TELEMETRY</span>
    <span class="hdr-status">● __ACTIVE_CNT__/4 ACTIVE</span>
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
function styleZone1Badge() {
  try {
    const parentDoc = window.parent.document;
    const sidebar = parentDoc.querySelector('section[data-testid="stSidebar"]');
    if (!sidebar) return;

    const allEls = sidebar.querySelectorAll('span, div, p');
    allEls.forEach(el => {
      const txt = (el.innerText || '').trim();
      if (txt === '🔒 적격 마스터 미등록 (잠김)' || txt === '🔓 적격 마스터 승인 완료') {
        const hasSameChild = Array.from(el.children).some(c => (c.innerText || '').trim() === txt);
        if (hasSameChild) {
          el.style.border = 'none';
          el.style.background = 'transparent';
          el.style.boxShadow = 'none';
          el.style.padding = '4px 0 0 0';
          el.style.margin = '0';
        } else {
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
        }
      }
    });
  } catch (e) {}
}
styleZone1Badge();
setInterval(styleZone1Badge, 700);

const canvas = document.getElementById('tesseractCanvas');
const ctx = canvas.getContext('2d');
let cw = 240, ch = 60;
function resize() {
  const r = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  cw = r.width || 240;
  ch = 60;
  canvas.width = cw * dpr;
  canvas.height = ch * dpr;
  ctx.scale(dpr, dpr);
}
window.addEventListener('resize', resize);
resize();

const vertices4D = [];
for (let i = 0; i < 16; i++) {
  vertices4D.push([(i & 1) ? 1 : -1, (i & 2) ? 1 : -1, (i & 4) ? 1 : -1, (i & 8) ? 1 : -1]);
}
const edges = [];
for (let i = 0; i < 16; i++) {
  for (let j = i + 1; j < 16; j++) {
    let d = i ^ j;
    if ((d & (d - 1)) === 0) edges.push([i, j]);
  }
}

let angle = 0;
function renderPanorama() {
  angle += 0.025;
  ctx.clearRect(0, 0, cw, ch);

  ctx.beginPath();
  for (let x = 0; x <= cw; x += 4) {
    const y = ch / 2 + Math.sin(x * 0.04 - angle * 2) * 9 * Math.sin(x / cw * Math.PI);
    if (x === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.3)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  const cx = cw / 2, cy = ch / 2;
  const cosA = Math.cos(angle), sinA = Math.sin(angle);
  const cosB = Math.cos(angle * 0.7), sinB = Math.sin(angle * 0.7);

  const pts = vertices4D.map(v => {
    let x = v[0], y = v[1], z = v[2], w4 = v[3];
    let nx = x * cosA - w4 * sinA, nw = x * sinA + w4 * cosA;
    let ny = y * cosB - z * sinB, nz = y * sinB + z * cosB;
    let fx = nx * cosB - ny * sinB, fy = nx * sinB + ny * cosB;
    const wf = 1 / (2.6 - nw * 0.65);
    const zf = 1 / (2.4 - nz * wf);
    return { x: cx + fx * wf * zf * 24, y: cy + fy * wf * zf * 22, w4: nw };
  });

  edges.forEach(e => {
    const p1 = pts[e[0]], p2 = pts[e[1]];
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.strokeStyle = (p1.w4 + p2.w4) > 0 ? 'rgba(56, 189, 248, 0.9)' : 'rgba(251, 191, 36, 0.7)';
    ctx.lineWidth = 1.2;
    ctx.stroke();
  });

  requestAnimationFrame(renderPanorama);
}
requestAnimationFrame(renderPanorama);
</script>
</body>
</html>"""
    return html_tpl.replace("__ACTIVE_CNT__", str(active_count))
