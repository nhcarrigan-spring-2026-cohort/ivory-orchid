from flask import Blueprint, Response, request, jsonify as flask_jsonify
from sqlalchemy.exc import IntegrityError

from .types import *
from . import db
from .models import User
from .validators import validate_user_data

data_bp = Blueprint('data', __name__, url_prefix='/api')

USE_DUMMY_VALUES = True #until the db is implemented

if USE_DUMMY_VALUES:
	def get_pets() -> list[Pet]:
		dog1 = Pet("rex", 10, "male", "calm border-collie", "kripto.jpg", 6.25, "cohort", True, "dog")
		dog2 = Pet("max", 3, "male", "survived a car crash", "dogandcat.jpg", 2.1, "shelterB", True, "dog")
		dog3 = Pet("bella", 1, "female", "loves big walks, needs attention", "kripto.jpg", 6.25, "cohort", True, "dog")

		cat1 = Pet("Snowball", 10, "male", "Full of energy", "dogandcat.jpg", 15, "shelterB", True, "cat")
		cat2 = Pet("fog", 10, "female", "has an interesting color", "snowball.jpg", 3, "cohort", True, "cat")
		cat3 = Pet("sunny", 10, "female", "Very fat", "dogandcat.jpg", 8, "closedShelter", False, "cat")

		return [dog1, dog2, dog3, cat1, cat2, cat3]

	def get_shelters() -> list[Shelter]:
		shelter_cohort = Shelter("cohort", "ivory-orchid@cohort.org", "+156547896542", "12 rue de Prony, 75017 Paris, France")
		shelter_b = Shelter("shelterB", "shelters@ivory.orchid.org", "+215654789564", "760 United Nations Plaza, New York, NY 10017, USA")
		shelter_closed = Shelter("closedShelter", "automations@example.com","+0123456789","1600 Pennsylvania Ave NW, Washington, DC 20500, USA")

		return [shelter_cohort, shelter_b, shelter_closed]
	#endif USE_DUMMY_VALUES

@data_bp.route('/pets', methods = ['GET'])
def full_pets_list():
	return Response(jsonify(get_pets(), JsonType.Short), mimetype="application/json")

@data_bp.route('/pets/<int:pet_id>', methods = ['GET'])
def pets_list_by_id(pet_id: int):
	pets = list()
	for pet in get_pets():
		if pet.id == pet_id:
			pets.append(pet)
	return Response(jsonify(pets, JsonType.Full), mimetype="application/json")

@data_bp.route('/shelters', methods = ['GET'])
def all_shelters():
	return Response(jsonify(get_shelters(), JsonType.Short), mimetype="application/json")

@data_bp.route('/shelters/<int:shelter_id>', methods = ['GET'])
def shelters_list_by_id(shelter_id: int):
	shelters = list()
	for shelter in get_shelters():
		if shelter.id == shelter_id:
				shelters.append(shelter)
	return Response(jsonify(shelters, JsonType.Full), mimetype="application/json")

def jsonify(data, json_type: JsonType, mapper = None) -> str:
	"""
	Function to convert an object to a JSON string

	Lists will be converted into JSON arrays

	Lists of tuple of 2 elements will be converted into an object where the first element is the key and the second the value

	A types.Jsonifable object will be converted into its JSON representation using the object's json() method

	Anything else will be passed to the mapper function (defaults to calling str()) which shall return a string
	"""
	if isinstance(data, Jsonifable):
		return data.json(json_type)
	if isinstance(data, list):
		if mapper is None:
			mapper = lambda x: str(x)

		result = ""
		is_object = False #True if it's an object, false if it's a list
		for item in data:
			if isinstance(item, Jsonifable):
				result += item.json(json_type) + ","
			elif isinstance(item, list):
				result += jsonify(item, mapper) + ","

			elif isinstance(item, tuple):
				is_object = True
				if isinstance(item[1], list):
					result += "\"" + str(item[0]) + "\":\"" + jsonify(item[1]) + "\","
				else:
					result += "\"" + str(item[0]) + "\":\"" + str(item[1]) + "\","

			else: #value is a string or a number or an object, so use the passed mapper
				obj = mapper(item)
				if isinstance(obj, list) | isinstance(obj, tuple): #Jsonify that also
					result += jsonify(obj, mapper) + ","
				else:
					result += obj + ","

		if is_object:
			result = "{" + result[:-1] + "}"
		else:
			result = "[" + result[:-1] + "]"
		return result

	return data
@data_bp.route('/users/register', methods=['POST'])
def register_user():
	"""
	Register a new user with validation.
	
	Request body (JSON):
	{
		"name": "John Doe",
		"email": "john@example.com",
		"age": 25
	}
	
	Returns:
	- 201 Created: User successfully created
	  {
	    "message": "User registered successfully",
	    "user": {
	      "id": 1,
	      "name": "John Doe",
	      "email": "john@example.com",
	      "age": 25,
	      "created_at": "2026-02-22T10:30:00"
	    }
	  }
	
	- 400 Bad Request: Validation errors
	  {
	    "message": "Validation failed",
	    "errors": {
	      "email": "Invalid email format: ...",
	      "age": "Age must be a positive integer"
	    }
	  }
	
	- 409 Conflict: Email already exists
	  {
	    "message": "Email already registered",
	    "error": "A user with this email already exists"
	  }
	
	- 422 Unprocessable Entity: Malformed JSON
	  {
	    "message": "Invalid JSON data",
	    "error": "..."
	  }
	"""
	try:
		# Parse JSON data
		data = request.get_json()
		if not data:
			return flask_jsonify({
				"message": "Invalid JSON data",
				"error": "Request body must be valid JSON"
			}), 422
		
		# Validate input data
		is_valid, errors = validate_user_data(data)
		if not is_valid:
			return flask_jsonify({
				"message": "Validation failed",
				"errors": errors
			}), 400
		
		# Create new user
		new_user = User(
			name=data['name'].strip(),
			email=data['email'].strip(),
			age=int(data['age'])
		)
		
		# Add to database and commit
		db.session.add(new_user)
		db.session.commit()
		
		return flask_jsonify({
			"message": "User registered successfully",
			"user": new_user.to_dict()
		}), 201
		
	except IntegrityError:
		# Handle unique constraint violation (duplicate email)
		db.session.rollback()
		return flask_jsonify({
			"message": "Email already registered",
			"error": "A user with this email already exists"
		}), 409
	except Exception as e:
		# Handle unexpected errors (including JSON parsing errors)
		db.session.rollback()
		return flask_jsonify({
			"message": "Invalid JSON data",
			"error": str(e)
		}), 422