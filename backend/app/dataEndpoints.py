from flask import Blueprint, Response

from .types import *

data_bp = Blueprint('data', __name__, url_prefix='/api')

@data_bp.route('/pets', methods = ['GET'])
def full_pets_list():
	return Response(jsonify(Pet.query.all(), JsonType.Short), mimetype="application/json")

@data_bp.route('/pets/<int:pet_id>', methods = ['GET'])
def pets_list_by_id(pet_id: int):
	return Response(jsonify(Pet.query.filter_by(id=pet_id).all(), JsonType.Full), mimetype="application/json")
s_sh = True
@data_bp.route('/shelters', methods = ['GET'])
def all_shelters():
	return Response(jsonify(Shelter.query.all(), JsonType.Short), mimetype="application/json")

@data_bp.route('/shelters/<int:shelter_id>', methods = ['GET'])
def shelters_list_by_id(shelter_id: int):
	return Response(jsonify(Shelter.query.filter_by(id=shelter_id).all(), JsonType.Full), mimetype="application/json")

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
