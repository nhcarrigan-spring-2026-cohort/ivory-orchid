from flask import Blueprint, render_template, Response, request, send_file, jsonify as flask_jsonify
from jinja2 import TemplateNotFound
from werkzeug.security import safe_join
from sqlalchemy.exc import IntegrityError
import os

from . import db, utils
from .models import Contact
from .validators import validate_contact_data

static_bp = Blueprint('static', __name__)

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
@static_bp.route("/")
def main_page():
	return get_page_or_template("index.html", default="The site is currently unavailable (maybe it's in maintenance?)\ncode: index404")

@static_bp.route("/contact", methods=["GET", "POST"])
@static_bp.route("/contact.html", methods=["GET", "POST"])
def contact_page():
	"""
	Handle contact form submissions with validation and database persistence.
	
	GET: Render the contact form.
	POST: Validate data, store in database, send webhook inquiry, and return response.
	"""
	if request.method == "GET":
		result = get_page_or_template("contact.html")
		if isinstance(result, str) and len(result) == 0:
			return get_page_or_template(FILE_404, TEMPLATE_404, "The requested page does not exists"), 404
		return result
	
	# Handle POST request
	# Accept both form data and JSON
	if request.is_json:
		data = request.get_json()
	else:
		data = request.form.to_dict()
	
	# Validate contact data
	is_valid, errors = validate_contact_data(data)
	if not is_valid:
		return flask_jsonify({
			"message": "Validation failed",
			"errors": errors
		}), 400
	
	try:
		# Create contact record in database
		new_contact = Contact(
			name=data['name'].strip(),
			email=data['email'].strip(),
			message=data['message'].strip()
		)
		
		db.session.add(new_contact)
		db.session.commit()
		
		# Send webhook inquiry if configured
		utils.send_inquiry(data)
		
		# Return JSON response for API requests, HTML for form submissions
		if request.is_json:
			return flask_jsonify({
				"message": "Contact form submitted successfully",
				"contact": new_contact.to_dict()
			}), 201
		else:
			# For regular form submissions, return HTML response
			return "<html><head></head><body>Request successfully sent!\n<a href=\"/\">Return to the home</a></body></html>"
	
	except IntegrityError:
		db.session.rollback()
		return flask_jsonify({
			"message": "Error processing request",
			"error": "Database error occurred"
		}), 409
	except Exception as e:
		db.session.rollback()
		return flask_jsonify({
			"message": "Internal server error",
			"error": str(e)
		}), 500

#Handles all pages not generated dynamically
#Will return the page if found, else the TEMPLATE_404 template will be returned to the client
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

	if "." in request.path:
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
