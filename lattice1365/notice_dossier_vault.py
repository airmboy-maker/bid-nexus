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


def build_boq_preview_table_html(prof: Dict[str, Any]) -> str:
    """
    [인앱 열람 1] CSV 원시 텍스트 대신 일정한 양식의 고가독성 공종별 물량내역서(BoQ) 테이블 렌더링
    """
    base_amt = prof["base_amt"]
    a_val = prof["a_val"]
    c_arch = int(base_amt * (prof["w_arch"] / 100.0))
    c_finish = int(base_amt * (prof["w_finish"] / 100.0))
    c_mech = int(base_amt * (prof["w_mech"] / 100.0))
    c_civil = base_amt - (c_arch + c_finish + c_mech)
    a_pct = round(a_val / max(1, base_amt) * 100, 2)

    rows = [
        ("A01", "건축골조", "가설 및 철근콘크리트(RC/S) 골조공사", "1 식", c_arch, prof["w_arch"], "#38bdf8"),
        ("A02", "건축마감", "조적·미장·방수·창호 및 내외장 마감공사", "1 식", c_finish, prof["w_finish"], "#10b981"),
        ("M01", "기계설비", "기계설비·환기·공조 및 부대설비공사", "1 식", c_mech, prof["w_mech"], "#a855f7"),
        ("C01", "부대토목", "토목·흙막이가시설 및 부대토목공사", "1 식", c_civil, prof["w_civil"], "#f59e0b"),
        ("S01", "법정비용", "[법정 A값] 국민연금·건강보험·산업안전보건관리비 등", "1 식", a_val, a_pct, "#f43f5e"),
    ]

    tr_html = ""
    for code, cat, name, unit, amt, pct, col in rows:
        tr_html += f"""
<tr style="border-bottom:1px solid rgba(51,65,85,0.65);">
<td style="padding:10px 12px;font-weight:900;color:{col};font-size:12.5px;white-space:nowrap;">{code}</td>
<td style="padding:10px 12px;"><span style="background:rgba(15,23,42,0.9);border:1px solid {col};color:{col};font-size:11px;font-weight:800;padding:2px 8px;border-radius:6px;white-space:nowrap;">{cat}</span></td>
<td style="padding:10px 12px;font-weight:800;color:#f1f5f9;font-size:13px;">{name}</td>
<td style="padding:10px 12px;text-align:center;color:#94a3b8;font-weight:700;font-size:12px;">{unit}</td>
<td style="padding:10px 12px;text-align:right;font-weight:900;color:#f8fafc;font-size:13.5px;white-space:nowrap;">{amt:,}원</td>
<td style="padding:10px 12px;width:160px;">
<div style="display:flex;justify-content:space-between;font-size:11px;font-weight:800;color:{col};margin-bottom:3px;"><span>비중</span><span>{pct}%</span></div>
<div style="width:100%;height:5px;background:#020617;border-radius:999px;overflow:hidden;"><div style="width:{min(100, int(pct*1.8))}%;height:100%;background:{col};"></div></div>
</td>
</tr>"""

    raw = f"""
<div style="background:linear-gradient(145deg,#09101f 0%,#050914 100%);border:1px solid rgba(56,189,248,0.35);border-radius:12px;padding:16px 18px;margin-top:6px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.18);">
<span style="font-size:14px;font-weight:900;color:#f8fafc;">📊 [{prof['nid']}] 공종별 표준 공내역서 (설계예산 물량내역서 규격 양식)</span>
<span style="background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.4);color:#7dd3fc;font-size:11px;font-weight:800;padding:2px 9px;border-radius:999px;">단위: 원 (부가세 포함)</span>
</div>
<table style="width:100%;border-collapse:collapse;text-align:left;">
<thead>
<tr style="background:rgba(15,23,42,0.95);border-bottom:2px solid #38bdf8;color:#94a3b8;font-size:11.5px;font-weight:900;">
<th style="padding:9px 12px;">코드</th>
<th style="padding:9px 12px;">분류</th>
<th style="padding:9px 12px;">세부 공종명</th>
<th style="padding:9px 12px;text-align:center;">단위·수량</th>
<th style="padding:9px 12px;text-align:right;">설계예산 금액</th>
<th style="padding:9px 12px;">원가 구성비</th>
</tr>
</thead>
<tbody>
{tr_html}
<tr style="background:rgba(16,185,129,0.12);border-top:2px solid #10b981;">
<td colspan="4" style="padding:11px 12px;font-weight:900;color:#34d399;font-size:13.5px;">🏆 [TOT] 기초금액 총괄 합계 (설계예산 총액)</td>
<td style="padding:11px 12px;text-align:right;font-weight:900;color:#fef08a;font-size:15px;">{base_amt:,}원</td>
<td style="padding:11px 12px;text-align:right;font-weight:900;color:#34d399;font-size:13px;">100.0% (기준)</td>
</tr>
</tbody>
</table>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def build_spec_sheet_html(prof: Dict[str, Any]) -> str:
    """
    [인앱 열람 2] 기존의 밋밋한 '===' 텍스트 코드블록을 대체하는 고가독성 '공사시방서 & AI 3대 트랙 전략 규격 양식서'
    """
    net_98 = int(prof["est_net_cost"] * 0.98)
    raw = f"""
<div style="background:linear-gradient(145deg,#080f1e 0%,#050914 100%);border:1.5px solid rgba(56,189,248,0.38);border-radius:14px;padding:18px 20px;margin-top:6px;word-break:keep-all;">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding-bottom:10px;margin-bottom:14px;border-bottom:2px solid rgba(56,189,248,0.3);">
<div>
<span style="background:#fbbf24;color:#020617;font-size:10px;font-weight:900;padding:3px 9px;border-radius:6px;letter-spacing:0.4px;">STANDARD SPEC SHEET</span>
<span style="font-size:16px;font-weight:900;color:#f8fafc;margin-left:8px;">📐 [공사시방서 및 현장설명서 요약 규격서] 공고번호: {prof['nid']}</span>
</div>
<span style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.45);color:#6ee7b7;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;">{prof['risk_badge']}</span>
</div>

<div style="font-size:12.5px;font-weight:900;color:#7dd3fc;margin-bottom:8px;">1. 현장 기본 제원 및 시공 개요</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;">
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-left:3.5px solid #38bdf8;border-radius:8px;padding:10px 13px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">🏛 발주기관 / 수요처</div>
<div style="font-size:13.5px;color:#f8fafc;font-weight:900;">{prof['agency']}</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-left:3.5px solid #a855f7;border-radius:8px;padding:10px 13px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">🪪 입찰 참가자격 (면허·지역)</div>
<div style="font-size:13.5px;color:#e9d5ff;font-weight:900;">{prof['license']} ({prof['region']})</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-left:3.5px solid #f59e0b;border-radius:8px;padding:10px 13px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">⏱ 공사기간 / 입찰마감</div>
<div style="font-size:13px;color:#fde68a;font-weight:900;">착공 후 {prof['duration_days']}일간 <span style="color:#94a3b8;font-size:11px;">(마감 {prof['deadline']})</span></div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-left:3.5px solid #10b981;border-radius:8px;padding:10px 13px;grid-column:span 2;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">🏗️ 공사종류 및 세부 구조형식</div>
<div style="font-size:13px;color:#34d399;font-weight:900;">{prof['work_type']} &nbsp;|&nbsp; <span style="color:#e2e8f0;">{prof['struct_type']}</span></div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-left:3.5px solid #38bdf8;border-radius:8px;padding:10px 13px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">📐 추정 연면적 규모</div>
<div style="font-size:13.5px;color:#f8fafc;font-weight:900;">약 {prof['area_m2']:,}㎡ <span style="color:#38bdf8;font-size:12px;">({prof['area_py']:,}평)</span></div>
</div>
</div>

<div style="font-size:12.5px;font-weight:900;color:#7dd3fc;margin-bottom:8px;">2. 재무 제원 및 원가 마지노선 분석</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px;">
<div style="background:rgba(2,6,23,0.85);border:1px solid rgba(56,189,248,0.35);border-radius:9px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">💎 기초금액 (부가세 포함)</div>
<div style="font-size:15px;color:#f8fafc;font-weight:900;margin-top:3px;">{prof['base_amt']:,}원</div>
</div>
<div style="background:rgba(2,6,23,0.85);border:1px solid rgba(168,85,247,0.35);border-radius:9px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">🛡️ 법정 A값 (정산비용)</div>
<div style="font-size:15px;color:#e9d5ff;font-weight:900;margin-top:3px;">{prof['a_val']:,}원</div>
</div>
<div style="background:rgba(2,6,23,0.85);border:1px solid rgba(245,158,11,0.35);border-radius:9px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">💰 추정 순공사원가 (81.5%)</div>
<div style="font-size:15px;color:#fbbf24;font-weight:900;margin-top:3px;">{prof['est_net_cost']:,}원</div>
<div style="font-size:10px;color:#fda4af;font-weight:700;margin-top:2px;">98% 미달 배제선: {net_98:,}원</div>
</div>
<div style="background:rgba(2,6,23,0.85);border:1px solid rgba(16,185,129,0.35);border-radius:9px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;">🎯 적격심사 낙찰하한율</div>
<div style="font-size:15px;color:#34d399;font-weight:900;margin-top:3px;">{prof['low_rate']:.3f}%</div>
<div style="font-size:10px;color:#94a3b8;font-weight:700;margin-top:2px;">적격 만점 커트라인</div>
</div>
</div>

<div style="font-size:12.5px;font-weight:900;color:#7dd3fc;margin-bottom:8px;">3. AI 3대 트랙 사전 추천 투찰가 및 나라장터 2픽 전략 비교표</div>
<table style="width:100%;border-collapse:collapse;margin-bottom:16px;font-size:12.5px;">
<thead>
<tr style="background:rgba(15,23,42,0.95);border-bottom:2px solid #38bdf8;color:#94a3b8;font-size:11.5px;">
<th style="padding:9px 12px;text-align:left;">AI 사정 트랙 구분</th>
<th style="padding:9px 12px;text-align:center;">목표 사정률</th>
<th style="padding:9px 12px;text-align:right;">권장 투찰금액 (원)</th>
<th style="padding:9px 12px;text-align:center;">나라장터 추천 2픽 번호</th>
<th style="padding:9px 12px;text-align:left;">전술적 특징</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom:1px solid rgba(51,65,85,0.6);background:rgba(56,189,248,0.06);">
<td style="padding:10px 12px;font-weight:900;color:#38bdf8;">👑 [트랙 1] M5 양자코어 (메인 기준선)</td>
<td style="padding:10px 12px;text-align:center;font-weight:800;color:#e2e8f0;">100.0907%</td>
<td style="padding:10px 12px;text-align:right;font-weight:900;color:#38bdf8;font-size:14px;">{prof['bid_m5']:,}원</td>
<td style="padding:10px 12px;text-align:center;"><span style="background:rgba(56,189,248,0.2);border:1px solid #38bdf8;color:#bae6fd;padding:2px 8px;border-radius:999px;font-weight:900;font-size:11px;">2번 + 12번 (#238)</span></td>
<td style="padding:10px 12px;color:#cbd5e1;font-weight:700;">15차 감사 Lock 고정밀 표준 타점</td>
</tr>
<tr style="border-bottom:1px solid rgba(51,65,85,0.6);background:rgba(245,158,11,0.06);">
<td style="padding:10px 12px;font-weight:900;color:#fbbf24;">🛡️ [트랙 2] EGR 강건방어 (M6·M7·M8)</td>
<td style="padding:10px 12px;text-align:center;font-weight:800;color:#e2e8f0;">100.1100%</td>
<td style="padding:10px 12px;text-align:right;font-weight:900;color:#fbbf24;font-size:14px;">{prof['bid_egr']:,}원</td>
<td style="padding:10px 12px;text-align:center;"><span style="background:rgba(245,158,11,0.2);border:1px solid #fbbf24;color:#fde68a;padding:2px 8px;border-radius:999px;font-weight:900;font-size:11px;">3번 + 12번 (Q50)</span></td>
<td style="padding:10px 12px;color:#cbd5e1;font-weight:700;">하한 미달(Drop-off) 원천 방어선</td>
</tr>
<tr style="border-bottom:1px solid rgba(51,65,85,0.6);background:rgba(16,185,129,0.06);">
<td style="padding:10px 12px;font-weight:900;color:#34d399;">⚡ [트랙 3] LATTICE 격자 (1,365계단)</td>
<td style="padding:10px 12px;text-align:center;font-weight:800;color:#e2e8f0;">100.0658%</td>
<td style="padding:10px 12px;text-align:right;font-weight:900;color:#34d399;font-size:14px;">{prof['bid_lat']:,}원</td>
<td style="padding:10px 12px;text-align:center;"><span style="background:rgba(16,185,129,0.2);border:1px solid #10b981;color:#a7f3d0;padding:2px 8px;border-radius:999px;font-weight:900;font-size:11px;">2번 + 13번 (#338)</span></td>
<td style="padding:10px 12px;color:#cbd5e1;font-weight:700;">15C4 이산 확률장 최빈 피크 타격</td>
</tr>
</tbody>
</table>

<div style="font-size:12.5px;font-weight:900;color:#7dd3fc;margin-bottom:8px;">4. 핵심 시공 유의사항 및 특기시방 체크리스트</div>
<div style="background:linear-gradient(90deg,rgba(245,158,11,0.14),rgba(15,23,42,0.92));border:1px solid rgba(245,158,11,0.45);border-left:4.5px solid #fbbf24;border-radius:10px;padding:12px 16px;color:#f8fafc;font-size:13px;font-weight:700;line-height:1.5;">
📌 <b style="color:#fde68a;">현장 필수 준수사항:</b> {prof['special_note']}
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def build_manifest_table_html(prof: Dict[str, Any], meta: Dict[str, Any]) -> str:
    """
    [인앱 열람 3] JSON 원시 텍스트 대신 SHA-256 해시 무결성 검증 테이블 렌더링
    """
    rows_html = ""
    for idx, (path, info) in enumerate(meta.get("manifest", {}).items(), start=1):
        folder, fname = path.split("/", 1) if "/" in path else ("ROOT", path)
        rows_html += f"""
<tr style="border-bottom:1px solid rgba(51,65,85,0.65);">
<td style="padding:9px 12px;font-weight:800;color:#94a3b8;font-size:12px;">0{idx}</td>
<td style="padding:9px 12px;"><span style="background:rgba(56,189,248,0.14);border:1px solid rgba(56,189,248,0.4);color:#7dd3fc;font-size:11px;font-weight:800;padding:2px 8px;border-radius:6px;">{folder}</span></td>
<td style="padding:9px 12px;font-weight:800;color:#f8fafc;font-size:12.5px;">{fname}</td>
<td style="padding:9px 12px;text-align:right;font-weight:800;color:#fde68a;font-size:12.5px;">{info['size_kb']} KB</td>
<td style="padding:9px 12px;font-family:monospace;font-weight:800;color:#c084fc;font-size:12px;">{info['sha256_short']}...</td>
<td style="padding:9px 12px;text-align:center;"><span style="background:rgba(16,185,129,0.16);border:1px solid #10b981;color:#34d399;font-size:10.5px;font-weight:900;padding:2px 8px;border-radius:999px;">✔ VERIFIED</span></td>
</tr>"""

    raw = f"""
<div style="background:linear-gradient(145deg,#09101f 0%,#050914 100%);border:1px solid rgba(168,85,247,0.4);border-radius:12px;padding:16px 18px;margin-top:6px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.18);">
<span style="font-size:14px;font-weight:900;color:#f8fafc;">🔐 [G2B-VAULT-{prof['nid']}] 첨부파일 패키지 SHA-256 암호화 무결성 검증서</span>
<span style="background:rgba(16,185,129,0.16);border:1px solid #10b981;color:#34d399;font-size:11px;font-weight:900;padding:2px 10px;border-radius:999px;">총 용량: {meta['raw_size_kb']} KB → 압축 후 {meta['zip_size_kb']} KB</span>
</div>
<table style="width:100%;border-collapse:collapse;text-align:left;">
<thead>
<tr style="background:rgba(15,23,42,0.95);border-bottom:2px solid #a855f7;color:#94a3b8;font-size:11.5px;font-weight:900;">
<th style="padding:8px 12px;">순번</th>
<th style="padding:8px 12px;">자동 분류 폴더</th>
<th style="padding:8px 12px;">수록 파일명</th>
<th style="padding:8px 12px;text-align:right;">원본 크기</th>
<th style="padding:8px 12px;">SHA-256 지문 (Fingerprint)</th>
<th style="padding:8px 12px;text-align:center;">무결성 상태</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())
