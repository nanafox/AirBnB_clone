#!/usr/bin/python3

"""This module tests the User model."""

import os
import unittest
from models.user import User
from models.base_model import BaseModel
from tests.test_models.test_base_model import JSON_FILE_PATH


class TestUserModel(unittest.TestCase):
    """Tests the User model."""

    __expected_attributes = {
        "email": "",
        "password": "",
        "first_name": "",
        "last_name": "",
    }

    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def setUp(self) -> None:
        self.user1 = User()
        self.user2 = User()

    def test_presence_of_class_attributes(self) -> None:
        """Tests the presence of the required class attributes."""
        for attribute in self.__expected_attributes:
            self.assertTrue(hasattr(self.user1, attribute))

    def test_save(self) -> None:
        """Tests the inherited `save()` method."""
        User().save()

        self.assertTrue(os.path.exists(JSON_FILE_PATH))

    def test_unique_objects(self) -> None:
        """Tests to ensure no two instances are the same."""
        self.assertNotEqual(self.user1, self.user2)

    def test_default_class_attribute_values(self) -> None:
        """Tests the default values for the public class attributes."""
        for attribute, value in self.__expected_attributes.items():
            self.assertTrue(getattr(self.user1, attribute) == value)
            self.assertTrue(getattr(self.user2, attribute) == value)

    def test_instance_of_object(self) -> None:
        """Tests the classes the User model is an instance of."""
        self.assertIsInstance(self.user2, User)
        self.assertIsInstance(self.user2, BaseModel)

    def test_subclass_of(self) -> None:
        """Tests to ensure User model objects are sub classes of BaseModel"""
        self.assertTrue(issubclass(self.user1.__class__, BaseModel))
        self.assertTrue(issubclass(self.user2.__class__, BaseModel))
        self.assertTrue(issubclass(User, BaseModel))

    def test_nonexistent_attribute(self) -> None:
        """Tests for non-existent attribute."""
        self.assertFalse(hasattr(self.user1, "user_id"))

    def test_nonexistent_method(self) -> None:
        """Tests for non-existent method."""
        self.assertFalse(hasattr(self.user2, "get_user_id()"))
