#!/usr/bin/python3

"""This module tests the State model."""

import os
import unittest
from models.state import State
from models.base_model import BaseModel
from tests.test_models.test_base_model import JSON_FILE_PATH


class TestStateModel(unittest.TestCase):
    """Tests the State model."""

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
        self.state1 = State()
        self.state2 = State()

    def test_presence_of_class_attributes(self) -> None:
        """Tests the presence of the required class attributes."""
        self.assertTrue(hasattr(self.state1, "name"))

    def test_save(self) -> None:
        """Tests the inherited `save()` method."""
        self.state1.save()

        self.assertTrue(os.path.exists(JSON_FILE_PATH))

    def test_unique_objects(self) -> None:
        """Tests to ensure no two instances are the same."""
        self.assertNotEqual(self.state1, self.state2)

    def test_default_class_attribute_values(self) -> None:
        """Tests the default values for the public class attributes."""
        self.assertTrue(getattr(self.state1, "name") == "")

    def test_instance_of_object(self) -> None:
        """Tests the classes the State model is an instance of."""
        self.assertIsInstance(self.state2, State)
        self.assertIsInstance(self.state2, BaseModel)

    def test_subclass_of(self) -> None:
        """Tests to ensure State model objects are sub classes of BaseModel"""
        self.assertTrue(issubclass(self.state1.__class__, BaseModel))
        self.assertTrue(issubclass(self.state2.__class__, BaseModel))
        self.assertTrue(issubclass(State, BaseModel))

    def test_nonexistent_attribute(self) -> None:
        """Tests for non-existent attribute."""
        self.assertFalse(hasattr(self.state1, "state_id"))

    def test_nonexistent_method(self) -> None:
        """Tests for non-existent method."""
        self.assertFalse(hasattr(self.state1, "get_state()"))
