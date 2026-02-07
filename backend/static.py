from flask import render_template
from flask import request
from flask import send_file
from jinja2 import TemplateNotFound

from werkzeug.security import safe_join
import os

from . import app

#Directory where non-template files are searched
#Those paths are not checked
#They will be first searched in FRONTEND, and then in the entry of FRONTEND_SPECIFIC
FRONTEND_DIRECTORY = os.path.join(os.path.dirname(__file__), "../frontend")
#Map of file extensions to directories, relative to FRONTEND
FRONTEND_SPECIFIC = {"js": "js", "css": "css", "png": "img"}

#The name of the 404-page template
TEMPLATE_404 = "404.html"
#The 404 static version of the page (fallback if the template version does not work)
FILE_404 = "404.html"

#Add here all the pages that have a different endpoint from the page name
@app.route("/")
def main_page():
	try:
		return render_template("index.html")
	except TemplateNotFound:
		try:
			return send_file(os.path.join(FRONTEND_DIRECTORY, "index.html"))
		except:
			#this shouldn't ever happen, why would the index page disappear?
			return "the site is currently unavailable (maybe it's in maintenance?)\ncode: index404"

#Handles all pages not generated dynamically
#Will return the page if found, else the TEMPLATE_404 template will be returned to the client
@app.errorhandler(404)
def load_static(e):
	# Prevent direct access to templates
	if request.path.__contains__("templates"):
		return page_404(), 404

	paths = set()
	paths.add(FRONTEND_DIRECTORY)

	try:
		return render_template(request.path.split("/")[-1])
	except TemplateNotFound:
		pass

	filetype = request.path.split(".")[-1]
	if filetype in FRONTEND_SPECIFIC:
		paths.add(os.path.join(FRONTEND_DIRECTORY, FRONTEND_SPECIFIC[filetype]))

	for path in paths:
		path = safe_join(path, request.path.lstrip("/"))
		if os.path.exists(path):
			return send_file(path)

	return page_404(), 404

def page_404():
	"""Returns a 404 page and the 404 error-code"""
	try:
		return render_template(TEMPLATE_404)
	except TemplateNotFound:
		try:
			return send_file(FILE_404)
		except:
			return "An internal error occurred while trying to return the 404 error page "
