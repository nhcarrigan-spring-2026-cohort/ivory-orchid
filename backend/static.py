from flask import render_template
from flask import request
from flask import send_file

from werkzeug.security import safe_join
import os

from . import app

#Directory where non-template files are searched
#Those paths are not checked
#They will be first searched in FRONTEND, and then in the entry of FRONTEND_SPECIFIC
FRONTEND = os.path.join(os.path.dirname(__file__), "../frontend")
#Map of file extensions to directories, relative to FRONTEND
#FRONTEND_SPECIFIC = {"js": "js", "css": "css", "html": "static"}
FRONTEND_SPECIFIC = {"js": "js", "css": "css"}

#The name of the 404 page template
TEMPLATE_404 = "404.html"

#Add here all the pages that have a different endpoint from the page name
@app.route("/")
def main_page():
	return render_template("index.html")

#Handles all pages not generated dynamically
#Will return the page if found, else the TEMPLATE_404 template will be returned to the client
@app.errorhandler(404)
def load_static(e):
	paths = set()
	paths.add(FRONTEND)

	try:
		return render_template(request.path.split("/")[-1])
	except:
		print("Template " + request.path.split("/")[-1] + " not found")

	filetype = request.path.split(".")[-1]
	if(filetype in FRONTEND_SPECIFIC):
		paths.add(os.path.join(FRONTEND, FRONTEND_SPECIFIC[filetype]))

	for path in paths:
		path = safe_join(path, request.path.lstrip("/"))
		if(os.path.exists(path)):
			return send_file(path)

	return render_template(TEMPLATE_404), 404
