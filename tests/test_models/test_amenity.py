#!/usr/bin/python3

"""This module tests the Amenity model."""

import os
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from tests.test_models.test_base_model import JSON_FILE_PATH


class TestAmenityModel(unittest.TestCase):
    """Tests the Amenity model."""

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
        self.amenity1 = Amenity()
        self.amenity2 = Amenity()

    def test_presence_of_class_attributes(self) -> None:
        """Tests the presence of the required class attributes."""
        self.assertTrue(hasattr(self.amenity1, "name"))

    def test_save(self) -> None:
        """Tests the inherited `save()` method."""
        self.amenity1.save()

        self.assertTrue(os.path.exists(JSON_FILE_PATH))

    def test_unique_objects(self) -> None:
        """Tests to ensure no two instances are the same."""
        self.assertIsNot(self.amenity1, self.amenity2)

    def test_default_class_attribute_values(self) -> None:
        """Tests the default values for the public class attributes."""
        self.assertTrue(getattr(self.amenity1, "name") == "")

    def test_instance_of_object(self) -> None:
        """Tests the classes the Amenity model is an instance of."""
        self.assertIsInstance(self.amenity2, Amenity)
        self.assertIsInstance(self.amenity2, BaseModel)

    def test_subclass_of(self) -> None:
        """Tests to ensure Amenity model objects are subclasses of BaseModel"""
        self.assertTrue(issubclass(self.amenity1.__class__, BaseModel))
        self.assertTrue(issubclass(self.amenity2.__class__, BaseModel))
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_nonexistent_attribute(self) -> None:
        """Tests for non-existent attribute."""
        self.assertFalse(hasattr(self.amenity1, "amenity_id"))

    def test_nonexistent_method(self) -> None:
        """Tests for non-existent method."""
        self.assertFalse(hasattr(self.amenity1, "get_amenity()"))
