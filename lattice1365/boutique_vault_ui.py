from typing import Dict, Any, List


def get_boutique_vault_css() -> str:
    css = """
    <style>
    @keyframes goldShimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes cabinetReveal {
        from { opacity: 0; transform: translateY(10px) scale(0.99); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    .boutique-cart-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        background:
            radial-gradient(circle at 15% 50%, rgba(251, 191, 36, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 85% 50%, rgba(56, 189, 248, 0.15) 0%, transparent 45%),
            linear-gradient(135deg, #090d18 0%, #111827 50%, #060911 100%);
        border: 1.5px solid rgba(251, 191, 36, 0.55);
        border-radius: 16px;
        padding: 14px 22px;
        margin-top: 6px;
        margin-bottom: 14px;
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.75), 0 0 24px rgba(251, 191, 36, 0.14);
        position: relative;
        overflow: hidden;
    }
    .boutique-cart-bar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #fbbf24, #38bdf8, #10b981, transparent);
        background-size: 200% 100%;
        animation: goldShimmer 6s linear infinite;
    }

    .jewel-showcase-card {
        position: relative;
        background: linear-gradient(155deg, rgba(15, 23, 42, 0.94) 0%, rgba(7, 11, 20, 0.99) 100%);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-top: 3px solid #38bdf8;
        border-radius: 16px;
        padding: 16px 16px 14px 16px;
        margin-bottom: 6px;
        min-height: 215px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
        overflow: hidden;
        word-break: keep-all;
    }
    .jewel-showcase-card:hover {
        transform: translateY(-5px) scale(1.012);
        border-color: rgba(251, 191, 36, 0.75);
        border-top-color: #fbbf24;
        box-shadow: 0 18px 38px rgba(0, 0, 0, 0.8), 0 0 26px rgba(251, 191, 36, 0.22);
    }
    .jewel-showcase-card.active-vault {
        background:
            radial-gradient(circle at 50% 0%, rgba(251, 191, 36, 0.22) 0%, transparent 65%),
            linear-gradient(155deg, #131c31 0%, #090d18 100%);
        border: 2px solid #fbbf24;
        box-shadow: 0 0 32px rgba(251, 191, 36, 0.38), inset 0 0 18px rgba(251, 191, 36, 0.12);
    }
    </style>
    """
    return "\n".join(line.lstrip() for line in css.splitlines())


def build_boutique_cart_bar_html(
    total_notices: int,
    cart_items: List[Dict[str, Any]],
    active_prof: Dict[str, Any],
    view_mode: str,
) -> str:
    cart_cnt = len(cart_items)
    total_est_profit = sum(int(c.get("base_amount", 0)) * 54 // 1000 for c in cart_items)
    profit_eok = round(total_est_profit / 100_000_000.0, 2)
    cart_names = " · ".join([str(c.get("title", ""))[:10] + ".." for c in cart_items[:3]])
    if not cart_names:
        cart_names = "마음에 드는 공고의 [💖 찜]을 눌러 나만의 입찰 포트폴리오를 구성하세요"

    raw = f"""
<div class="boutique-cart-bar">
<div style="display:flex;align-items:center;gap:14px;">
<div style="width:48px;height:48px;border-radius:13px;background:linear-gradient(135deg,#f59e0b,#fbbf24);display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 0 18px rgba(245,158,11,0.5);">
💎
</div>
<div>
<div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;flex-wrap:wrap;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;letter-spacing:0.4px;">TREASURE BOUTIQUE v3.0</span>
<span style="color:#7dd3fc;font-size:11px;font-weight:800;">● {view_mode}</span>
<span style="color:#94a3b8;font-size:11px;">|</span>
<span style="color:#fde68a;font-size:11px;font-weight:800;">열린 캐비닛: [{active_prof['nid']}] {active_prof['title'][:18]}</span>
</div>
<div style="font-size:16px;font-weight:900;color:#f8fafc;letter-spacing:-0.3px;">
🛍️ 나의 보물 공고 컬렉션 <span style="color:#fbbf24;">({cart_cnt}건 담김 / 전체 {total_notices}건)</span>
</div>
<div style="font-size:11.5px;color:#cbd5e1;font-weight:600;margin-top:2px;">
📌 <b>포트폴리오:</b> {cart_names}
</div>
</div>
</div>

<div style="background:rgba(15,23,42,0.92);border:1px solid rgba(16,185,129,0.45);border-radius:11px;padding:8px 14px;text-align:right;">
<div style="font-size:10px;color:#94a3b8;font-weight:800;">카트 합산 기대수익 (마진율 5.4% 기준)</div>
<div style="font-size:16px;color:#34d399;font-weight:900;">+ 약 {profit_eok:,.2f}억 원 <span style="font-size:11px;color:#6ee7b7;">({total_est_profit:,}원)</span></div>
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def build_jewel_showcase_tile_html(
    prof: Dict[str, Any],
    idx: int,
    is_active: bool,
    in_cart: bool,
) -> str:
    base_eok = round(prof["base_amt"] / 100_000_000.0, 1)
    est_margin_man = int(round((prof["bid_m5"] - prof["est_net_cost"]) / 10_000.0))

    if is_active:
        cls_name = "jewel-showcase-card active-vault"
        status_pill = '<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 8px;border-radius:999px;">🗝️ CABINET OPENED</span>'
        top_border = "#fbbf24"
    else:
        cls_name = "jewel-showcase-card"
        status_pill = f'<span style="background:rgba(56,189,248,0.14);border:1px solid rgba(56,189,248,0.4);color:#7dd3fc;font-size:10px;font-weight:800;padding:2px 8px;border-radius:999px;">VAULT #{idx+1:02d}</span>'
        top_border = "#38bdf8" if prof["base_amt"] >= 5_000_000_000 else "#10b981"

    cart_badge = (
        '<span style="background:rgba(244,63,94,0.2);border:1px solid #f43f5e;color:#fda4af;font-size:10px;font-weight:900;padding:2px 7px;border-radius:999px;">💖 찜완료</span>'
        if in_cart
        else '<span style="background:rgba(15,23,42,0.8);border:1px solid #334155;color:#94a3b8;font-size:10px;font-weight:700;padding:2px 7px;border-radius:999px;">⏱ ' + prof["deadline"].split(" ")[0] + '</span>'
    )

    raw = f"""
<div class="{cls_name}" style="border-top-color:{top_border};">
<div>
<div style="display:flex;justify-content:space-between;align-items:center;gap:4px;margin-bottom:8px;">
{status_pill}
{cart_badge}
</div>
<div style="font-size:14.5px;font-weight:900;color:#f8fafc;line-height:1.35;margin-bottom:6px;min-height:38px;">
{prof['title']}
</div>
<div style="font-size:11px;color:#94a3b8;font-weight:700;margin-bottom:10px;">
🏛 {prof['agency']} &nbsp;|&nbsp; <span style="color:#cbd5e1;">{prof['nid']}</span>
</div>
</div>

<div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;background:rgba(2,6,23,0.75);border:1px solid rgba(51,65,85,0.75);border-radius:10px;padding:8px 10px;margin-bottom:8px;">
<div>
<div style="font-size:9.5px;color:#94a3b8;font-weight:800;">💎 기초금액 스케일</div>
<div style="font-size:14px;color:#38bdf8;font-weight:900;">{base_eok}억 원</div>
</div>
<div style="border-left:1px solid rgba(51,65,85,0.7);padding-left:8px;">
<div style="font-size:9.5px;color:#94a3b8;font-weight:800;">👑 M5 기대순익</div>
<div style="font-size:13px;color:#34d399;font-weight:900;">+{est_margin_man:,}만</div>
</div>
</div>

<div style="display:flex;justify-content:space-between;align-items:center;font-size:10.5px;font-weight:800;color:#fde68a;">
<span>{prof['risk_badge']}</span>
<span style="color:#c084fc;">하한 {prof['low_rate']:.3f}%</span>
</div>
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def build_private_cabinet_header_html(prof: Dict[str, Any], idx: int) -> str:
    raw = f"""
<div style="background:linear-gradient(90deg,rgba(251,191,36,0.18) 0%,rgba(16,185,129,0.14) 50%,rgba(15,23,42,0.95) 100%);border:1.5px solid #fbbf24;border-left:6px solid #f59e0b;border-radius:14px;padding:14px 20px;margin-top:10px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;box-shadow:0 12px 30px rgba(0,0,0,0.65);">
<div>
<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:2px 9px;border-radius:999px;letter-spacing:0.5px;">PRIVATE VAULT CABINET #{idx+1:02d} UNLOCKED</span>
<span style="color:#6ee7b7;font-size:11px;font-weight:800;">● 집중 분석 모드 (나머지 캐비닛 자동 닫힘)</span>
</div>
<div style="font-size:18px;font-weight:900;color:#f8fafc;letter-spacing:-0.3px;">
🗝️ [{prof['nid']}] {prof['title']} — 프라이빗 전술 금고
</div>
</div>
<div style="text-align:right;">
<div style="font-size:10.5px;color:#fde68a;font-weight:800;">👑 M5 양자코어 추천 투찰가</div>
<div style="font-size:18px;color:#38bdf8;font-weight:900;">{prof['bid_m5']:,}원</div>
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())
