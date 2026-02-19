from abc import ABC, abstractmethod

class Jsonifable(ABC):
	@abstractmethod
	def json(self) -> str:
		pass

class Shelter(Jsonifable):
	name: str
	email: str
	phone_number: str
	address: str

	def __init__(self, name: str, email: str, phone_number: str, address: str):
		self.name = name
		self.email = email
		self.phone_number = phone_number
		self.address = address

	def json(self) -> str:
		return ("{\"name\":\"" + self.name +
				"\",\"email\":\"" + self.email +
				"\",\"phone\":\"" + self.phone_number +
				"\",\"address\":\"" + self.address + "\"}")

class Pet(Jsonifable):
	name: str
	age: int
	sex: str
	description: str
	image_path: str
	size: float
	shelter_name: str
	status: bool
	animal: str

	def __init__(self, name: str, age: int, sex: str, description: str,
				 image_path: str, size: float, shelter_name: str, status: bool, animal: str):
		self.name = name
		self.age = age
		self.sex = sex
		self.description = description
		self.image_path = image_path
		self.size = size
		self.shelter_name = shelter_name
		self.status = status
		self.animal = animal

	def json(self) -> str:
		status = "\"status\":\"pending\"}" if self.status else "\"status\":\"available\"}"
		return ("{\"name\":\"" + self.name +
				"\",\"age\":" + str(self.age) +
				"\",\"sex\":\"" + self.sex +
				"\",\"type\":\"" + self.animal +
				"\",\"age\":" + str(self.age) +
				",\"description\":\"n" + self.description +
				"\",\"size\":" + str(self.size) +
				"	,\"image\":\"" + self.image_path +
				"\",\"animal\":\"" + self.animal +
				status)
