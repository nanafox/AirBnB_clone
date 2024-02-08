#!/usr/bin/python3

"""
This module defines the File Storage class that serializes instances to JSON
files deserializes JSON files to instances.
"""

import json
from typing import Any
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review


class FileStorage:
    """Defines the file storage model."""

    __file_path = "file_storage.json"
    __objects = {}
    __models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def all(self) -> dict:
        """
        Returns all the objects in the dictionary

        Returns:
            dict: A dictionary containing all serialized objects.
        """
        return self.__objects

    def new(self, obj: Any) -> None:
        """
        Saves a new instance to the objects dictionary

        Args:
            obj (Any): The object save in dictionary
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def reload(self) -> None:
        """Deserializes the json objects into their respective models."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                instances = json.load(json_file)

                for class_id, json_dict in instances.items():
                    obj_class = json_dict["__class__"]
                    self.__objects[class_id] = self.__models[obj_class](
                        **json_dict
                    )
        except (FileNotFoundError, PermissionError):
            pass

    def save(self) -> None:
        """
        Saves the contents of the dictionary containing the serialized objects.
        """
        instances = {}

        for class_id, obj in self.__objects.items():
            instances[class_id] = obj.to_dict()

        try:
            with open(self.__file_path, "w", encoding="utf-8") as json_file:
                json.dump(instances, json_file, indent=4)
        except (FileNotFoundError, PermissionError):
            pass
