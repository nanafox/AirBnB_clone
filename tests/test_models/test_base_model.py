#!/usr/bin/python3

"""Tests the BaseModel class"""

import os
import unittest
import inspect
import datetime
from models import storage
from models.base_model import BaseModel


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
            str(self.base1),
            f"[BaseModel] ({self.base1.id}) {self.base1.__dict__}",
        )

    def test_str_with_extra_attributes(self) -> None:
        """Tests the return value of the `__str__()` method."""
        self.base1.name = "Test Name"
        self.base1.number = 25

        self.assertEqual(
            str(self.base1),
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

    def test_instance_change_updated_at(self) -> None:
        """
        Tests whether the `updated_at` attribute is updated when a change
        occurs to the instance.
        """
        prev_updated_at = self.base1.updated_at
        self.base1.name = "My New Class"

        self.assertNotEqual(prev_updated_at, self.base1.updated_at)

    def test_same_datetime_on_instantiation(self):
        """
        Tests for the same `created_at` and `updated_at` time values when an
        instance is initialized for the first time.
        """
        self.assertEqual(self.base1.created_at, self.base1.updated_at)

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


class TestSaveMethod(unittest.TestCase):
    """Tests the `save` method."""

    __file_path = "file_storage.json"

    def setUp(self) -> None:
        self.base1 = BaseModel()
        self.base2 = BaseModel()

    def test_time_updated_on_save(self) -> None:
        """Tests that the `updated_at` date and time are updated on save."""
        prev_timestamp = self.base2.updated_at

        # perform save operation - updates the 'updated_at' timestamp
        self.base2.save()
        self.assertNotEqual(self.base2.updated_at, prev_timestamp)

    def test_file_created_on_save(self) -> None:
        """Tests to ensure the JSON file is created on save."""
        try:
            # remove the previous files created
            os.remove(self.__file_path)
        except FileNotFoundError:
            pass

        self.base1.save()
        self.assertTrue(os.path.exists(self.__file_path))

    def test_read_saved_file_and_type(self) -> None:
        """Tests the readability and type of the content in the JSON file."""
        with open(self.__file_path, "r", encoding="utf-8") as json_file:
            self.assertEqual(type(json_file.read()), str)

    def test_objects_instance_of(self) -> None:
        """Tests to ensure objects inherit from `BaseModel`."""
        objects = storage.all()

        for obj in objects.values():
            self.assertTrue(isinstance(obj, BaseModel))

            # ensure they are sub classes
            if obj.__class__.__name__ != "BaseModel":
                self.assertTrue(issubclass(obj.__class__, BaseModel))
