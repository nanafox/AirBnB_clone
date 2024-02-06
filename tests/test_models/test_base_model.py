#!/usr/bin/python3

"""Tests the BaseModel class"""

import unittest
import inspect
from models.base_model import BaseModel
import datetime


class TestDocumentation(unittest.TestCase):
    """Tests the documentation for modules, classes and methods."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class method for the doc tests."""
        cls.methods = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_module_docstring_exists(self) -> None:
        """Tests if module docstring documentation exists."""
        self.assertIsNotNone(BaseModel.__doc__)

    def test_classes_docstring_exists(self) -> None:
        """Tests if class docstring documentation exists."""
        self.assertIsNotNone(BaseModel.__doc__.__class__)

    def test_methods_docstring_exists(self) -> None:
        """Tests if methods docstring documentation exists."""
        for _, method in self.methods:
            self.assertIsNotNone(method.__doc__)


class TestBaseModel(unittest.TestCase):
    """Tests the Base Model class."""

    def setUp(self) -> None:
        self.base1 = BaseModel()
        self.base2 = BaseModel()

    def test_updated_at_type(self) -> None:
        """Tests the data type for the `updated_at` attribute."""
        self.assertEqual(type(self.base1.created_at), datetime.datetime)

    def test_created_at_type(self) -> None:
        """Tests the data type for the `created_at` attribute."""
        self.assertEqual(type(self.base1.created_at), datetime.datetime)

    def test_str(self) -> None:
        """Tests the return value of the `__str__()` method."""
        self.assertEqual(
            self.base1.__str__(),
            f"[BaseModel] ({self.base1.id}) {self.base1.__dict__}",
        )

    def test_str_with_extra_attributes(self) -> None:
        """Tests the return value of the `__str__()` method."""
        self.base1.name = "Test Name"
        self.base1.number = 25

        self.assertEqual(
            self.base1.__str__(),
            f"[BaseModel] ({self.base1.id}) {self.base1.__dict__}",
        )

    def test_unique_id(self) -> None:
        """Tests to ensure no two objects have the same UUID."""
        self.assertNotEqual(self.base1.id, self.base2.id)

    def test_unique_objects(self) -> None:
        """Tests to ensure no two objects have the same ID (Address)."""
        self.assertNotEqual(id(self.base1.id), id(self.base2.id))

    def test_type_id_str(self) -> None:
        """Tests to ensure the ID field is a string."""
        self.assertEqual(type(self.base1.id), str)

    def test_save(self) -> None:
        """Tests the `save()` method."""
        prev_timestamp = self.base2.updated_at

        # perform save operation - updates the 'updated_at' timestamp
        self.base2.save()
        self.assertNotEqual(self.base2.updated_at, prev_timestamp)

    def test_iso_format(self) -> None:
        """Tests the ISO format after `to_dict()` is called."""
        expected_iso_format_1 = self.base2.updated_at.isoformat()
        expected_iso_format_2 = self.base2.created_at.isoformat()

        # generate the dictionary
        base2_dict = self.base2.to_dict()

        self.assertEqual(base2_dict["updated_at"], expected_iso_format_1)
        self.assertEqual(base2_dict["created_at"], expected_iso_format_2)

    def test_class_name_in_to_dict(self) -> None:
        """Tests if the class name was added to the dictionary returned."""
        base1_dict = self.base1.to_dict()

        # confirm the key `__class__` is present
        self.assertIn("__class__", base1_dict)

        # confirm the value is as expected
        self.assertIn("BaseModel", base1_dict.values())

    def test_to_dict_return_type(self) -> None:
        """Ensures the return value of the `to_dict()` is a dictionary."""
        self.assertEqual(type(self.base1.to_dict()), dict)
        self.assertEqual(type(self.base2.to_dict()), dict)

    def test_instantiation_from_dict(self) -> None:
        """Tests object instantiation from a dictionary."""
        new_base = BaseModel(**self.base1.to_dict())

        self.assertEqual(type(new_base).__name__, BaseModel.__name__)

    def test_invalid_iso_format_from_dict(self) -> None:
        """Handle invalid dates passed when instantiating with a dictionary."""
        base2_dict = self.base2.to_dict()

        with self.assertRaisesRegex(ValueError, "Invalid isoformat string"):
            # screw up the date
            base2_dict["updated_at"] = "Hello world"

            BaseModel(**base2_dict)

    def test_same_id_from_dict(self) -> None:
        """Tests for the same UUID when instantiated from a dictionary."""
        new_base = BaseModel(**self.base2.to_dict())

        self.assertEqual(new_base.id, self.base2.id)

    def test_same_creation_datetime_from_dict(self) -> None:
        """
        Tests for the same creation dates when instantiated from
        a dictionary.
        """
        new_base = BaseModel(**self.base1.to_dict())

        self.assertEqual(self.base1.created_at, new_base.created_at)

    def test_same_updated_datetime_from_dict(self) -> None:
        """
        Tests for the same `updated_at` dates when instantiated from
        a dictionary.
        """
        new_base = BaseModel(**self.base1.to_dict())

        self.assertEqual(new_base.updated_at, self.base1.updated_at)

    def test_updated_at_type_from_dict(self) -> None:
        """
        Tests the data type of the `updated_at` instance attribute
        after instantiating from a dictionary.
        """
        new_base = BaseModel(**self.base1.to_dict())

        self.assertEqual(type(new_base.updated_at), datetime.datetime)

    def test_created_at_type_from_dict(self) -> None:
        """
        Tests the data type of the `created_at` instance attribute
        after instantiating from a dictionary.
        """
        new_base = BaseModel(**self.base1.to_dict())

        self.assertEqual(type(new_base.created_at), datetime.datetime)
