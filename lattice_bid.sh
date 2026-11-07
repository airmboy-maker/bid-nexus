#!/usr/bin/env python3
import os, sys, webbrowser
from decimal import Decimal
from bid_math_fixed import resolve_notice_record
from research.egr_bid.evidence_contract import VerifiedNotice
from research.egr_bid.robust_selector import egr_bid_recommend
from research.egr_bid.csv_loader import load_verified_history_from_csv
from research.egr_bid.report_formatter import (
    compute_m1_to_m5_breakdown, format_standardized_assessment_report, format_printable_html_report
)

arg1 = sys.argv[1].strip() if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "R26BK01812785-000"
rec = resolve_notice_record(arg1, strict=True, allow_demo=False)
notice = VerifiedNotice(
    notice_id=rec["internal_id"], revision_id="REV-0",
    source_sha256="41a5bfd7790732771f9430b13fb74c0ef7476f18",
    source_verified=rec["source_verified"], is_demo_data=rec["is_demo_data"],
    profile_key=rec["profile_key"], base_amt=rec["base_amt"], a_val=rec["a_val"],
    net_cost_base=rec["net_cost_base"], deadline_at=rec["deadline_date"], limit_rate=rec["limit_rate"],
)
hist = load_verified_history_from_csv("research/egr_bid/verified_opening_template.csv")
src_label = f"verified_opening_template.csv ({len(hist)}건)"
res = egr_bid_recommend(notice, hist, cost_input=None)
m1_m5 = compute_m1_to_m5_breakdown(rec["internal_id"], rec["base_amt"], rec["a_val"], rec["limit_rate"], Decimal("30.00"), rec["profile_key"], rec["net_cost_base"])

print(format_standardized_assessment_report(notice, rec["title"], res, m1_m5, src_label, report_mode="lattice_only"))
html_doc = format_printable_html_report(notice, rec["title"], res, m1_m5, src_label, standalone_doc=True, report_mode="lattice_only")
out_html = os.path.abspath(f"LATTICE1365_ASSESSMENT_{rec['internal_id']}.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_doc)
if "--no-open" not in sys.argv and os.environ.get("CI") != "true":
    try: webbrowser.open(f"file://{out_html}")
    except Exception: pass
