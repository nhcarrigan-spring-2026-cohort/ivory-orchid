from flask import Blueprint, Response

data_bp = Blueprint('data', __name__, url_prefix='/data')

USE_DUMMY_VALUES = True #until the db is implemented

if USE_DUMMY_VALUES:
	#this is here until there is some real data structure
	class Pet:
		name: str
		age: int
		sex: str
		description: str
		image_path: str
		size: float
		shelter_name: str
		status: bool
		animal: str

	# this is here until there is some real data structure
	class Shelter:
		name: str
		email: str
		phone_number: str
		address: str

	def get_pets() -> list[Pet]:
		dog1 = Pet()
		dog1.name = "rex"
		dog1.sex = "male"
		dog1.age = 10
		dog1.description = "calm border-collie"
		dog1.shelter_name = "cohort"
		dog1.status = True
		dog1.size = 6.25
		dog1.image_path = "Kripto.jpg"
		dog1.animal = "dog"

		dog2 = Pet()
		dog2.name = "max"
		dog2.sex = "male"
		dog2.age = 3
		dog2.description = "survived a car crash"
		dog2.shelter_name = "shelterB"
		dog2.status = True
		dog2.size = 2.1
		dog2.image_path = "dogandcat.jpg"
		dog2.animal = "dog"

		dog3 = Pet()
		dog3.name = "bella"
		dog3.sex = "female"
		dog3.age = 1
		dog3.description = "loves big walks, needs attention"
		dog3.shelter_name = "cohort"
		dog3.status = True
		dog3.size = 6.25
		dog3.image_path = "Kripto.jpg"
		dog3.animal = "dog"

		cat1 = Pet()
		cat1.name = "Snowball"
		cat1.sex = "male"
		cat1.age = 10
		cat1.description = "Full of energy"
		cat1.shelter_name = "shelterB"
		cat1.status = True
		cat1.size = 15
		cat1.image_path = "dogandcat.jpg"
		cat1.animal = "cat"

		cat2 = Pet()
		cat2.name = "fog"
		cat2.sex = "female"
		cat2.age = 10
		cat2.description = "has an interesting color"
		cat2.shelter_name = "cohort"
		cat2.status = True
		cat2.size = 3
		cat2.image_path = "snowball.jpg"
		cat2.animal = "cat"

		cat3 = Pet()
		cat3.name = "sunny"
		cat3.sex = "female"
		cat3.age = 10
		cat3.description = "Very fat"
		cat3.shelter_name = "closedShelter"
		cat3.status = False
		cat3.size = 8
		cat3.image_path = "dogandcat.jpg"
		cat3.animal = "cat"

		return [dog1, dog2, dog3, cat1, cat2, cat3]

	def get_shelters() -> list[Shelter]:
		shelter_cohort = Shelter()
		shelter_cohort.name = "cohort"
		shelter_cohort.email = "ivory-orchid@cohort.org"
		shelter_cohort.phone_number = "+156547896542"
		shelter_cohort.address = "12 rue de Prony, 75017 Paris, France"

		shelter_b = Shelter()
		shelter_b.name = "shelterB"
		shelter_b.email = "shelters@ivory.orchid.org"
		shelter_b.phone_number = "+156547896542"
		shelter_b.address = "760 United Nations Plaza, New York, NY 10017, USA"

		shelter_closed = Shelter()
		shelter_closed.name = "closedShelter"
		shelter_closed.email = "automations@example.com"
		shelter_closed.phone_number = "+0123456789"
		shelter_closed.address = "1600 Pennsylvania Ave NW, Washington, DC 20500, USA"

		return [shelter_cohort, shelter_b, shelter_closed]

	def pet_mapper(pet: Pet):
		return [
			("name", pet.name),
			("shelter", pet.shelter_name),
			("sex", pet.sex),
			("type", pet.animal),
			("age", pet.age),
			("description", pet.description),
			("size", pet.size),
			("image", pet.image_path),
			("status", "pending" if pet.status else "available")
		]

	def shelter_mapper(shelter: Shelter):
		return [
			("name", shelter.name),
			("email", shelter.email),
			("phone", shelter.phone_number),
			("address", shelter.address)
		]

@data_bp.route('/pets')
@data_bp.route('/pets.json')
def pets():
	return Response(jsonify(get_pets(), pet_mapper), mimetype="application/json")

@data_bp.route('/shelters')
@data_bp.route('/shelters.json')
def shelters():
	return Response(jsonify(get_shelters(), shelter_mapper), mimetype="application/json")

def jsonify(data: list | str | float | int, mapper = None) -> str:
	if isinstance(data, list):
		if mapper is None:
			mapper = lambda x: str(x)

		result = ""
		is_object = False #True if it's an object, false if it's a list
		for item in data:
			if isinstance(item, list):
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
