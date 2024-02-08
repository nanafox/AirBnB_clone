#!/usr/bin/python3

"""This model define the User model."""

from models.base_model import BaseModel


class User(BaseModel):
    """Defines the User model."""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
