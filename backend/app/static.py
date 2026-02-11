from flask import render_template, Response
from flask import request
from flask import send_file
from jinja2 import TemplateNotFound

from werkzeug.security import safe_join
import os

from . import app

#Directory where non-template files are searched
#Those paths are not checked
#They will be first searched in FRONTEND, and then in the entry of FRONTEND_SPECIFIC
FRONTEND_DIRECTORY = os.path.join(os.path.dirname(__file__), "../../frontend")
#Map of file extensions to directories, relative to FRONTEND
FRONTEND_SPECIFIC = {"js": "js", "css": "css", "png": "img", "jpg": "img"}

#The name of the 404-page template
TEMPLATE_404 = "404.html"
#The 404 static version of the page (fallback if the template version does not work)
FILE_404 = "404.html"

#Add here all the pages that have a different endpoint from the page name
@app.route("/")
def main_page():
	return get_page_or_template("index.html", default="The site is currently unavailable (maybe it's in maintenance?)\ncode: index404")

@app.route("/contact", methods=["GET", "POST"])
@app.route("/contact.html", methods=["GET", "POST"])
def contact_page():
	print(request.method)
	if request.method == "GET":
		result = get_page_or_template("contact.html")
		if isinstance(result, str) and len(result) == 0:
			return get_page_or_template(FILE_404, TEMPLATE_404, "The requested page does not exists"), 404
		return result
	print(request.form)
	return "Request successfully sent!"

#Handles all pages not generated dynamically
#Will return the page if found, else the TEMPLATE_404 template will be returned to the client
@app.errorhandler(404)
def load_static(e):
	# Prevent direct access to templates
	if request.path.__contains__("templates"):
		return get_page_or_template(FILE_404, TEMPLATE_404, "The requested page does not exists"), 404

	paths = set()
	paths.add(FRONTEND_DIRECTORY)

	try:
		return render_template(request.path.split("/")[-1])
	except TemplateNotFound:
		pass

	if request.path.contains("."):
		filetype = request.path.split(".")[-1]
	else: filetype = "html"

	if filetype in FRONTEND_SPECIFIC:
		paths.add(os.path.join(FRONTEND_DIRECTORY, FRONTEND_SPECIFIC[filetype]))

	for path in paths:
		path = safe_join(path, request.path.lstrip("/"))
		if os.path.exists(path):
			return send_file(path)

	return get_page_or_template(FILE_404, TEMPLATE_404, "An internal error occurred while trying to return the 404 error page"), 404

def get_page_or_template(page_name: str, template_name: str | None = None, default: str | None = None) -> str | Response:
	if template_name is None:
		template_name = page_name
	try:
		return render_template(template_name)
	except TemplateNotFound:
		# noinspection PyBroadException
		try:
			return send_file(safe_join(FRONTEND_DIRECTORY, page_name))
		except:
			if default is None:
				return ""
			return default
