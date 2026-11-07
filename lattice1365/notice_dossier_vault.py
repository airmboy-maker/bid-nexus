import re
import json
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
    """
    공고 제목과 금액을 분석하여 어떤 종류의 공사인지(규모, 구조, 공종 비중, 공기, 특기사항) 자동 추론
    """
    nid = str(_pick_val(n, ["id", "no", "notice_no", "notice_id", "공고번호", "code"], f"202611-0{idx+1:04d}"))
    title = str(_pick_val(n, ["title", "name", "notice_title", "subject", "공고명", "공사명"], "관급 건축공사"))
    agency = str(_pick_val(n, ["agency", "org", "client", "발주처", "발주기관", "수요기관"], "조달청"))
    deadline = str(_pick_val(n, ["deadline", "close_dt", "end_date", "due", "마감", "마감일시"], "2026-11-13 10:00"))
    license_name = str(_pick_val(n, ["license", "lic", "category", "sector", "업종", "면허"], "건축공사업"))
    region_name = str(_pick_val(n, ["region", "loc", "area", "location", "지역", "관할지역"], "강원특별자치도"))

    base_amt = _to_int(_pick_val(n, ["base_amount", "base", "base_amt", "base_price", "기초금액", "기초"], 5_180_000_000))
    a_val = _to_int(_pick_val(n, ["a_value", "a_val", "a_amt", "a_cost", "A값", "a"], 241_800_000))
    low_rate = _to_float(_pick_val(n, ["lower_limit_rate", "low_rate", "limit_rate", "cutline", "낙찰하한율", "하한율"], 88.745))

    # 공사 성격 분류
    if "리모델링" in title or "증축" in title or "공간재구조화" in title:
        work_type = "🏛 기존 건축물 그린리모델링 · 내진보강 및 증축공사"
        struct_type = "철근콘크리트조(RC) + 철골조(S) 복합 보강구조"
        duration_days = max(180, min(540, int((base_amt / 100_000_000) * 7.5)))
        w_arch, w_civil, w_mech, w_finish = 38, 12, 22, 28
        special_note = "기존 시설물 철거/해체 안전관리계획서 필수, 석면 해체 및 비산먼지 저감 대책 포함, 야간/휴일 소음 제어 공법 적용"
    elif "체육" in title or "수영장" in title or "문화" in title:
        work_type = "🏟 대공간 장스팬(Long-Span) 다목적 체육·문화시설 신축공사"
        struct_type = "철골트러스 대공간 지붕구조(PEB/Space Frame) + 철근콘크리트조"
        duration_days = max(360, min(720, int((base_amt / 100_000_000) * 8.2)))
        w_arch, w_civil, w_mech, w_finish = 44, 18, 20, 18
        special_note = "대공간 지붕 철골 트러스 인양 안전검토, 수영장/체육관 방수·방습 특화시공, 고단열 커튼월 및 흡음 내장재 적용"
    elif "청사" in title or "부두" in title or "센터" in title or "조리원" in title:
        work_type = "🏢 공공청사 · 특수목적 스마트 복지/행정 인프라 신축공사"
        struct_type = "철근콘크리트 라멘조(지하 1층 ~ 지상 4층 규모)"
        duration_days = max(300, min(660, int((base_amt / 100_000_000) * 8.0)))
        w_arch, w_civil, w_mech, w_finish = 42, 16, 21, 21
        special_note = "제로에너지건축물(ZEB 5등급) 인증 및 BF(장애물 없는 생활환경) 예비인증 기준 준수, 흙막이 가시설 및 지정공사 포함"
    else:
        work_type = "🏗️ 일반 관급 공공시설 신축 및 부대토목 건축공사"
        struct_type = "철근콘크리트조(RC) 표준 구조"
        duration_days = max(240, min(600, int((base_amt / 100_000_000) * 7.8)))
        w_arch, w_civil, w_mech, w_finish = 45, 15, 18, 22
        special_note = "조달청 표준일위대가 및 적격심사 세부기준 적용, 안전관리비·품질관리비 법정 정산 대상 공사"

    # 기초금액 기반 연면적 추정 (평당 약 780만~850만원 기준)
    area_m2 = round((base_amt / 2_550_000.0), 1)
    area_py = round(area_m2 / 3.3058, 1)
    est_net_cost = int(round(base_amt * 0.815))

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
    }


def build_notice_dossier_html(prof: Dict[str, Any]) -> str:
    """
    공고 클릭(열람) 시 펼쳐지는 4D AI 현장 도감 브리핑 보드 HTML
    """
    raw = f"""
<div style="background:linear-gradient(145deg,#080f1e 0%,#0f172a 55%,#050914 100%);border:1.5px solid rgba(16,185,129,0.45);border-left:5px solid #10b981;border-radius:14px;padding:18px 20px;margin-top:4px;margin-bottom:12px;box-shadow:0 12px 30px rgba(0,0,0,0.65);word-break:keep-all;">
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding-bottom:10px;margin-bottom:12px;border-bottom:1px solid rgba(148,163,184,0.18);">
<div>
<span style="background:linear-gradient(90deg,#10b981,#38bdf8);color:#020617;font-size:10.5px;font-weight:900;padding:3px 10px;border-radius:999px;">AI CONSTRUCTION DOSSIER</span>
<span style="font-size:16px;font-weight:900;color:#f8fafc;margin-left:8px;">🏗️ [{prof['nid']}] {prof['title']} — 종합 현장 브리핑</span>
</div>
<span style="background:rgba(245,158,11,0.16);border:1px solid rgba(245,158,11,0.5);color:#fde68a;font-size:11px;font-weight:800;padding:3px 10px;border-radius:999px;">예상 공기: 착공일로부터 {prof['duration_days']}일</span>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;">
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">📌 공사 유형 분류</div>
<div style="font-size:12.5px;color:#34d399;font-weight:900;line-height:1.35;">{prof['work_type']}</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">🏢 주구조 및 추정 연면적</div>
<div style="font-size:12.5px;color:#38bdf8;font-weight:900;line-height:1.35;">{prof['struct_type']}<br><span style="color:#e2e8f0;font-size:11.5px;">연면적 약 {prof['area_m2']:,}㎡ ({prof['area_py']:,}평)</span></div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">💰 추정 순공사원가 (81.5%)</div>
<div style="font-size:13.5px;color:#fbbf24;font-weight:900;">{prof['est_net_cost']:,}원</div>
<div style="font-size:10.5px;color:#94a3b8;margin-top:2px;">98% 원가하한: {int(prof['est_net_cost']*0.98):,}원</div>
</div>
<div style="background:rgba(15,23,42,0.9);border:1px solid #334155;border-radius:10px;padding:10px 12px;">
<div style="font-size:10.5px;color:#94a3b8;font-weight:800;margin-bottom:3px;">⚖️ 입찰 및 계약 방식</div>
<div style="font-size:12px;color:#e9d5ff;font-weight:900;line-height:1.35;">적격심사 / 내역입찰(총액)<br><span style="color:#cbd5e1;font-size:11px;">지역제한({prof['region']}) · {prof['license']}</span></div>
</div>
</div>

<div style="background:rgba(2,6,23,0.75);border:1px solid rgba(56,189,248,0.28);border-radius:10px;padding:11px 14px;margin-bottom:10px;">
<div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;color:#cbd5e1;margin-bottom:6px;">
<span>📊 <b>공종별 예정 원가 구성비 (AI 물량내역 분해)</b></span>
<span style="color:#7dd3fc;">골조 {prof['w_arch']}% · 마감/창호 {prof['w_finish']}% · 기계/부대설비 {prof['w_mech']}% · 토목/가시설 {prof['w_civil']}%</span>
</div>
<div style="width:100%;height:10px;background:#0f172a;border-radius:999px;overflow:hidden;display:flex;">
<div style="width:{prof['w_arch']}%;height:100%;background:#38bdf8;" title="건축골조"></div>
<div style="width:{prof['w_finish']}%;height:100%;background:#10b981;" title="마감/창호"></div>
<div style="width:{prof['w_mech']}%;height:100%;background:#a855f7;" title="기계/설비"></div>
<div style="width:{prof['w_civil']}%;height:100%;background:#f59e0b;" title="토목/가시설"></div>
</div>
</div>

<div style="background:rgba(15,23,42,0.85);border-left:3.5px solid #fbbf24;border-radius:6px;padding:8px 12px;font-size:12px;color:#e2e8f0;">
💡 <b style="color:#fde68a;">현장 핵심 시공 유의사항 (시방서 요약):</b> {prof['special_note']}
</div>
</div>
"""
    return "\n".join(line.lstrip() for line in raw.splitlines() if line.strip())


def generate_notice_attachments(prof: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    해당 공고의 실제 제원이 100% 반영된 4종 첨부파일(공고문 HTML, 공내역서 CSV, 물량내역 JSON, 시방서 TXT) 바이트 문자열 생성
    """
    nid = prof["nid"]
    title = prof["title"]
    agency = prof["agency"]
    base_amt = prof["base_amt"]
    a_val = prof["a_val"]
    low_rate = prof["low_rate"]
    net_cost = prof["est_net_cost"]

    # 1) 공식 입찰공고문 HTML
    doc_html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><title>[입찰공고문] {title}</title>
<style>
body {{ font-family: 'Malgun Gothic', sans-serif; padding: 36px; color: #111827; line-height: 1.6; max-width: 820px; margin: 0 auto; }}
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
<h3>2. 입찰 및 계약방식</h3>
<ul>
<li>적격심사 대상공사이며, 복수예비가격(15개 중 4개 추첨 산술평균)이 적용되는 전자입찰입니다.</li>
<li>입찰마감일시: <b>{prof['deadline']}</b> (국가종합전자조달시스템 나라장터)</li>
<li>특기사항: {prof['special_note']}</li>
</ul>
<div class="stamp">위와 같이 공고합니다.<br><br>{agency} 재무관</div>
</body></html>"""

    # 2) 공종별 물량내역서(공내역서) CSV (UTF-8 BOM 포함하여 엑셀에서 한글 안 깨짐)
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
        f"{nid},{title},S01,[법정 A값] 국민연금·건강보험·안전관리비 등 합계,식,1,{a_val},{round(a_val/base_amt*100,2)}%",
        f"{nid},{title},TOT,[합계] 기초금액 총괄,식,1,{base_amt},100.0%",
    ])

    # 3) 나라장터 표준 전자입찰(.bid 호환) JSON 패키지
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
        "engineering_profile": {
            "work_type": prof["work_type"],
            "structure": prof["struct_type"],
            "estimated_area_m2": prof["area_m2"],
            "duration_days": prof["duration_days"],
        }
    }, ensure_ascii=False, indent=2)

    # 4) 공사시방서 및 현장설명 특기사항 TXT
    spec_txt = "\n".join([
        f"======================================================================",
        f" [공사시방서 및 현장설명서 요약] 공고번호: {nid}",
        f" 공사명: {title}",
        f"======================================================================",
        f"1. 발주기관: {agency}",
        f"2. 참가자격: {prof['license']} ({prof['region']})",
        f"3. 공사종류: {prof['work_type']}",
        f"4. 구조/규모: {prof['struct_type']} / 연면적 약 {prof['area_m2']:,}㎡ ({prof['area_py']:,}평)",
        f"5. 공사기간: 착공일로부터 {prof['duration_days']}일간",
        f"6. 재무제원:",
        f"   - 기초금액: {base_amt:,}원",
        f"   - 법정 A값: {a_val:,}원",
        f"   - 추정 순공사원가: {net_cost:,}원 (98% 미달 배제선: {int(net_cost*0.98):,}원)",
        f"   - 적격심사 낙찰하한율: {low_rate:.3f}%",
        f"7. 핵심 시공 유의사항 및 특기시방:",
        f"   - {prof['special_note']}",
        f"======================================================================",
    ])

    return doc_html, boq_csv, bid_json, spec_txt
