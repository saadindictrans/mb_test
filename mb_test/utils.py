import frappe


@frappe.whitelist
def f1_get_today():
	return frappe.utils.nowdate()


@frappe.whitelist
def f2_get_now():
	return frappe.utils.now()


@frappe.whitelist
def f3_add_days(d, days):
	return frappe.utils.add_days(d, int(days))


@frappe.whitelist
def f4_format_date(d):
	return frappe.utils.getdate(d).strftime("%d-%m-%Y")


@frappe.whitelist
def f5_get_doc(dt, name):
	return frappe.get_doc(dt, name)


@frappe.whitelist
def f6_get_all(dt):
	return frappe.get_all(dt, fields=["name"])


@frappe.whitelist
def f7_to_string(val):
	return frappe.utils.cstr(val)


@frappe.whitelist
def f8_now_datetime():
	return frappe.utils.now_datetime().isoformat()


@frappe.whitelist
def f9_custom_format(d, fmt):
	return frappe.utils.formatdate(d, fmt)


@frappe.whitelist
def f10_build_url(path):
	return frappe.utils.get_url(path)
