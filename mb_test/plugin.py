import frappe
from frappe import _


def assesment_renderer(quiz_name, lms_batch):
	if frappe.session.user == "Guest":
		return " <div class='alert alert-info'>" + _(
			"Quiz is not available to Guest users. Please login to continue."
		)
		+"</div>"



	quiz = frappe.db.get_value("Assessment",quiz_name,["name","title","max_attempts","show_answers","show_submission_history","passing_percentage","heading","video_id","time","likert_scale",],as_dict=True,)
	quiz.questions = []
	fields = ["name", "question", "type", "multiple", "required_explanation"]
	for num in range(1, 11):
		fields.append(f"option_{num}")
		fields.append(f"is_correct_{num}")
		fields.append(f"explanation_{num}")
		fields.append(f"possibility_{num}")

	questions = frappe.get_all("Assessment Quiz Question",filters={"parent": quiz.name},fields=["question", "marks"],order_by="idx",)

	for question in questions:
		details = frappe.db.get_value("Assessment Question", question.question, fields, as_dict=1)
		details["marks"] = question.marks
		quiz.questions.append(details)

	no_of_attempts = frappe.db.get_value("Assessment Submission",
		{"member": frappe.session.user, "quiz": quiz_name, "lms_batch": lms_batch},
		["no_of_attempts"],)
	if not no_of_attempts:
		no_of_attempts = 0

	if quiz.show_submission_history:
		all_submissions = frappe.get_all(
			"Assessment Submission",
			{
				"quiz": quiz.name,
				"member": frappe.session.user,
			},
			["name", "score", "creation"],
			order_by="creation desc",
		)

	return frappe.render_template(
		"templates/macro/assessment.html",
		{
			"quiz": quiz,
			"no_of_attempts": no_of_attempts,
			"all_submissions": all_submissions if quiz.show_submission_history else None,
			"hide_quiz": False,
			"lms_batch": lms_batch,
		},
	)


def summary_renderer(name):
	have_question = 0
	have_answer = 0
	answer = ""

	if frappe.db.exists("Summary", {"course_lesson": name}):
		have_question = 1
		title, question, instructors = frappe.db.get_value(
			"Summary",
			{"course_lesson": name},
			["title", "question", "instructors_comments"],
		)

		if frappe.db.exists("Summary Submission", {"member": frappe.session.user, "lesson": name}):
			have_answer = 1
			answer = frappe.db.get_value(
				"Summary Submission",
				{"member": frappe.session.user, "lesson": name},
				["answer"],
			)

		context = {
			"name": name,
			"have_question": have_question,
			"title": title,
			"question": question,
			"instructors": instructors,
			"answer": answer,
			"have_answer": have_answer,
		}
		return frappe.render_template("mb_fxlh/templates/macro/summary.html", context)
	return ""


@frappe.whitelist(allow_guest=True)
def make_summary_submission(lesson, answer):
	if frappe.db.exists("Summary", {"course_lesson": lesson}):
		name, question, instructors = frappe.db.get_value(
			"Summary",
			{"course_lesson": lesson},
			["name", "question", "instructors_comments"],
		)

		ss_doc = frappe.get_doc(
			{
				"doctype": "Summary Submission",
				"member": frappe.session.user,
				"lesson": lesson,
				"answer": answer,
				"summary": name,
			}
		)
		ss_doc.insert(
			ignore_permissions=True,  # ignore write permissions during insert
			ignore_links=True,  # ignore Link validation in the document
			ignore_if_duplicate=True,  # dont insert if DuplicateEntryError is thrown
			ignore_mandatory=True,  # insert even if mandatory fields are not set
		)

		frappe.db.commit()

		return True


# mb_fxlh.patches.zoom_user_for_youth_master
