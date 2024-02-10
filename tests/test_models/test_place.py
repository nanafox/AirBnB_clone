#!/usr/bin/python3

"""This module tests the Place model."""

import os
import unittest
from models.place import Place
from models.base_model import BaseModel
from tests.test_models.test_base_model import JSON_FILE_PATH


class TestPlaceModel(unittest.TestCase):
    """Tests the Place model."""

    __expected_attributes = {
        "city_id": "",
        "user_id": "",
        "name": "",
        "description": "",
        "number_rooms": 0,
        "number_bathrooms": 0,
        "max_guest": 0,
        "price_by_night": 0,
        "latitude": 0.0,
        "longitude": 0.0,
        "amenity_ids": [],
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
        self.place1 = Place()
        self.place2 = Place()

    def test_presence_of_class_attributes(self) -> None:
        """Tests the presence of the required class attributes."""
        for attribute in self.__expected_attributes:
            self.assertTrue(hasattr(self.place1, attribute))

    def test_save(self) -> None:
        """Tests the inherited `save()` method."""
        Place().save()

        self.assertTrue(os.path.exists(JSON_FILE_PATH))

    def test_unique_objects(self) -> None:
        """Tests to ensure no two instances are the same."""
        self.assertNotEqual(self.place1, self.place2)

    def test_default_class_attribute_values(self) -> None:
        """Tests the default values for the public class attributes."""
        for attribute, value in self.__expected_attributes.items():
            self.assertTrue(getattr(self.place1, attribute) == value)
            self.assertTrue(getattr(self.place2, attribute) == value)

    def test_default_class_attribute_values_type(self) -> None:
        """Tests the default values' type for the public class attributes."""
        for attribute, value in self.__expected_attributes.items():
            self.assertTrue(
                type(getattr(self.place1, attribute)) is type(value)
            )
            self.assertTrue(
                type(getattr(self.place2, attribute)) is type(value)
            )

    def test_instance_of_object(self) -> None:
        """Tests the classes the Place model is an instance of."""
        self.assertIsInstance(self.place2, Place)
        self.assertIsInstance(self.place2, BaseModel)

    def test_subclass_of(self) -> None:
        """Tests to ensure Place model objects are sub classes of BaseModel"""
        self.assertTrue(issubclass(self.place1.__class__, BaseModel))
        self.assertTrue(issubclass(self.place2.__class__, BaseModel))
        self.assertTrue(issubclass(Place, BaseModel))

    def test_nonexistent_attribute(self) -> None:
        """Tests for non-existent attribute."""
        self.assertFalse(hasattr(self.place1, "no_attribute"))

    def test_nonexistent_method(self) -> None:
        """Tests for non-existent method."""
        self.assertFalse(hasattr(self.place1, "get_place()"))
