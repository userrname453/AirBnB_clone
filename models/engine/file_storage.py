#!/usr/bin/python3
"""Module for the FileStorage class."""
import datetime
import json
import os


class FileStorage:
    """Handles serialization and deserialization of instances to and from JSON files."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the __objects dictionary."""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the __objects dictionary."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to a JSON file."""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            serialized_data = {key: value.to_dict() for key, value in FileStorage.__objects.items()}
            json.dump(serialized_data, file)

    def classes(self):
        """Returns the dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        valid_classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        return valid_classes

    def reload(self):
        """Deserializes the JSON file back into __objects."""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            loaded_data = json.load(file)
            deserialized_objects = {key: self.classes()[value["__class__"]](**value)
                                    for key, value in loaded_data.items()}
            FileStorage.__objects = deserialized_objects

    def attributes(self):
        """Returns the valid attributes and their types for each class."""
        valid_attributes = {
            "BaseModel": {
                "id": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime
            },
            "User": {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str
            },
            "State": {
                "name": str
            },
            "City": {
                "state_id": str,
                "name": str
            },
            "Amenity": {
                "name": str
            },
            "Place": {
                "city_id": str,
                "user_id": str,
                "name": str,
                "description": str,
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "price_by_night": int,
                "latitude": float,
                "longitude": float,
                "amenity_ids": list
            },
            "Review": {
                "place_id": str,
                "user_id": str,
                "text": str
            }
        }
        return valid_attributes
