#!/usr/bin/python3


"""Tests the FileStorage model."""


import os
import unittest
import inspect
import models
from models.city import City
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestDocumentation(unittest.TestCase):
    """Tests the documentation for modules, classes and methods."""

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


class TestFileStorage(unittest.TestCase):
    """Tests the FileStorage model."""

    __file_path = "file_storage.json"

    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.remove(cls.__file_path)
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            os.remove(cls.__file_path)
        except FileNotFoundError:
            pass

    def setUp(self) -> None:
        self.base = BaseModel()
        self.city = City()

    def test_create_save_object(self) -> None:
        """Tests that the instances are saved on instantiation."""
        models.storage.save()
        self.assertTrue(os.path.exists(self.__file_path))

    def test_all_method_return_type(self) -> None:
        """Tests the return type of the `all()` method."""
        objects = models.storage.all()

        self.assertTrue(isinstance(objects, dict))
