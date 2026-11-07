import json
from typing import Dict


def build_tactical_sniper_arena_html(
    m5_bid: int,
    egr_bid: int,
    lat_bid: int,
    lower_cut: int,
    net_cost_98: int,
    n_rivals: int = 48,
) -> str:
    """
    [1] 3대 트랙(M5 · EGR-BID · LATTICE-1365) vs N개 경쟁사 실시간 스나이퍼 탄착 배틀 시뮬레이터
    """
    egr_val = egr_bid if egr_bid and egr_bid > 0 else m5_bid + 617624
    lat_val = lat_bid if lat_bid and lat_bid > 0 else m5_bid - 796054

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', 'Malgun Gothic', sans-serif; }}
  body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
  .arena-box {{
    background: radial-gradient(circle at 50% 50%, #0f172a 0%, #060b14 70%, #020617 100%);
    border: 1.5px solid #f43f5e; border-radius: 14px; padding: 14px 18px;
    box-shadow: 0 0 30px rgba(244, 63, 94, 0.18);
  }}
  .arena-hdr {{
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid rgba(244, 63, 94, 0.25); padding-bottom: 8px; margin-bottom: 10px;
  }}
  .badge-red {{
    background: linear-gradient(90deg, #f43f5e, #fb923c); color: #020617;
    font-size: 11px; font-weight: 900; padding: 3px 10px; border-radius: 999px;
  }}
  .btn-fire {{
    background: linear-gradient(135deg, #f43f5e, #e11d48); color: #fff;
    border: none; padding: 6px 14px; border-radius: 999px; font-size: 12px;
    font-weight: 800; cursor: pointer; box-shadow: 0 0 14px rgba(244, 63, 94, 0.6);
  }}
  .btn-fire:hover {{ transform: scale(1.05); }}
  #sniperCanvas {{
    width: 100%; height: 250px; display: block;
    background: rgba(2, 6, 23, 0.85); border: 1px solid #1e293b; border-radius: 10px;
  }}
  .hud-bar {{
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;
  }}
  .hud-item {{
    background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-radius: 8px;
    padding: 8px 12px; display: flex; justify-content: space-between; align-items: center;
  }}
</style>
</head>
<body>
<div class="arena-box">
  <div class="arena-hdr">
    <div>
      <span class="badge-red">TACTICAL SNIPER BATTLE ARENA</span>
      <span style="font-size:16px;font-weight:900;margin-left:8px;">🎯 3대 엔진 vs 경쟁사({n_rivals}개사) 실시간 개찰 탄착 시뮬레이터</span>
    </div>
    <button class="btn-fire" onclick="resetBattle()">🔥 경쟁사 탄착 & 스나이퍼 재발사 (FIRE)</button>
  </div>
  <canvas id="sniperCanvas"></canvas>
  <div class="hud-bar">
    <div class="hud-item" style="border-left:4px solid #38bdf8;">
      <div>
        <div style="font-size:11px;color:#7dd3fc;font-weight:800;">👑 트랙 1: M5 양자스나이퍼</div>
        <div style="font-size:15px;font-weight:900;">{m5_bid:,}원</div>
      </div>
      <span id="m5RankBadge" style="background:rgba(56,189,248,0.2);color:#38bdf8;font-size:11px;font-weight:900;padding:4px 8px;border-radius:6px;">정밀 조준</span>
    </div>
    <div class="hud-item" style="border-left:4px solid #fbbf24;">
      <div>
        <div style="font-size:11px;color:#fcd34d;font-weight:800;">🛡️ 트랙 2: EGR-BID 방어선</div>
        <div style="font-size:15px;font-weight:900;color:#fbbf24;">{egr_val:,}원</div>
      </div>
      <span style="background:rgba(251,191,36,0.2);color:#fbbf24;font-size:11px;font-weight:900;padding:4px 8px;border-radius:6px;">하한방어 100%</span>
    </div>
    <div class="hud-item" style="border-left:4px solid #10b981;">
      <div>
        <div style="font-size:11px;color:#6ee7b7;font-weight:800;">⚡ 트랙 3: LATTICE-1365</div>
        <div style="font-size:15px;font-weight:900;color:#34d399;">{lat_val:,}원</div>
      </div>
      <span style="background:rgba(16,185,129,0.2);color:#34d399;font-size:11px;font-weight:900;padding:4px 8px;border-radius:6px;">최저가 돌파</span>
    </div>
  </div>
</div>
<script>
const canvas = document.getElementById('sniperCanvas');
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

let rivals = [];
let ripples = [];
let scanAngle = 0;
let startT = performance.now();

function resetBattle() {{
  const cw = canvas.width / window.devicePixelRatio;
  const ch = canvas.height / window.devicePixelRatio;
  const cutX = cw * 0.28; // 낙찰하한선 위치
  rivals = [];
  for (let i = 0; i < {n_rivals}; i++) {{
    // 경쟁사 탄착 분포 (일부는 하한선 미달 적색 데드존에 추락, 다수는 우측 상방에 분포)
    const isDead = Math.random() < 0.28;
    const targetX = isDead
      ? cutX * (0.25 + Math.random() * 0.72)
      : cutX + 18 + Math.pow(Math.random(), 1.35) * (cw - cutX - 40);
    const targetY = 35 + Math.random() * (ch - 75);
    rivals.push({{
      x: targetX, y: -20, tx: targetX, ty: targetY,
      delay: Math.random() * 1.4, landed: false, isDead: isDead
    }});
  }}
  ripples = [];
  startT = performance.now();
}}

function draw(now) {{
  const cw = canvas.width / window.devicePixelRatio;
  const ch = canvas.height / window.devicePixelRatio;
  const elapsed = (now - startT) / 1000;
  ctx.clearRect(0, 0, cw, ch);

  const cutX = cw * 0.28;
  // 1. 좌측 하한선 미달 데드존(적색 심연) 표시
  const deadGrad = ctx.createLinearGradient(0, 0, cutX, 0);
  deadGrad.addColorStop(0, 'rgba(225, 29, 72, 0.32)');
  deadGrad.addColorStop(1, 'rgba(225, 29, 72, 0.08)');
  ctx.fillStyle = deadGrad;
  ctx.fillRect(0, 0, cutX, ch);

  // 격자선
  ctx.strokeStyle = 'rgba(51, 65, 85, 0.35)';
  ctx.lineWidth = 1;
  for (let x = 40; x < cw; x += 60) {{ ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, ch); ctx.stroke(); }}
  for (let y = 30; y < ch; y += 45) {{ ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(cw, y); ctx.stroke(); }}

  // 낙찰하한선 레이저 펜스
  ctx.beginPath();
  ctx.moveTo(cutX, 0); ctx.lineTo(cutX, ch);
  ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 2.5; ctx.stroke();
  ctx.fillStyle = '#fda4af'; ctx.font = '800 11px Pretendard, sans-serif';
  ctx.fillText('⛔ 낙찰하한선 데드존 (미달 시 0점 탈락)', 10, 20);
  ctx.fillStyle = '#6ee7b7';
  ctx.fillText('✅ 적격 유효 투찰 구간 (하한선 직상단 최저가 승리) ➔', cutX + 12, 20);

  // 2. 경쟁사 탄착 애니메이션
  rivals.forEach(rv => {{
    if (elapsed > rv.delay) {{
      rv.y += (rv.ty - rv.y) * 0.18;
      if (!rv.landed && Math.abs(rv.ty - rv.y) < 3) {{
        rv.landed = true;
        ripples.push({{ x: rv.tx, y: rv.ty, r: 2, a: 0.75, c: rv.isDead ? '#f43f5e' : '#64748b' }});
      }}
      ctx.beginPath();
      ctx.arc(rv.tx, rv.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = rv.isDead ? 'rgba(244, 63, 94, 0.65)' : 'rgba(148, 163, 184, 0.55)';
      ctx.fill();
    }}
  }});

  // 3. 3대 AI 모델 스나이퍼 조준선 락온 (LATTICE / M5 / EGR-BID)
  const models = [
    {{ name: '⚡ LATTICE-1365', x: cutX + 16, y: ch * 0.35, color: '#10b981', delay: 1.5 }},
    {{ name: '👑 M5 기준선(+19원)', x: cutX + 42, y: ch * 0.55, color: '#38bdf8', delay: 1.8 }},
    {{ name: '🛡️ EGR-BID 방어선', x: cutX + 78, y: ch * 0.74, color: '#fbbf24', delay: 2.1 }}
  ];

  scanAngle += 0.06;
  models.forEach(m => {{
    if (elapsed > m.delay) {{
      // 스나이퍼 조준경 회전 링
      ctx.save();
      ctx.translate(m.x, m.y);
      ctx.rotate(scanAngle);
      ctx.beginPath();
      ctx.arc(0, 0, 14, 0, Math.PI * 1.5);
      ctx.strokeStyle = m.color;
      ctx.lineWidth = 2.2;
      ctx.stroke();
      ctx.restore();

      // 십자선 및 중심 코어
      ctx.beginPath();
      ctx.moveTo(m.x - 20, m.y); ctx.lineTo(m.x + 20, m.y);
      ctx.moveTo(m.x, m.y - 20); ctx.lineTo(m.x, m.y + 20);
      ctx.strokeStyle = m.color; ctx.lineWidth = 1.2; ctx.stroke();

      ctx.beginPath();
      ctx.arc(m.x, m.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = m.color; ctx.fill();

      // 라벨 태그
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(m.x + 16, m.y - 11, 128, 22);
      ctx.strokeStyle = m.color;
      ctx.strokeRect(m.x + 16, m.y - 11, 128, 22);
      ctx.fillStyle = m.color;
      ctx.font = '900 11px Pretendard, sans-serif';
      ctx.fillText(m.name, m.x + 22, m.y + 4);
    }}
  }});

  // 충격파 링 업데이트
  ripples.forEach(rp => {{
    ctx.beginPath(); ctx.arc(rp.x, rp.y, rp.r, 0, Math.PI * 2);
    ctx.strokeStyle = rp.c; ctx.globalAlpha = Math.max(0, rp.a);
    ctx.lineWidth = 1.8; ctx.stroke(); ctx.globalAlpha = 1.0;
    rp.r += 1.8; rp.a -= 0.03;
  }});
  ripples = ripples.filter(rp => rp.a > 0);

  requestAnimationFrame(draw);
}}
resetBattle();
requestAnimationFrame(draw);
</script>
</body>
</html>"""


def build_egr_shield_matrix_html(q_map: Dict, status_str: str, egr_bid: int, min_nc_98: int) -> str:
    """
    [2] 번외 1 (EGR-BID) 전용: 발주기관 사정률 변동 파동(Q10~Q90) vs M8 5중 에너지 방어 쉴드 애니메이션
    """
    q10 = q_map.get("q10", "100.0500")
    q50 = q_map.get("q50", "100.1100")
    q90 = q_map.get("q90", "100.1400")
    bid_disp = f"{egr_bid:,}원" if egr_bid else "HOLD (보류)"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }}
  body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
  .shield-wrap {{
    background: linear-gradient(135deg, #090d16 0%, #1e1b4b 55%, #090d16 100%);
    border: 1.5px solid #f59e0b; border-radius: 14px; padding: 14px 18px;
    box-shadow: 0 0 28px rgba(245, 158, 11, 0.2);
  }}
  #shieldCanvas {{
    width: 100%; height: 210px; display: block;
    background: rgba(2, 6, 23, 0.85); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px;
    margin-top: 8px;
  }}
</style>
</head>
<body>
<div class="shield-wrap">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <span style="background:#f59e0b;color:#020617;font-size:11px;font-weight:900;padding:3px 9px;border-radius:999px;">M6·M7·M8 ROBUST SHIELD DYNAMICS</span>
      <span style="font-size:15.5px;font-weight:900;margin-left:8px;">🛡️ EGR-BID 발주처 사정률 충격파(Q10~Q90) 5중 방어 배리어 시뮬레이터</span>
    </div>
    <span style="font-size:12px;color:#fcd34d;font-weight:800;">방어 타점: {bid_disp} ({status_str})</span>
  </div>
  <canvas id="shieldCanvas"></canvas>
</div>
<script>
const canvas = document.getElementById('shieldCanvas');
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

let waves = [];
let sparks = [];
let tick = 0;

function animateShield() {{
  const cw = canvas.width / window.devicePixelRatio;
  const ch = canvas.height / window.devicePixelRatio;
  tick++;
  ctx.clearRect(0, 0, cw, ch);

  if (tick % 38 === 0) {{
    waves.push({{ x: 20, y: ch / 2, r: 15, speed: 3.4, label: ['Q10({q10}%)', 'Q25', 'Q50({q50}%)', 'Q75', 'Q90({q90}%)'][ (tick/38)%5 | 0 ] }});
  }}

  const shieldX = cw * 0.68;

  // 우측 M8 헥사곤 골드 에너지 배리어
  for (let i = 0; i < 3; i++) {{
    ctx.beginPath();
    ctx.arc(shieldX + 90, ch / 2, 110 + i * 14, Math.PI * 0.72, Math.PI * 1.28);
    ctx.strokeStyle = i === 0 ? '#fbbf24' : 'rgba(245, 158, 11, 0.35)';
    ctx.lineWidth = i === 0 ? 4 : 2;
    ctx.shadowColor = '#f59e0b';
    ctx.shadowBlur = i === 0 ? 18 : 0;
    ctx.stroke();
    ctx.shadowBlur = 0;
  }}

  ctx.fillStyle = '#fbbf24';
  ctx.font = '900 12px Pretendard, sans-serif';
  ctx.fillText('🛡️ EGR-BID Q50 강건 방어막', shieldX + 8, 28);
  ctx.fillStyle = '#e2e8f0';
  ctx.font = '700 11px Pretendard, sans-serif';
  ctx.fillText('• 시나리오 적격 통과율: 60% 이상 보장', shieldX + 8, ch / 2 - 8);
  ctx.fillText('• 98% 원가 배제선: {min_nc_98:,}원 방어', shieldX + 8, ch / 2 + 14);

  // 좌측에서 밀려오는 발주처 사정률 변동 파동
  waves.forEach(wv => {{
    wv.x += wv.speed;
    ctx.beginPath();
    ctx.arc(wv.x - 40, ch / 2, 55, -0.45, 0.45);
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.fillStyle = '#7dd3fc';
    ctx.font = '800 10px Pretendard, sans-serif';
    ctx.fillText('🌊 ' + wv.label, wv.x - 25, ch / 2 - 38);

    // 방어막 충돌 시 스파크 생성
    if (Math.abs(wv.x - (shieldX - 20)) < 4) {{
      for (let s = 0; s < 14; s++) {{
        sparks.push({{
          x: shieldX - 18,
          y: ch / 2 + (Math.random() - 0.5) * 70,
          vx: -1.5 - Math.random() * 3,
          vy: (Math.random() - 0.5) * 4,
          alpha: 1.0
        }});
      }}
    }}
  }});
  waves = waves.filter(wv => wv.x < shieldX - 15);

  sparks.forEach(sp => {{
    sp.x += sp.vx; sp.y += sp.vy; sp.alpha -= 0.04;
    ctx.beginPath(); ctx.arc(sp.x, sp.y, 2.5, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(251, 191, 36, ${{Math.max(0, sp.alpha)}})`;
    ctx.fill();
  }});
  sparks = sparks.filter(sp => sp.alpha > 0);

  requestAnimationFrame(animateShield);
}}
requestAnimationFrame(animateShield);
</script>
</body>
</html>"""


def build_lattice_wave_rider_html(
    opt_step: int,
    opt_price: int,
    exp_profit: int,
    p_miss_pct: float,
    eff_floor_pct: float,
) -> str:
    """
    [3] 번외 2 (LATTICE-1365) 전용: 1,365 계단 확률장 오로라 파도 & 기대이익 골든 피크(Golden Peak) 락온 애니메이션
    """
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }}
  body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
  .wave-wrap {{
    background: linear-gradient(135deg, #022c22 0%, #090d16 60%, #064e3b 100%);
    border: 1.5px solid #10b981; border-radius: 14px; padding: 14px 18px;
    box-shadow: 0 0 28px rgba(16, 185, 129, 0.22);
  }}
  #waveCanvas {{
    width: 100%; height: 215px; display: block;
    background: rgba(2, 6, 23, 0.85); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px;
    margin-top: 8px;
  }}
</style>
</head>
<body>
<div class="wave-wrap">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <span style="background:#10b981;color:#020617;font-size:11px;font-weight:900;padding:3px 9px;border-radius:999px;">L0~L5 LADDER PROBABILITY WAVE</span>
      <span style="font-size:15.5px;font-weight:900;margin-left:8px;">🌊 LATTICE-1365 계단 확률장 파동 & 기대이익 골든 피크(#{opt_step}) 서핑 엔진</span>
    </div>
    <span style="font-size:12px;color:#34d399;font-weight:800;">최적해: {opt_price:,}원 (실효하한 {eff_floor_pct:.3f}%)</span>
  </div>
  <canvas id="waveCanvas"></canvas>
</div>
<script>
const canvas = document.getElementById('waveCanvas');
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

let phase = 0;
function animateWave() {{
  const cw = canvas.width / window.devicePixelRatio;
  const ch = canvas.height / window.devicePixelRatio;
  phase += 0.045;
  ctx.clearRect(0, 0, cw, ch);

  const peakRatio = Math.min(0.82, Math.max(0.22, {opt_step} / 1365.0 + 0.18));
  const peakX = cw * peakRatio;

  // 68개의 양자 계단 바를 실시간 사인파 + 가우시안 기대이익 봉우리로 렌더링
  const nBars = 68;
  const barW = (cw - 40) / nBars;
  let peakY = ch * 0.3;

  for (let i = 0; i < nBars; i++) {{
    const x = 20 + i * barW;
    const norm = i / nBars;
    const dist = (norm - peakRatio) / 0.18;
    const profitEnv = Math.exp(-0.5 * dist * dist);
    const waveOsc = Math.sin(norm * 10 - phase) * 8 + Math.cos(norm * 22 + phase * 1.3) * 4;
    const barH = Math.max(12, profitEnv * (ch * 0.62) + waveOsc + 18);
    const y = ch - 24 - barH;

    if (Math.abs(norm - peakRatio) < 0.015) peakY = y;

    if (norm < 0.18) {{
      ctx.fillStyle = 'rgba(244, 63, 94, 0.55)'; // 좌측 적격 탈락 구간
    }} else if (Math.abs(norm - peakRatio) < 0.04) {{
      ctx.fillStyle = '#fbbf24'; // 골든 피크 최적 계단
    }} else {{
      ctx.fillStyle = `rgba(16, 185, 129, ${{0.25 + profitEnv * 0.65}})`;
    }}
    ctx.fillRect(x, y, barW - 2, barH);
  }}

  // 골든 피크 락온 비콘 및 레이저 마커
  ctx.beginPath();
  ctx.arc(peakX, peakY - 12, 8 + Math.sin(phase * 2) * 3, 0, Math.PI * 2);
  ctx.strokeStyle = '#fbbf24';
  ctx.lineWidth = 2.5;
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(peakX, peakY - 12, 4, 0, Math.PI * 2);
  ctx.fillStyle = '#fbbf24';
  ctx.fill();

  ctx.fillStyle = '#fef08a';
  ctx.font = '900 11.5px Pretendard, sans-serif';
  ctx.fillText('⚡ GOLDEN PEAK 계단 #{opt_step}/1,365 (기대이익 극대점)', Math.max(20, peakX - 110), Math.max(20, peakY - 26));

  ctx.fillStyle = '#fda4af';
  ctx.font = '700 10.5px Pretendard, sans-serif';
  ctx.fillText('◀ L4 수행능력 부적격 절벽', 20, ch - 7);
  ctx.fillStyle = '#6ee7b7';
  ctx.fillText('1,365개 복수예가 계단 격자 (W_j × 마진 기대이익장) ▶', cw - 270, ch - 7);

  requestAnimationFrame(animateWave);
}}
requestAnimationFrame(animateWave);
</script>
</body>
</html>"""
