import frappe
from frappe.model.naming import make_autoname
from frappe.utils import nowdate
from frappe import _


def before_insert(doc, method):
    gate_pass_date = doc.gate_pass_date or nowdate()

    fy = frappe.db.get_value("Fiscal Year",{"year_start_date": ["<=", gate_pass_date], "year_end_date": [">=", gate_pass_date],"disabled": 0}, "name")

    if not fy:
        frappe.throw(_("No active Fiscal Year found for today. Please add a Fiscal Year."))

    
    company_abbr = frappe.db.get_value("Company",doc.company,"abbr")[:1]
    branch = frappe.db.get_value("Branch",doc.branch,"custom_branch_code")
   
    if not branch:
        frappe.throw(_("Please set the Branch Code in Branch Master for branch"))

    doc.naming_series = f"{company_abbr}{branch}S{fy}-.#"
    doc.name = make_autoname(f"{company_abbr}{branch}S{fy}-.#")
