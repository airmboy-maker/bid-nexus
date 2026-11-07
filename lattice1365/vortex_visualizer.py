import json
from typing import Dict


def build_quantum_lotto_vortex_html(ai_sel: Dict, target_model_label: str, target_ep: int, base_amt: int) -> str:
    """
    창의적 애니메이션이 적용된 15C4 복수예가 추첨 시뮬레이터:
    - 3D Orbital Vortex Chamber (15개 예비가격 에너지 구체 실시간 3D 회전)
    - Sequential Lock-On Chamber (4개 추첨 번호 순차 도킹 + 쇼크웨이브 파동)
    - Best 2-Pick Neon Spotlight (나라장터 투찰창 체크용 1순위 2개 번호 홀로그램 강조)
    """
    p2 = ai_sel["primary_2_pick"]
    b2 = ai_sel["backup_2_pick"]
    c4 = ai_sel["exact_combo_4"]
    step_no = ai_sel["exact_step_no"]
    slot_data_json = json.dumps(ai_sel["slot_table"], ensure_ascii=False)
    c4_json = json.dumps(c4)
    p2_json = json.dumps(p2)
    b2_json = json.dumps(b2)
    rate_pct = round((target_ep / float(base_amt)) * 100.0, 4) if base_amt > 0 else 100.0

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', 'Malgun Gothic', sans-serif; }}
  body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
  .vortex-wrap {{
    background: radial-gradient(circle at 30% 45%, #0f172a 0%, #090d16 65%, #020617 100%);
    border: 1.5px solid #38bdf8;
    border-radius: 16px;
    padding: 16px 20px;
    position: relative;
    box-shadow: 0 0 35px rgba(56, 189, 248, 0.18), inset 0 0 40px rgba(16, 185, 129, 0.08);
  }}
  .vortex-header {{
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    padding-bottom: 10px; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;
  }}
  .vortex-badge {{
    background: linear-gradient(90deg, #0ea5e9, #10b981);
    color: #020617; font-weight: 900; font-size: 11px;
    padding: 3px 10px; border-radius: 999px; letter-spacing: 0.8px;
  }}
  .vortex-title {{ font-size: 17px; font-weight: 900; color: #f8fafc; margin-left: 8px; }}
  .btn-replay {{
    background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
    color: #090d16; border: none; padding: 7px 16px; border-radius: 999px;
    font-size: 12.5px; font-weight: 900; cursor: pointer;
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.5);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }}
  .btn-replay:hover {{ transform: scale(1.05); box-shadow: 0 0 24px rgba(245, 158, 11, 0.85); }}
  .main-grid {{
    display: grid; grid-template-columns: 1.25fr 1fr; gap: 16px; align-items: stretch;
  }}
  .canvas-box {{
    position: relative; background: rgba(2, 6, 23, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px;
    height: 330px; overflow: hidden;
  }}
  #lottoCanvas {{ width: 100%; height: 100%; display: block; }}
  .hud-overlay {{
    position: absolute; top: 10px; left: 12px; pointer-events: none;
    font-size: 11.5px; color: #94a3b8; line-height: 1.5;
  }}
  .hud-status {{
    position: absolute; bottom: 10px; left: 12px; right: 12px;
    display: flex; justify-content: space-between; align-items: center;
    background: rgba(15, 23, 42, 0.82); border: 1px solid rgba(56, 189, 248, 0.25);
    padding: 6px 12px; border-radius: 8px; font-size: 12px;
  }}
  .right-panel {{
    display: flex; flex-direction: column; justify-content: space-between; gap: 10px;
  }}
  .chamber-card {{
    background: rgba(15, 23, 42, 0.85); border: 1px solid #334155;
    border-radius: 12px; padding: 12px 14px;
  }}
  .chamber-label {{
    font-size: 11.5px; font-weight: 800; color: #38bdf8;
    margin-bottom: 8px; display: flex; justify-content: space-between;
  }}
  .balls-row {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;
  }}
  .slot-tube {{
    background: radial-gradient(circle at 50% 30%, #1e293b, #090d16);
    border: 1.5px solid #475569; border-radius: 12px;
    padding: 10px 6px; text-align: center; position: relative;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  }}
  .slot-tube.locked {{
    border-color: #10b981;
    box-shadow: 0 0 18px rgba(16, 185, 129, 0.35);
    transform: translateY(-3px);
  }}
  .slot-tube.primary-pick {{
    border: 2px solid #f59e0b;
    background: radial-gradient(circle at 50% 25%, rgba(245, 158, 11, 0.28), #090d16 80%);
    box-shadow: 0 0 24px rgba(245, 158, 11, 0.55);
  }}
  .ball-sphere {{
    width: 46px; height: 46px; border-radius: 50%; margin: 0 auto 6px auto;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; font-weight: 900; color: #020617;
    background: radial-gradient(circle at 32% 30%, #ffffff, #38bdf8 55%, #0284c7 100%);
    box-shadow: inset -3px -3px 8px rgba(0,0,0,0.45), 0 0 12px rgba(56, 189, 248, 0.6);
  }}
  .slot-tube.primary-pick .ball-sphere {{
    background: radial-gradient(circle at 32% 30%, #fffbeb, #fbbf24 50%, #d97706 100%);
    box-shadow: inset -3px -3px 8px rgba(0,0,0,0.45), 0 0 18px rgba(251, 191, 36, 0.9);
  }}
  .pick-tag {{
    font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 4px;
    display: inline-block; margin-top: 3px;
  }}
  .tag-gold {{ background: #f59e0b; color: #020617; }}
  .tag-cyan {{ background: rgba(56, 189, 248, 0.2); color: #7dd3fc; border: 1px solid #38bdf8; }}
  .pick-box-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
  }}
  .Action-card {{
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
    border-radius: 10px; padding: 11px 12px; border-left: 4px solid #f59e0b;
  }}
  .Action-card.backup {{ border-left-color: #38bdf8; }}
  .mini-grid-15 {{
    display: grid; grid-template-columns: repeat(15, 1fr); gap: 4px; margin-top: 6px;
  }}
  .mini-cell {{
    background: #0f172a; border: 1px solid #334155; border-radius: 5px;
    text-align: center; padding: 4px 0; font-size: 11px; font-weight: 700; color: #64748b;
    transition: all 0.25s ease;
  }}
  .mini-cell.active-4 {{
    background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #34d399;
  }}
  .mini-cell.active-2 {{
    background: #f59e0b; border-color: #fde68a; color: #020617; font-weight: 900;
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.8); transform: scale(1.08);
  }}
</style>
</head>
<body>
<div class="vortex-wrap">
  <div class="vortex-header">
    <div>
      <span class="vortex-badge">QUANTUM 15C4 VORTEX SIMULATOR</span>
      <span class="vortex-title">🎯 복수예가 15개 슬롯 양자 궤도 추첨 & 최적 2픽(Best 2-Pick) 락온 엔진</span>
    </div>
    <button class="btn-replay" onclick="startQuantumDraw()">⚡ 실시간 양자 추첨 재가동 (LIVE DRAW)</button>
  </div>

  <div class="main-grid">
    <!-- 좌측: 60FPS 3D 궤도 와류 & 양자 락온 캔버스 -->
    <div class="canvas-box">
      <canvas id="lottoCanvas"></canvas>
      <div class="hud-overlay">
        <div>• <b>타점 기준:</b> <span style="color:#38bdf8;">{target_model_label}</span></div>
        <div>• <b>양자 계단:</b> <span style="color:#34d399;">#{step_no} / 1,365 조합</span></div>
        <div>• <b>물리 모드:</b> 3D Orbital Gravity + Crowd Bias</div>
      </div>
      <div class="hud-status">
        <span id="simPhaseText" style="color:#fbbf24;font-weight:800;">⚡ 양자 와류 추첨 가동 중...</span>
        <span style="color:#e2e8f0;font-weight:800;">목표 예가: <span id="counterEp" style="color:#34d399;">{target_ep:,}</span>원 ({rate_pct:.4f}%)</span>
      </div>
    </div>

    <!-- 우측: 4개 추첨 챔버 도킹 슬롯 & 나라장터 실전 2픽 지시판 -->
    <div class="right-panel">
      <div class="chamber-card">
        <div class="chamber-label">
          <span>🍀 [15C4 추첨 챔버] 목표 예정가격 달성 4개 슬롯 도킹</span>
          <span id="lockProgress" style="color:#10b981;">4 / 4 LOCKED</span>
        </div>
        <div class="balls-row" id="tubesContainer"></div>
      </div>

      <div class="pick-box-grid">
        <div class="Action-card">
          <div style="font-size:11px;color:#fcd34d;font-weight:800;">👑 나라장터 투찰창 1순위 체크 (Best 2-Pick)</div>
          <div style="font-size:22px;font-weight:900;color:#ffffff;margin:3px 0;">{p2[0]}번 · {p2[1]}번</div>
          <div style="font-size:11px;color:#94a3b8;">다수결 중앙 선호도 + 목표계단 동조율 1위</div>
        </div>
        <div class="Action-card backup">
          <div style="font-size:11px;color:#7dd3fc;font-weight:800;">🛡️ 2순위 예비 교차 번호 (Backup 2-Pick)</div>
          <div style="font-size:22px;font-weight:900;color:#38bdf8;margin:3px 0;">{b2[0]}번 · {b2[1]}번</div>
          <div style="font-size:11px;color:#94a3b8;">공동도급/분산 투찰 시 서브 체크 번호</div>
        </div>
      </div>

      <div class="chamber-card" style="padding:9px 12px;">
        <div style="display:flex;justify-content:space-between;font-size:11px;color:#94a3b8;">
          <span>📊 <b>1~15번 전체 슬롯 실시간 스펙트럼</b> (골드=1순위 2픽 / 에메랄드=4개 추첨조합)</span>
          <span style="color:#fbbf24;font-weight:800;">투찰 시 [{p2[0]}번, {p2[1]}번] 선택</span>
        </div>
        <div class="mini-grid-15" id="miniGrid15"></div>
      </div>
    </div>
  </div>
</div>

<script>
const slotTable = {slot_data_json};
const target4 = {c4_json};
const primary2 = {p2_json};
const backup2 = {b2_json};
const targetEp = {target_ep};

const canvas = document.getElementById('lottoCanvas');
const ctx = canvas.getContext('2d');
let width, height;
function resizeCanvas() {{
  const rect = canvas.parentElement.getBoundingClientRect();
  width = canvas.width = rect.width * window.devicePixelRatio;
  height = canvas.height = rect.height * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
}}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// 15개 에너지 볼 초기화
let balls = [];
let shockwaves = [];
let lockedCount = 0;
let startTime = performance.now();

function initSimulation() {{
  const w = canvas.width / window.devicePixelRatio;
  const h = canvas.height / window.devicePixelRatio;
  balls = slotTable.map((s, idx) => {{
    const num = s.slot_no;
    const isTarget4 = target4.includes(num);
    const isPrimary2 = primary2.includes(num);
    const angle = (idx / 15) * Math.PI * 2;
    return {{
      num: num,
      prob: s["AI 다수결 선택확률(%)"],
      sRate: s["사정률(%)"],
      isTarget4: isTarget4,
      isPrimary2: isPrimary2,
      targetOrder: target4.indexOf(num),
      angle: angle,
      radiusX: 70 + (idx % 3) * 32,
      radiusY: 42 + (idx % 3) * 20,
      speed: 0.028 + (idx % 5) * 0.006,
      x: w / 2 + Math.cos(angle) * 90,
      y: h / 2 + Math.sin(angle) * 50,
      z: 0,
      locked: false,
      lockX: 0,
      lockY: 0
    }};
  }});
  shockwaves = [];
  lockedCount = 0;
  startTime = performance.now();
  renderTubes(0);
  renderMiniGrid(0);
}}

function renderTubes(lockedStep) {{
  const container = document.getElementById('tubesContainer');
  container.innerHTML = '';
  target4.forEach((num, idx) => {{
    const isLocked = idx < lockedStep;
    const isP2 = primary2.includes(num);
    const sInfo = slotTable[num - 1];
    const tube = document.createElement('div');
    tube.className = 'slot-tube' + (isLocked ? ' locked' : '') + (isLocked && isP2 ? ' primary-pick' : '');
    tube.innerHTML = `
      <div class="ball-sphere" style="opacity:${{isLocked ? '1' : '0.25'}};transform:scale(${{isLocked ? '1' : '0.75'}});">
        ${{isLocked ? num : '?'}}
      </div>
      <div style="font-size:11px;font-weight:800;color:#e2e8f0;">${{isLocked ? sInfo['사정률(%)'].toFixed(3) + '%' : '스캐닝...'}}</div>
      <div style="font-size:10px;color:#94a3b8;">확률 ${{sInfo['AI 다수결 선택확률(%)']}}%</div>
      <span class="pick-tag ${{isP2 ? 'tag-gold' : 'tag-cyan'}}">${{isP2 ? '👑 1순위 체크' : '🍀 추첨조합'}}</span>
    `;
    container.appendChild(tube);
  }});
  document.getElementById('lockProgress').innerText = `${{lockedStep}} / 4 LOCKED`;
}}

function renderMiniGrid(lockedStep) {{
  const g = document.getElementById('miniGrid15');
  g.innerHTML = '';
  for (let n = 1; n <= 15; n++) {{
    const d = document.createElement('div');
    const idxIn4 = target4.indexOf(n);
    const isUnlocked4 = idxIn4 !== -1 && idxIn4 < lockedStep;
    const isP2 = primary2.includes(n) && isUnlocked4;
    d.className = 'mini-cell' + (isP2 ? ' active-2' : (isUnlocked4 ? ' active-4' : ''));
    d.innerText = n + '번';
    g.appendChild(d);
  }}
}}

function startQuantumDraw() {{
  initSimulation();
}}

function animate(now) {{
  const w = canvas.width / window.devicePixelRatio;
  const h = canvas.height / window.devicePixelRatio;
  const elapsed = (now - startTime) / 1000;

  ctx.clearRect(0, 0, w, h);

  // 배경 양자 중력장 링 그리기
  const cx = w * 0.5;
  const cy = h * 0.48;
  for (let r = 35; r <= 135; r += 32) {{
    ctx.beginPath();
    ctx.ellipse(cx, cy, r * 1.35, r * 0.72, 0, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.14)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }}

  // 단계별 락온 진행 (0.6초 간격으로 4개 번호 순차 락온)
  let newLockedCount = 0;
  if (elapsed > 0.7) newLockedCount = 1;
  if (elapsed > 1.25) newLockedCount = 2;
  if (elapsed > 1.8) newLockedCount = 3;
  if (elapsed > 2.35) newLockedCount = 4;

  if (newLockedCount !== lockedCount) {{
    lockedCount = newLockedCount;
    renderTubes(lockedCount);
    renderMiniGrid(lockedCount);
    // 락온 순간 쇼크웨이브 발생
    const lockedNum = target4[lockedCount - 1];
    const bObj = balls.find(b => b.num === lockedNum);
    if (bObj) {{
      shockwaves.push({{ x: cx, y: cy, r: 10, alpha: 1.0, color: bObj.isPrimary2 ? '#f59e0b' : '#10b981' }});
    }}
  }}

  const phaseEl = document.getElementById('simPhaseText');
  if (lockedCount < 4) {{
    phaseEl.innerHTML = `🌀 [PHASE ${{lockedCount+1}}/4] 다수결 편향 중력장 스캐닝... (${{target4[lockedCount]}}번 슬롯 락온 중)`;
  }} else {{
    phaseEl.innerHTML = `✅ [LOCK-ON 완료] 최적 2픽 【 ${{primary2[0]}}번 · ${{primary2[1]}}번 】 & 4개 조합 도킹 확정!`;
  }}

  // 락온된 공들의 목표 좌표 (캔버스 상단 아치형 배치)
  const archPositions = [
    {{ x: cx - 105, y: cy - 18 }},
    {{ x: cx - 35,  y: cy - 38 }},
    {{ x: cx + 35,  y: cy - 38 }},
    {{ x: cx + 105, y: cy - 18 }}
  ];

  // 공 위치 업데이트
  balls.forEach(b => {{
    const isNowLocked = b.isTarget4 && b.targetOrder < lockedCount;
    b.locked = isNowLocked;
    if (isNowLocked) {{
      const targetPos = archPositions[b.targetOrder];
      b.x += (targetPos.x - b.x) * 0.14;
      b.y += (targetPos.y - b.y) * 0.14;
      b.z = 1.2;
    }} else {{
      const speedMult = lockedCount < 4 ? 1.8 : 0.65;
      b.angle += b.speed * speedMult;
      b.x = cx + Math.cos(b.angle) * b.radiusX * 1.25;
      b.y = cy + Math.sin(b.angle) * b.radiusY * 1.15;
      b.z = Math.sin(b.angle);
    }}
  }});

  // 락온된 공들 사이에 시너지 레이저 네트워크 선 그리기
  const lockedBalls = balls.filter(b => b.locked).sort((a, b) => a.targetOrder - b.targetOrder);
  if (lockedBalls.length >= 2) {{
    ctx.beginPath();
    for (let i = 0; i < lockedBalls.length; i++) {{
      for (let j = i + 1; j < lockedBalls.length; j++) {{
        ctx.moveTo(lockedBalls[i].x, lockedBalls[i].y);
        ctx.lineTo(lockedBalls[j].x, lockedBalls[j].y);
      }}
    }}
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.45)';
    ctx.lineWidth = 1.8;
    ctx.stroke();
  }}

  // 쇼크웨이브 애니메이션
  shockwaves.forEach(sw => {{
    ctx.beginPath();
    ctx.arc(sw.x, sw.y, sw.r, 0, Math.PI * 2);
    ctx.strokeStyle = sw.color;
    ctx.globalAlpha = Math.max(0, sw.alpha);
    ctx.lineWidth = 2.5;
    ctx.stroke();
    ctx.globalAlpha = 1.0;
    sw.r += 4.2;
    sw.alpha -= 0.03;
  }});
  shockwaves = shockwaves.filter(sw => sw.alpha > 0);

  // Z-축 깊이순 정렬 후 15개 구체 렌더링
  const sortedBalls = [...balls].sort((a, b) => a.z - b.z);
  sortedBalls.forEach(b => {{
    const radius = b.locked ? (b.isPrimary2 ? 22 : 19) : (12 + (b.z + 1) * 2.2);
    ctx.save();
    ctx.beginPath();
    ctx.arc(b.x, b.y, radius, 0, Math.PI * 2);

    const grad = ctx.createRadialGradient(b.x - radius * 0.3, b.y - radius * 0.3, 2, b.x, b.y, radius);
    if (b.locked && b.isPrimary2) {{
      grad.addColorStop(0, '#fffbeb');
      grad.addColorStop(0.5, '#fbbf24');
      grad.addColorStop(1, '#b45309');
      ctx.shadowColor = '#f59e0b';
      ctx.shadowBlur = 20;
    }} else if (b.locked) {{
      grad.addColorStop(0, '#ecfdf5');
      grad.addColorStop(0.5, '#10b981');
      grad.addColorStop(1, '#047857');
      ctx.shadowColor = '#10b981';
      ctx.shadowBlur = 15;
    }} else {{
      grad.addColorStop(0, '#e2e8f0');
      grad.addColorStop(0.5, '#334155');
      grad.addColorStop(1, '#0f172a');
      ctx.globalAlpha = lockedCount === 4 ? 0.38 : 0.78;
    }}

    ctx.fillStyle = grad;
    ctx.fill();
    ctx.restore();

    // 번호 텍스트
    ctx.fillStyle = b.locked ? '#020617' : '#cbd5e1';
    ctx.font = `900 ${{b.locked ? 13 : 10}}px Pretendard, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(b.num, b.x, b.y);
  }});

  requestAnimationFrame(animate);
}}

initSimulation();
requestAnimationFrame(animate);
</script>
</body>
</html>"""
