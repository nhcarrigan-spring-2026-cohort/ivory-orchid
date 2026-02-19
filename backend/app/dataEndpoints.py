from flask import Blueprint, Response

from .types import *

data_bp = Blueprint('data', __name__, url_prefix='/data')

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

@data_bp.route('/pets')
@data_bp.route('/pets.json')
def pets():
	return Response(jsonify(get_pets()), mimetype="application/json")

@data_bp.route('/shelters')
@data_bp.route('/shelters.json')
def shelters():
	return Response(jsonify(get_shelters()), mimetype="application/json")

def jsonify(data, mapper = None) -> str:
	"""
	Function to convert an object to a JSON string

	Lists will be converted into JSON arrays

	Lists of tuple of 2 elements will be converted into an object where the first element is the key and the second the value

	A types.Jsonifable object will be converted into its JSON representation using the object's json() method

	Anything else will be passed to the mapper function (defaults to calling str()) which shall return a string
	"""
	if isinstance(data, Jsonifable):
		return data.json()
	if isinstance(data, list):
		if mapper is None:
			mapper = lambda x: str(x)

		result = ""
		is_object = False #True if it's an object, false if it's a list
		for item in data:
			if isinstance(item, Jsonifable):
				result += item.json() + ","
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
