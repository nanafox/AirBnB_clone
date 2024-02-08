#!/usr/bin/python3

"""A module that defines the Base Model"""

from datetime import datetime
from typing import Any
from uuid import uuid4
import models


class BaseModel:
    """Defines the Base Model."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes the Base Model."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue

                # ensure the date and time is set correctly
                if key in ["updated_at", "created_at"]:
                    value = datetime.fromisoformat(value)

                self.__dict__[key] = value
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self) -> str:
        """Returns the string representation for an instance of the Base Model.

        Returns:
            str: The string representation for an instance of the Base Model.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Handles the setting of attributes.

        This method updates the `updated_at` attribute whenever a new attribute
        is added to the instance.

        Args:
            __name (str): The name of the attribute.
            __value (Any): The value for the attribute.
        """
        if __name != "update_at":
            self.__dict__["updated_at"] = datetime.now()
            self.__dict__[__name] = __value

    def save(self) -> None:
        """Save the instance and updates the `updated_at`"""
        self.updated_at = datetime.now()

        models.storage.save()

    def to_dict(self) -> dict:
        """Returns the dictionary containing all the key/values of `__dict__`
        of the instance.

        The `updated_at` and `created_at` instance attributes are converted to
        ISO format. A new key named `__class__` is added to the dictionary.

        Returns:
            dict: The dictionary containing all the key/values of `__dict__`
            of the instance.
        """
        # copy the dictionary to avoid changing the original
        obj_dict = dict(self.__dict__)

        obj_dict["__class__"] = self.__class__.__name__

        # update time to ISO format
        obj_dict["updated_at"] = self.updated_at.isoformat()
        obj_dict["created_at"] = self.created_at.isoformat()

        return obj_dict
