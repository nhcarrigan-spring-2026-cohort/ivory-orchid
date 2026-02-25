from abc import ABC, abstractmethod
from enum import Enum

from sqlalchemy.orm import Mapped

from . import db

class JsonType(Enum):
    Full = 1
    Short = 2

class Jsonifable(ABC):
    @abstractmethod
    def json(self, json_type: JsonType = JsonType.Full) -> str:
        pass

#Fix multiple metaclass error with multiple inheritance
class CommonMetaclass(type(Jsonifable), type(db.Model)):
    pass

class Shelter(Jsonifable, db.Model, metaclass=CommonMetaclass):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]
    address: Mapped[str]

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

class Pet(Jsonifable, db.Model, metaclass=CommonMetaclass):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    sex: Mapped[str]
    description: Mapped[str]
    image_path: Mapped[str]
    size: Mapped[float]
    shelter_name: Mapped[str]
    status: Mapped[bool]
    animal: Mapped[str]

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
