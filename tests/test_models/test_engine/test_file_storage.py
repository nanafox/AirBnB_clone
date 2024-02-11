#!/usr/bin/python3


"""Tests the FileStorage engine."""


import os
import json
import inspect
import unittest
from models import storage
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from tests.test_models.test_base_model import JSON_FILE_PATH


class TestFileStorageDocumentation(unittest.TestCase):
    """Tests the documentation for modules, classes and methods for
    FileStorage."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class method for the doc tests."""
        cls.methods = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_module_docstring_exists(self) -> None:
        """Tests if module docstring documentation exists."""
        self.assertIsNotNone(FileStorage.__doc__)

    def test_classes_docstring_exists(self) -> None:
        """Tests if class docstring documentation exists."""
        self.assertIsNotNone(FileStorage.__doc__.__class__)

    def test_methods_docstring_exists(self) -> None:
        """Tests if methods docstring documentation exists."""
        for _, method in self.methods:
            self.assertIsNotNone(method.__doc__)


class TestFileStorageAllMethod(unittest.TestCase):
    """Tests the `all()` method of the FileStorage engine."""

    def setUp(self) -> None:
        # remove all objects from the dictionary
        storage.all().clear()

        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def tearDown(self) -> None:
        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def test_all_method_return_type(self) -> None:
        """Tests the return type of the `all()` method."""
        self.assertTrue(isinstance(storage.all(), dict))

    def test_key_name_in_objects_dict_one_object(self) -> None:
        """Tests to ensure key names are correct for a single object."""
        base1 = BaseModel()

        objects = storage.all()

        expected_key = f"{base1.__class__.__name__}.{base1.id}"
        self.assertDictEqual({expected_key: base1}, objects)

    def test_key_name_in_objects_dict_same_two_objects(self) -> None:
        """Ensure key names are correct for two objects of the same class."""
        base1 = BaseModel()
        base2 = BaseModel()

        expected_key_1 = f"{base1.__class__.__name__}.{base1.id}"
        expected_key_2 = f"{base2.__class__.__name__}.{base2.id}"

        self.assertDictEqual(
            {expected_key_1: base1, expected_key_2: base2}, storage.all()
        )

    def test_key_name_in_objects_dict_diff_two_objects(self) -> None:
        """Ensure key names are correct for two objects of different classes"""
        base = BaseModel()
        city = City()

        expected_key_1 = f"{base.__class__.__name__}.{base.id}"
        expected_key_2 = f"{city.__class__.__name__}.{city.id}"

        self.assertDictEqual(
            {expected_key_1: base, expected_key_2: city}, storage.all()
        )


class TestFileStorageNewMethod(unittest.TestCase):
    """Tests the `new()` method of the FileStorage engine."""

    def test_invalid_new_list_object(self) -> None:
        """Tests invalid objects passed to the `new()` method"""
        new_data = [1, 23, 4]

        with self.assertRaisesRegex(AttributeError, "no attribute 'id'"):
            storage.new(new_data)

    def test_new_base_model(self) -> None:
        """Tests the `new()` method with a single BaseModel instance object."""
        base = BaseModel()

        # remove all objects from the dictionary
        storage.all().clear()

        # capture this new instance
        storage.new(base)

        # check to ensure it made it to the dictionary and it's the only object
        self.assertDictEqual(
            {f"{base.__class__.__name__}.{base.id}": base}, storage.all()
        )

    def test_many_args_passed_to_new(self) -> None:
        """Tests passing too many arguments to the `new()` method."""
        with self.assertRaises(TypeError):
            storage.new(BaseModel(), City())


class TestFileStorageSaveMethod(unittest.TestCase):
    """Tests the `save()` method of the FileStorage engine."""

    def setUp(self) -> None:
        # remove all objects from the dictionary
        storage.all().clear()

        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def tearDown(self) -> None:
        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def test_save_object_on_empty_objects(self) -> None:
        """Tests the `save()` on an empty objects dictionary."""
        self.assertEqual(storage.all(), {})
        storage.save()
        self.assertTrue(os.path.exists(JSON_FILE_PATH))

        with open(JSON_FILE_PATH, "r", encoding="utf-8") as json_file:
            self.assertEqual(json_file.read(), "{}")

    def test_no_object_no_file(self) -> None:
        """Tests to ensure that JSON file does not exist before a save."""
        self.assertFalse(os.path.exists(JSON_FILE_PATH))

    def test_save_invalid_dict_object(self) -> None:
        """Tests the `save()` method on a dictionary with invalid objects."""
        objects = storage.all()

        # update the objects dictionary with some bad data
        objects.update({"first_name": "John", "last_name": "Doe"})

        with self.assertRaises(AttributeError):
            storage.save()

    def test_save_dict_key_error(self) -> None:
        """Tests for invalid keys in the dictionary while saving objects."""
        objects = storage.all()

        objects.clear()
        objects.update({"BaseModel": BaseModel()})

        with self.assertRaisesRegex(KeyError, "key must be <class name>.<id>"):
            storage.save()


class TestFileStorageReloadMethod(unittest.TestCase):
    """Tests the `reload()` method of the FileStorage engine."""

    def setUp(self) -> None:
        # remove all objects from the dictionary
        storage.all().clear()

        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def tearDown(self) -> None:
        try:
            os.remove(JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def test_save_and_reload_valid_objects(self) -> None:
        """Tests saving and reloading valid objects of different models."""
        for _ in range(10):
            BaseModel()
            City()
            User()
            Review()
            State()
            Place()
            Amenity()

        num_of_objects = len(storage.all())
        storage.save()

        self.assertNotEqual(storage.all(), {})
        self.assertTrue(os.path.exists(JSON_FILE_PATH))

        # clear the original objects dictionary
        storage.all().clear()
        self.assertEqual(storage.all(), {})

        # deserialize JSON file and load objects into the dictionary
        storage.reload()

        # check that the dictionary is not empty after the reload
        self.assertNotEqual(storage.all(), {})

        # ensure the number of objects match the number created initially
        self.assertEqual(len(storage.all()), num_of_objects)

    def test_arg_passed_to_reload(self) -> None:
        """Tests when an argument is passed to the `reload()` method."""
        with self.assertRaises(TypeError):
            storage.reload(BaseModel)

    def test_invalid_json_file_reload(self) -> None:
        """Tests a reload on an invalid JSON file format"""
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as json_file:
            json.dump({"BaseModel": [1, 2, 4]}, json_file)

        with self.assertRaises(TypeError):
            storage.reload()
