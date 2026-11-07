def get_sidebar_4d_global_css() -> str:
    """
    개별 위젯마다 덕지덕지 붙던 테두리를 전면 제거하고,
    좌우 끝선이 100% 일치하는 '일체형 모놀리식 대시보드(Monolithic Command Console)' 스타일 적용
    """
    return """
    <style>
    /* 1. 사이드바 베이스: 미니멀 딥블랙 & 네온 사이드 라인 */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebarContent"] {
        background: linear-gradient(180deg, #050811 0%, #090e1a 55%, #03060c 100%) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.28) !important;
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
        padding: 0.65rem 0.75rem 0.4rem 0.75rem !important;
    }

    /* 모든 직계 블록의 가로폭을 100%로 통일하고 일정한 6px 간격 유지 */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 6px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* 2. 상단 GATEKEEPER 타이틀: 박스 테두리를 없애고 깔끔한 섹션 인덱스로 표현 */
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        background: transparent !important;
        border: none !important;
        border-bottom: 1.5px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 0 !important;
        padding: 2px 2px 6px 2px !important;
        margin: 0 0 4px 0 !important;
        color: #f8fafc !important;
        font-size: 13px !important;
        font-weight: 900 !important;
        letter-spacing: 0.5px !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    section[data-testid="stSidebar"] h2::after,
    section[data-testid="stSidebar"] h3::after {
        content: "SYS-GATE";
        font-size: 9px;
        font-weight: 800;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* 3. 알림창(stAlert)도 무거운 박스 대신 좌측 엣지 바가 달린 미니멀 배너로 통일 */
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: rgba(244, 63, 94, 0.08) !important;
        border: 1px solid rgba(244, 63, 94, 0.28) !important;
        border-left: 3px solid #f43f5e !important;
        border-radius: 8px !important;
        padding: 7px 10px !important;
        margin: 0 !important;
        box-shadow: none !important;
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
        font-size: 11px !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
        color: #fda4af !important;
        white-space: normal !important;
    }

    /* 4. 보안 PIN 설정 Expander: 100% 폭 슬림 바 */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(148, 163, 184, 0.22) !important;
        border-radius: 8px !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
        padding: 6px 10px !important;
        min-height: 32px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
        font-size: 11.5px !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }

    /* 5. 2x2 택티컬 모듈 그리드 타일 (체크박스를 정사각 대칭 타일로 변환) */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        gap: 6px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="column"] {
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        width: 100% !important;
        box-sizing: border-box !important;
        background: rgba(15, 23, 42, 0.78) !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-top: 2.5px solid #10b981 !important;
        border-radius: 8px !important;
        padding: 7px 8px !important;
        margin: 0 !important;
        min-height: 44px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05) !important;
        transition: all 0.18s ease !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"]:hover {
        background: rgba(30, 41, 59, 0.9) !important;
        border-color: #38bdf8 !important;
        border-top-color: #fbbf24 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p {
        font-size: 11px !important;
        font-weight: 800 !important;
        line-height: 1.22 !important;
        color: #f1f5f9 !important;
        white-space: nowrap !important;
        letter-spacing: -0.3px !important;
    }

    /* 6. 구분선 제거 (일체감을 위해 투명 여백으로 대체) */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        height: 1px !important;
        background: rgba(148, 163, 184, 0.15) !important;
        margin: 4px 0 !important;
    }
    </style>
    """


def build_sidebar_4d_tesseract_html(active_count: int = 4) -> str:
    """
    일체형 콕핏 레이더 & 3대 트랙 실시간 비교 게이지 바 (들쭉날쭉한 외곽 박스 없이 100% 폭 일치)
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
  body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
  .cockpit-panel {{
    width: 100%;
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.85) 0%, rgba(6, 11, 20, 0.95) 100%);
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 10px;
    padding: 10px 11px;
  }}
  .hdr-line {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 8px; padding-bottom: 5px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.14);
  }}
  .hdr-title {{ font-size: 11px; font-weight: 900; color: #e2e8f0; letter-spacing: 0.3px; }}
  .hdr-status {{
    font-size: 9.5px; font-weight: 800; color: #34d399;
    background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 1.5px 7px; border-radius: 999px;
  }}
  .viz-row {{
    display: grid; grid-template-columns: 92px 1fr; gap: 10px; align-items: center;
  }}
  #tesseractCanvas {{
    width: 92px; height: 92px; display: block;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.12) 0%, rgba(2, 6, 23, 0.8) 75%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 8px;
  }}
  .bars-col {{
    display: flex; flex-direction: column; gap: 7px;
  }}
  .bar-item {{
    background: rgba(2, 6, 23, 0.55);
    border: 1px solid rgba(51, 65, 85, 0.6);
    border-radius: 6px; padding: 4px 7px;
  }}
  .bar-top {{
    display: flex; justify-content: space-between; font-size: 10px; font-weight: 800; margin-bottom: 3px;
  }}
  .track-bg {{
    width: 100%; height: 4px; background: #0f172a; border-radius: 999px; overflow: hidden;
  }}
  .track-fill {{ height: 100%; border-radius: 999px; }}
</style>
</head>
<body>
<div class="cockpit-panel">
  <div class="hdr-line">
    <span class="hdr-title">🪐 QUANTUM TELEMETRY</span>
    <span class="hdr-status">● {active_count}/4 ONLINE</span>
  </div>
  <div class="viz-row">
    <canvas id="tesseractCanvas"></canvas>
    <div class="bars-col">
      <div class="bar-item">
        <div class="bar-top">
          <span style="color:#cbd5e1;">👑 M5 양자코어</span>
          <span style="color:#38bdf8;">100.09% (#238)</span>
        </div>
        <div class="track-bg"><div class="track-fill" style="width:78%;background:#38bdf8;"></div></div>
      </div>
      <div class="bar-item">
        <div class="bar-top">
          <span style="color:#cbd5e1;">🛡️ EGR 강건방어</span>
          <span style="color:#fbbf24;">100.11% (Q50)</span>
        </div>
        <div class="track-bg"><div class="track-fill" style="width:88%;background:#fbbf24;"></div></div>
      </div>
      <div class="bar-item">
        <div class="bar-top">
          <span style="color:#cbd5e1;">⚡ LATTICE 확률장</span>
          <span style="color:#34d399;">100.06% (#338)</span>
        </div>
        <div class="track-bg"><div class="track-fill" style="width:68%;background:#10b981;"></div></div>
      </div>
    </div>
  </div>
</div>

<script>
// 상단 잠금 배지도 100% 폭 미니멀 캡슐로 통일
function unifyTopBadge() {{
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
          el.style.margin = '0';
          el.style.borderRadius = '8px';
          el.style.fontWeight = '800';
          el.style.fontSize = '11px';
          el.style.textAlign = 'center';
          el.style.background = txt.includes('잠김') ? 'rgba(244, 63, 94, 0.12)' : 'rgba(16, 185, 129, 0.12)';
          el.style.border = txt.includes('잠김') ? '1px solid rgba(244, 63, 94, 0.35)' : '1px solid rgba(16, 185, 129, 0.35)';
          el.style.color = txt.includes('잠김') ? '#fda4af' : '#6ee7b7';
          el.style.boxShadow = 'none';
        }}
      }}
    }});
  }} catch (e) {{}}
}}
unifyTopBadge();
setInterval(unifyTopBadge, 700);

const canvas = document.getElementById('tesseractCanvas');
const ctx = canvas.getContext('2d');
function resize() {{
  const dpr = window.devicePixelRatio || 1;
  canvas.width = 92 * dpr;
  canvas.height = 92 * dpr;
  ctx.scale(dpr, dpr);
}}
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
function render4D() {{
  angle += 0.024;
  ctx.clearRect(0, 0, 92, 92);
  const cx = 46, cy = 46;

  ctx.beginPath();
  ctx.arc(cx, cy, 36, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(56, 189, 248, 0.18)';
  ctx.lineWidth = 1;
  ctx.stroke();

  const cosA = Math.cos(angle), sinA = Math.sin(angle);
  const cosB = Math.cos(angle * 0.7), sinB = Math.sin(angle * 0.7);

  const pts = vertices4D.map(v => {{
    let x = v[0], y = v[1], z = v[2], w4 = v[3];
    let nx = x * cosA - w4 * sinA, nw = x * sinA + w4 * cosA;
    let ny = y * cosB - z * sinB, nz = y * sinB + z * cosB;
    let fx = nx * cosB - ny * sinB, fy = nx * sinB + ny * cosB;
    const wf = 1 / (2.6 - nw * 0.65);
    const zf = 1 / (2.4 - nz * wf);
    return {{ x: cx + fx * wf * zf * 34, y: cy + fy * wf * zf * 34, w4: nw }};
  }});

  edges.forEach(e => {{
    const p1 = pts[e[0]], p2 = pts[e[1]];
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.strokeStyle = (p1.w4 + p2.w4) > 0 ? 'rgba(56, 189, 248, 0.85)' : 'rgba(251, 191, 36, 0.65)';
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }});

  requestAnimationFrame(render4D);
}}
requestAnimationFrame(render4D);
</script>
</body>
</html>"""
