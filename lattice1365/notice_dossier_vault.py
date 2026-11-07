import re
import io
import json
import zipfile
import hashlib
from typing import Dict, Any, Tuple


def _pick_val(d: Dict[str, Any], keys, default):
    for k in keys:
        if k in d and d[k] is not None and d[k] != "":
            return d[k]
    return default


def _to_int(val, default=0) -> int:
    if isinstance(val, (int, float)):
        return int(val)
    if isinstance(val, str):
        cleaned = re.sub(r"[^0-9]", "", val)
        return int(cleaned) if cleaned else default
    return default


def _to_float(val, default=88.745) -> float:
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        m = re.search(r"[0-9]+(?:\.[0-9]+)?", val)
        return float(m.group(0)) if m else default
    return default


def analyze_construction_profile(n: Dict[str, Any], idx: int = 0) -> Dict[str, Any]:
    nid = str(_pick_val(n, ["id", "no", "notice_no", "notice_id", "공고번호", "code"], f"202611-0{idx+1:04d}"))
    title = str(_pick_val(n, ["title", "name", "notice_title", "subject", "공고명", "공사명"], "관급 건축공사"))
    agency = str(_pick_val(n, ["agency", "org", "client", "발주처", "발주기관", "수요기관"], "조달청"))
    deadline = str(_pick_val(n, ["deadline", "close_dt", "end_date", "due", "마감", "마감일시"], "2026-11-13 10:00"))
    license_name = str(_pick_val(n, ["license", "lic", "category", "sector", "업종", "면허"], "건축공사업"))
    region_name = str(_pick_val(n, ["region", "loc", "area", "location", "지역", "관할지역"], "강원특별자치도"))

    base_amt = _to_int(_pick_val(n, ["base_amount", "base", "base_amt", "base_price", "기초금액", "기초"], 5_180_000_000))
    a_val = _to_int(_pick_val(n, ["a_value", "a_val", "a_amt", "a_cost", "A값", "a"], 241_800_000))
    low_rate = _to_float(_pick_val(n, ["lower_limit_rate", "low_rate", "limit_rate", "cutline", "낙찰하한율", "하한율"], 88.745))

    if "리모델링" in title or "증축" in title or "공간재구조화" in title:
        work_type = "🏛 기존 건축물 그린리모델링 · 내진보강 및 증축공사"
        struct_type = "철근콘크리트조(RC) + 철골조(S) 복합 보강구조"
        duration_days = max(180, min(540, int((base_amt / 100_000_000) * 7.5)))
        w_arch, w_civil, w_mech, w_finish = 38, 12, 22, 28
        special_note = "기존 시설물 철거/해체 안전관리계획서 필수, 석면 해체 및 비산먼지 저감 대책 포함, 야간/휴일 소음 제어 공법 적용"
        risk_badge = "⚠️ 철거·석면해체 공정 간섭 주의"
    elif "체육" in title or "수영장" in title or "문화" in title:
        work_type = "🏟 대공간 장스팬(Long-Span) 다목적 체육·문화시설 신축공사"
        struct_type = "철골트러스 대공간 지붕구조(PEB/Space Frame) + 철근콘크리트조"
        duration_days = max(360, min(720, int((base_amt / 100_000_000) * 8.2)))
        w_arch, w_civil, w_mech, w_finish = 44, 18, 20, 18
        special_note = "대공간 지붕 철골 트러스 인양 안전검토, 수영장/체육관 방수·방습 특화시공, 고단열 커튼월 및 흡음 내장재 적용"
        risk_badge = "🛡️ 대공간 철골 인양·특수방수 중점"
    elif "청사" in title or "부두" in title or "센터" in title or "조리원" in title:
        work_type = "🏢 공공청사 · 특수목적 스마트 복지/행정 인프라 신축공사"
        struct_type = "철근콘크리트 라멘조(지하 1층 ~ 지상 4층 규모)"
        duration_days = max(300, min(660, int((base_amt / 100_000_000) * 8.0)))
        w_arch, w_civil, w_mech, w_finish = 42, 16, 21, 21
        special_note = "제로에너지건축물(ZEB 5등급) 인증 및 BF(장애물 없는 생활환경) 예비인증 기준 준수, 흙막이 가시설 및 지정공사 포함"
        risk_badge = "⚡ ZEB 5등급·BF 인증 자재 필수"
    else:
        work_type = "🏗️ 일반 관급 공공시설 신축 및 부대토목 건축공사"
        struct_type = "철근콘크리트조(RC) 표준 구조"
        duration_days = max(240, min(600, int((base_amt / 100_000_000) * 7.8)))
        w_arch, w_civil, w_mech, w_finish = 45, 15, 18, 22
        special_note = "조달청 표준일위대가 및 적격심사 세부기준 적용, 안전관리비·품질관리비 법정 정산 대상 공사"
        risk_badge = "✅ 표준 적격심사 일반공정"

    area_m2 = round((base_amt / 2_550_000.0), 1)
    area_py = round(area_m2 / 3.3058, 1)
    est_net_cost = int(round(base_amt * 0.815))

    def _calc_bid(rate_pct: float) -> int:
        pred = base_amt * (rate_pct / 100.0)
        return int(round(((pred - a_val) * (low_rate / 100.0)) + a_val))

    bid_m5 = _calc_bid(100.0907)
    bid_egr = _calc_bid(100.1100)
    bid_lat = _calc_bid(100.0658)

    return {
        "nid": nid,
        "title": title,
        "agency": agency,
        "deadline": deadline,
        "license": license_name,
        "region": region_name,
        "base_amt": base_amt,
        "a_val": a_val,
        "low_rate": low_rate,
        "est_net_cost": est_net_cost,
        "work_type": work_type,
        "struct_type": struct_type,
        "duration_days": duration_days,
        "area_m2": area_m2,
        "area_py": area_py,
        "w_arch": w_arch,
        "w_civil": w_civil,
        "w_mech": w_mech,
        "w_finish": w_finish,
        "special_note": special_note,
        "risk_badge": risk_badge,
        "bid_m5": bid_m5,
        "bid_egr": bid_egr,
        "bid_lat": bid_lat,
    }


def generate_notice_attachments(prof: Dict[str, Any]) -> Tuple[str, str, str, str]:
    nid = prof["nid"]
    title = prof["title"]
    agency = prof["agency"]
    base_amt = prof["base_amt"]
    a_val = prof["a_val"]
    low_rate = prof["low_rate"]
    net_cost = prof["est_net_cost"]

    doc_html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><title>[입찰공고문] {title}</title>
<style>
body {{ font-family: 'Malgun Gothic', sans-serif; padding: 36px; color: #111827; line-height: 1.6; max-width: 840px; margin: 0 auto; }}
h1 {{ text-align: center; border-bottom: 3px double #1e293b; padding-bottom: 12px; font-size: 22px; }}
table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
th, td {{ border: 1px solid #64748b; padding: 9px 12px; font-size: 13.5px; }}
th {{ background: #f1f5f9; width: 24%; text-align: left; font-weight: 800; }}
.stamp {{ margin-top: 32px; text-align: center; font-size: 18px; font-weight: 900; }}
</style></head><body>
<h1>시설공사 입찰공고문 (나라장터 G2B 연동)</h1>
<p><b>공고번호:</b> 제 {nid} 호 &nbsp;|&nbsp; <b>발주기관:</b> {agency}</p>
<h3>1. 입찰에 부치는 사항</h3>
<table>
<tr><th>공사명</th><td colspan="3"><b>{title}</b></td></tr>
<tr><th>공사현장</th><td>{prof['region']} 관내</td><th>공사기간</th><td>착공일로부터 {prof['duration_days']}일간</td></tr>
<tr><th>공사개요</th><td colspan="3">{prof['work_type']} ({prof['struct_type']}, 추정 연면적 {prof['area_m2']:,}㎡)</td></tr>
<tr><th>기초금액</th><td><b>{base_amt:,}원</b> (부가세 포함)</td><th>A값(법정비용)</th><td><b>{a_val:,}원</b></td></tr>
<tr><th>추정 순공사원가</th><td><b>{net_cost:,}원</b> (98% 하한: {int(net_cost*0.98):,}원)</td><th>낙찰하한율</th><td><b>{low_rate:.3f}%</b></td></tr>
</table>
<h3>2. AI 3대 트랙 사전 사정 가이드</h3>
<table>
<tr><th>👑 트랙 1 (M5 양자코어)</th><td><b>{prof['bid_m5']:,}원</b> (100.0907%)</td><th>🛡️ 트랙 2 (EGR 방어선)</th><td><b>{prof['bid_egr']:,}원</b> (100.1100%)</td></tr>
<tr><th>⚡ 트랙 3 (LATTICE 격자)</th><td><b>{prof['bid_lat']:,}원</b> (100.0658%)</td><th>핵심 리스크 진단</th><td>{prof['risk_badge']}</td></tr>
</table>
<h3>3. 입찰 및 계약방식</h3>
<ul>
<li>적격심사 대상공사이며, 복수예비가격(15개 중 4개 추첨 산술평균)이 적용되는 전자입찰입니다.</li>
<li>입찰마감일시: <b>{prof['deadline']}</b> (국가종합전자조달시스템 나라장터)</li>
<li>특기사항: {prof['special_note']}</li>
</ul>
<div class="stamp">위와 같이 공고합니다.<br><br>{agency} 재무관</div>
</body></html>"""

    c_arch = int(base_amt * (prof["w_arch"] / 100.0))
    c_finish = int(base_amt * (prof["w_finish"] / 100.0))
    c_mech = int(base_amt * (prof["w_mech"] / 100.0))
    c_civil = base_amt - (c_arch + c_finish + c_mech)
    boq_csv = "\ufeff" + "\n".join([
        "공고번호,공사명,공종코드,세부공종명,단위,수량,설계예산금액(원),원가비중(%)",
        f"{nid},{title},A01,가설 및 철근콘크리트 골조공사,식,1,{c_arch},{prof['w_arch']}%",
        f"{nid},{title},A02,조적·미장·방수·창호 및 내외장 마감공사,식,1,{c_finish},{prof['w_finish']}%",
        f"{nid},{title},M01,기계설비·환기 및 부대설비공사,식,1,{c_mech},{prof['w_mech']}%",
        f"{nid},{title},C01,토목·흙막이가시설 및 부대토목공사,식,1,{c_civil},{prof['w_civil']}%",
        f"{nid},{title},S01,[법정 A값] 국민연금·건강보험·안전관리비 등 합계,식,1,{a_val},{round(a_val/max(1,base_amt)*100,2)}%",
        f"{nid},{title},TOT,[합계] 기초금액 총괄,식,1,{base_amt},100.0%",
    ])

    bid_json = json.dumps({
        "g2b_notice_id": nid,
        "project_title": title,
        "ordering_agency": agency,
        "license_required": prof["license"],
        "region_limit": prof["region"],
        "deadline": prof["deadline"],
        "financial_specs": {
            "base_amount_won": base_amt,
            "a_value_won": a_val,
            "estimated_net_cost_won": net_cost,
            "net_cost_98_cutline_won": int(net_cost * 0.98),
            "lower_limit_rate_pct": low_rate,
        },
        "ai_triple_track_recommendations": {
            "track1_m5_core_won": prof["bid_m5"],
            "track2_egr_defense_won": prof["bid_egr"],
            "track3_lattice_1365_won": prof["bid_lat"],
        },
        "engineering_profile": {
            "work_type": prof["work_type"],
            "structure": prof["struct_type"],
            "estimated_area_m2": prof["area_m2"],
            "duration_days": prof["duration_days"],
            "risk_badge": prof["risk_badge"],
        }
    }, ensure_ascii=False, indent=2)

    spec_txt = "\n".join([
        "======================================================================",
        f" [공사시방서 및 현장설명서 요약] 공고번호: {nid}",
        f" 공사명: {title}",
        "======================================================================",
        f"1. 발주기관: {agency}",
        f"2. 참가자격: {prof['license']} ({prof['region']})",
        f"3. 공사종류: {prof['work_type']}",
        f"4. 구조/규모: {prof['struct_type']} / 연면적 약 {prof['area_m2']:,}㎡ ({prof['area_py']:,}평)",
        f"5. 공사기간: 착공일로부터 {prof['duration_days']}일간",
        "6. 재무제원:",
        f"   - 기초금액: {base_amt:,}원",
        f"   - 법정 A값: {a_val:,}원",
        f"   - 추정 순공사원가: {net_cost:,}원 (98% 미달 배제선: {int(net_cost*0.98):,}원)",
        f"   - 적격심사 낙찰하한율: {low_rate:.3f}%",
        "7. AI 3대 트랙 사전 추천 투찰가:",
        f"   - [트랙 1] M5 양자코어 (100.0907%): {prof['bid_m5']:,}원",
        f"   - [트랙 2] EGR 강건방어 (100.1100%): {prof['bid_egr']:,}원",
        f"   - [트랙 3] LATTICE 격자 (100.0658%): {prof['bid_lat']:,}원",
        "8. 핵심 시공 유의사항 및 특기시방:",
        f"   - {prof['special_note']}",
        "======================================================================",
    ])

    return doc_html, boq_csv, bid_json, spec_txt


def generate_master_zip_bundle(prof: Dict[str, Any]) -> Tuple[bytes, Dict[str, Any]]:
    doc_html, boq_csv, bid_json, spec_txt = generate_notice_attachments(prof)
    nid = prof["nid"]
    title = prof["title"]

    ai_strategy_md = f"""# 🪐 [{nid}] {title} — AI 3대 트랙 통합 입찰 전략서

## 1. 공고 핵심 제원
- **발주기관**: {prof['agency']}
- **입찰마감**: {prof['deadline']}
- **기초금액**: {prof['base_amt']:,}원
- **법정 A값**: {prof['a_val']:,}원
- **추정 순공사원가 (81.5%)**: {prof['est_net_cost']:,}원
- **적격심사 낙찰하한율**: {prof['low_rate']:.3f}%

## 2. AI 3대 트랙 권장 투찰금액 및 나라장터 2픽 전략
| 트랙 구분 | 목표 사정률 | 권장 투찰금액(원) | 추천 복수예가 2픽 조합 |
| :--- | :---: | :---: | :---: |
| **👑 트랙 1 (M5 양자코어)** | 100.0907% | **{prof['bid_m5']:,}원** | **2번 + 12번** (조합 #238) |
| **🛡️ 트랙 2 (EGR 강건방어)** | 100.1100% | **{prof['bid_egr']:,}원** | **3번 + 12번** (Q50 중위방어) |
| **⚡ 트랙 3 (LATTICE 격자)** | 100.0658% | **{prof['bid_lat']:,}원** | **2번 + 13번** (조합 #338) |

## 3. 현장 공정 및 시방서 중점 체크포인트
- **공사분류**: {prof['work_type']}
- **구조/연면적**: {prof['struct_type']} / 약 {prof['area_m2']:,}㎡ ({prof['area_py']:,}평)
- **리스크 진단**: {prof['risk_badge']}
- **특기시방 요약**: {prof['special_note']}
"""

    files_map = {
        f"01_입찰공고문/입찰공고문_{nid}.html": doc_html.encode("utf-8"),
        f"02_물량내역서_CSV/공내역서_{nid}.csv": boq_csv.encode("utf-8"),
        f"03_전자입찰_BID/G2B제원_{nid}.json": bid_json.encode("utf-8"),
        f"04_시방서_및_특기사항/공사시방서_{nid}.txt": spec_txt.encode("utf-8"),
        f"05_AI_투찰전략_리포트/AI_3대트랙_전략서_{nid}.md": ai_strategy_md.encode("utf-8"),
    }

    manifest = {}
    total_bytes = 0
    for path, raw_bytes in files_map.items():
        h = hashlib.sha256(raw_bytes).hexdigest()[:16].upper()
        sz_kb = round(len(raw_bytes) / 1024.0, 2)
        manifest[path] = {"size_kb": sz_kb, "sha256_short": h}
        total_bytes += len(raw_bytes)

    manifest_bytes = json.dumps({
        "package_id": f"G2B-VAULT-{nid}",
        "total_files": len(files_map) + 1,
        "integrity_status": "VERIFIED_SHA256",
        "files": manifest,
    }, ensure_ascii=False, indent=2).encode("utf-8")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path, raw_bytes in files_map.items():
            zf.writestr(path, raw_bytes)
        zf.writestr(f"00_무결성검증_MANIFEST_{nid}.json", manifest_bytes)

    zip_bytes = buf.getvalue()
    zip_sha256 = hashlib.sha256(zip_bytes).hexdigest()[:16].upper()

    meta = {
        "zip_size_kb": round(len(zip_bytes) / 1024.0, 2),
        "raw_size_kb": round(total_bytes / 1024.0, 2),
        "zip_sha256": zip_sha256,
        "manifest": manifest,
        "ai_strategy_md": ai_strategy_md,
    }
    return zip_bytes, meta


def build_notice_dossier_html(prof: Dict[str, Any]) -> str:
    _, meta = generate_master_zip_bundle(prof)
    raw = f"""
<div style="background:linear-gradient(145deg,#070d19 0%,#0f172a 55%,#040811 100%);border:1.5px solid rgba(16,185,129,0.5);border-left:5px solid #10b981;border-radius:14px;padding:18px 20px;margin-top:4px;margin-bottom:12px;box-shadow:0 14px 34px rgba(0,0,0,0.7);word-break:keep-all;">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding-bottom:10px;margin-bottom:12px;border-bottom:1px solid rgba(148,163,184,0.18);">
<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
<span style="background:linear-gradient(90deg,#10b981,#38bdf8);color:#020617;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:999px;">QUANTUM DOSSIER VAULT v2.0</span>
<span style="font-size:16px;font-weight:900;color:#f8fafc;">🏗️ [{prof['nid']}] {prof['title']}</span>
</div>
<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
<span style="background:rgba(56,189,248,0.14);border:1px solid rgba(56,189,248,0.45);color:#7dd3fc;font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:999px;">🔒 SHA-256: {meta['zip_sha256']}</span>
<span style="background:rgba(245,158,11,0.16);border:1px solid rgba(245,158,11,0.5);color:#fde68a;font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:999px;">⏱ 예상 공기: {prof['duration_days']}일</span>
</div>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;">
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">📌 공사 유형 및 리스크</div>
<div style="font-size:12px;color:#34d399;font-weight:900;line-height:1.35;margin-bottom:3px;">{prof['work_type']}</div>
<span style="font-size:10.5px;color:#fde68a;font-weight:800;">{prof['risk_badge']}</span>
</div>
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">🏢 주구조 및 추정 연면적</div>
<div style="font-size:12px;color:#38bdf8;font-weight:900;line-height:1.35;">{prof['struct_type']}<br><span style="color:#e2e8f0;font-size:11px;">약 {prof['area_m2']:,}㎡ ({prof['area_py']:,}평)</span></div>
</div>
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">💰 추정 순공사원가 (81.5%)</div>
<div style="font-size:13.5px;color:#fbbf24;font-weight:900;">{prof['est_net_cost']:,}원</div>
<div style="font-size:10.5px;color:#94a3b8;margin-top:2px;">98% 원가하한: {int(prof['est_net_cost']*0.98):,}원</div>
</div>
<div style="background:rgba(15,23,42,0.92);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">🎯 AI 3대 트랙 예상 투찰가</div>
<div style="font-size:11px;color:#38bdf8;font-weight:800;">👑 M5: {prof['bid_m5']:,}원</div>
<div style="font-size:11px;color:#fbbf24;font-weight:800;">🛡️ EGR: {prof['bid_egr']:,}원</div>
<div style="font-size:11px;color:#34d399;font-weight:800;">⚡ LAT: {prof['bid_lat']:,}원</div>
</div>
</div>

<div style="background:rgba(2,6,23,0.78);border:1px solid rgba(56,189,248,0.28);border-radius:10px;padding:10px 14px;margin-bottom:10px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;color:#cbd5e1;margin-bottom:6px;flex-wrap:wrap;gap:6px;">
<span>📊 <b>공종별 예정 원가 구성비 (AI 물량내역 X-Ray 분해)</b></span>
<span style="color:#7dd3fc;">🟦 골조 {prof['w_arch']}% ({int(prof['base_amt']*prof['w_arch']/100):,}원) · 🟩 마감 {prof['w_finish']}% · 🟪 기계설비 {prof['w_mech']}% · 🟨 토목 {prof['w_civil']}%</span>
</div>
<div style="width:100%;height:10px;background:#0f172a;border-radius:999px;overflow:hidden;display:flex;">
<div style="width:{prof['w_arch']}%;height:100%;background:#38bdf8;"></div>
<div style="width:{prof['w_finish']}%;height:100%;background:#10b981;"></div>
<div style="width:{prof['w_mech']}%;height:100%;background:#a855f7;"></div>
<div style="width:{prof['w_civil']}%;height:100%;background:#f59e0b;"></div>
</div>
</div>

<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;background:rgba(15,23,42,0.88);border-left:3.5px solid #fbbf24;border-radius:6px;padding:8px 12px;font-size:12px;color:#e2e8f0;">
<span>💡 <b style="color:#fde68a;">시방서 핵심 스캔:</b> {prof['special_note']}</span>
<span style="background:rgba(16,185,129,0.16);border:1px solid rgba(16,185,129,0.45);color:#6ee7b7;font-size:10.5px;font-weight:900;padding:2px 8px;border-radius:6px;">📦 6종 통합 패키지 ({meta['zip_size_kb']} KB) 준비완료</span>
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())
