#!/usr/bin/python3

"""This module tests the console program `HBNBCommand`."""


import inspect
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from console import HBNBCommand as hbnb


class TestHBNBCommandDocumentation(TestCase):
    """Tests the documentation for modules, classes and methods for
    hbnb and anything else that inherits from it."""

    __known_methods = [
        "do_all",
        "help_all",
        "do_create",
        "help_create",
        "do_count",
        "help_count",
        "do_destroy",
        "help_destroy",
        "do_update",
        "help_update",
        "do_eof",
        "do_show",
        "help_show",
        "do_shell",
        "do_clear",
        "do_quit",
        "__is_valid_args",
        "__is_valid_args_helper",
        "__search_instance",
        "__handle_model_based_cmd",
    ]

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class method for the doc tests."""
        cls.methods = inspect.getmembers(hbnb, inspect.isfunction)

    def test_module_docstring_exists(self) -> None:
        """Tests if module docstring documentation exists."""
        self.assertIsNotNone(hbnb.__doc__)

    def test_classes_docstring_exists(self) -> None:
        """Tests if class docstring documentation exists."""
        self.assertIsNotNone(hbnb.__doc__.__class__)

    def test_methods_docstring_exists(self) -> None:
        """Tests if methods docstring documentation exists."""
        for _, method in self.methods:
            if method.__name__ in self.__known_methods:
                self.assertIsNotNone(method.__doc__)


class TestHelpCommand(TestCase):
    """Tests the `help` command of the console program."""

    __expected_output = ""

    def test_no_help(self) -> None:
        """Tests the behaviour when a help for a command does not exist."""
        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help console")

        self.assertEqual(result.getvalue(), "*** No help on console\n")

    def test_help_no_args(self) -> None:
        """Tests the `help` command with no args"""
        self.__expected_output = (
            "\n"
            "hbnb console commands (type help <command>)\n"
            "+++++++++++++++++++++++++++++++++++++++++++\n"
            "all  clear  count  create  destroy  eof  "
            "help  quit  shell  show  update\n"
            "\n"
        )
        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help")

        self.assertEqual(result.getvalue(), self.__expected_output)

        # let's do one more check with "?"
        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("?")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_all(self) -> None:
        """Tests the output of the `all` command's help message."""
        self.__expected_output = (
            "Prints the string representation for all or a specified model's "
            "instances.\n"
            "Usage:\n"
            "\tOption 1: all [<class name>]\n"
            "\tOption 2: <class name>.all()\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help all")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_clear(self) -> None:
        """Tests the output of the `clear` command's help message."""
        self.__expected_output = "Clears the console screen.\n"

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help clear")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_count(self) -> None:
        """Tests the output of the `count` command's help message."""
        self.__expected_output = (
            "Prints the number of instances for a particular model.\n"
            "Usage:\n"
            "\tOption 1: count <class name>\n"
            "\tOption 2: <class name>.count()\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help count")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_create(self) -> None:
        """Tests the output of the `create` command's help message."""
        self.__expected_output = (
            "Creates an  instance of a model and saves it to a JSON file.\n"
            "Usage:\n"
            "\tOption 1: create <class name>\n"
            "\tOption 2: <class name>.create(<id>)\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help create")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_destroy(self) -> None:
        """Tests the output of the `destroy` command's help message."""
        self.__expected_output = (
            "Deletes an instance based on the class name and id\n"
            "Usage:\n"
            "\tOption 1: destroy <class name> <id>\n"
            "\tOption 2: <class name>.destroy(<id>)\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help destroy")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_eof(self) -> None:
        """Tests the output of the `EOF` command's help message."""
        self.__expected_output = "Exits the console gracefully.\n"

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help eof")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_help(self) -> None:
        """Tests the output of the `help` command's help message."""
        self.__expected_output = (
            'List available commands with "help" '
            'or detailed help with "help cmd".\n'
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help help")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_quit(self) -> None:
        """Tests the output of the `quit` command's help message."""
        self.__expected_output = "Quit command to exit the console.\n"

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help quit")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_shell(self) -> None:
        """Tests the output of the `shell` command's help message."""
        self.__expected_output = (
            "Invokes the builtin shell program to execute a command.\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help shell")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_show(self) -> None:
        """Tests the output of the `show` command's help message."""
        self.__expected_output = (
            "Prints the string representation of an instance based on the "
            "class name and id\n"
            "Usage:\n"
            "\tOption 1: show <class name> <id>\n"
            "\tOption 2: <class name>.show(<id>)\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help show")

        self.assertEqual(result.getvalue(), self.__expected_output)

    def test_help_on_update(self) -> None:
        """Tests the output of the `update` command's help message."""
        self.__expected_output = (
            "Updates an instance based on the class name and id by adding or "
            "updating attributes.\n"
            "Usage:\n"
            "\tOption 1: "
            'update <class name> <id> <attribute name> "<attribute value>"\n'
            "\tOption 2: "
            "<class name>.update(<id>, <attribute name>, <attribute value>)\n"
            "\tOption 3: "
            "<class name>.update(<id>, <dictionary representation>)\n"
        )

        with patch("sys.stdout", new=StringIO()) as result:
            hbnb().onecmd("help update")

        self.assertEqual(result.getvalue(), self.__expected_output)
