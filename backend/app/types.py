from abc import ABC, abstractmethod
from enum import Enum

class JsonType(Enum):
    Full = 1
    Short = 2

class Jsonifable(ABC):
    @abstractmethod
    def json(self, json_type: JsonType = JsonType.Full) -> str:
        pass

class Shelter(Jsonifable):
    id: int = -1
    name: str
    email: str
    phone_number: str
    address: str

    def __init__(self, name: str, email: str, phone_number: str, address: str):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address

    def json(self, json_type: JsonType = JsonType.Full) -> str:
        return ("{\"id\":" + str(self.id) +
                ",\"name\":\"" + self.name +
                "\",\"email\":\"" + self.email +
                "\",\"phone\":\"" + self.phone_number +
                "\",\"address\":\"" + self.address + "\"}")

class Pet(Jsonifable):
    id: int = -1
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

    def json(self, json_type: JsonType = JsonType.Full) -> str:
        if json_type == JsonType.Short:
            return ("{\"id\":" + str(self.id) +
                    ",\"name\":\"" + self.name +
                    "\",\"age\":" + str(self.age) +
                    ",\"description\":\"" + self.description +
                    "\",\"type\":\"" + self.animal +
                    "\",\"image\":\"" + self.image_path +"\"}")

        status = "\"status\":\"pending\"}" if self.status else "\"status\":\"available\"}"
        return ("{\"id\":" + str(self.id) +
                ",\"name\":\"" + self.name +
                "\",\"age\":" + str(self.age) +
                "\",\"sex\":\"" + self.sex +
                "\",\"type\":\"" + self.animal +
                "\",\"description\":\"" + self.description +
                "\",\"size\":" + str(self.size) +
                ",\"image\":\"" + self.image_path +
                "\",\"animal\":\"" + self.animal +
                status)
