#!/usr/bin/python3

"""This module tests the console program `HBNBCommand`."""


import os
import inspect
from io import StringIO
from uuid import UUID as uuid
from unittest import TestCase
from unittest.mock import patch
from console import HBNBCommand as hbnb
from tests.test_models.test_base_model import JSON_FILE_PATH
import models
from lazy_methods import LazyMethods

instance = LazyMethods()


known_models = [
    "User",
    "BaseModel",
    "Amenity",
    "Place",
    "City",
    "Review",
    "State",
]


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
            "Documented commands (type help <topic>):\n"
            "========================================\n"
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
            "\tOption 2: <class name>.create()\n"
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


class TestCreateCommand(TestCase):
    """Tests the `create` command on the all known models."""

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
        models.storage.all().clear()

    ##########################################################
    # The following test cases tests the `create` command.   #
    # It uses general syntax: create <class name>.           #
    # It will also test for edge cases and potential errors  #
    # while using the create command on the all known Models #
    ##########################################################

    def test_general_cmd_create_instance_valid(self) -> None:
        """Tests the creation of a valid model instance."""
        for model in known_models:
            models.storage.all().clear()

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"create {model}")

            # grab the string ID and convert it to a valid UUID for checking
            instance_id = instance.get_uuid(result)

            # ensure the id is valid
            self.assertTrue(isinstance(instance_id, uuid))

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"count {model}")

            num_of_instances = instance.get_instances_count(result)

            # the number of instance must be 1 at this point
            self.assertEqual(num_of_instances, 1)

    def test_general_cmd_create_instance_no_class(self) -> None:
        """Tests the creation of an instance without the model name."""
        with patch("sys.stdout", new=StringIO()) as error:
            hbnb().onecmd("create")

        self.assertEqual(error.getvalue().strip(), "** class name missing **")

    def test_general_cmd_create_instance_invalid_class(self) -> None:
        """Tests the creation of an instance with a wrong model name"""
        with patch("sys.stdout", new=StringIO()) as error:
            hbnb().onecmd("create MyModel")

        self.assertEqual(error.getvalue().strip(), "** class doesn't exist **")

    def test_general_cmd_create_instance_lowercase_class(self) -> None:
        """Tests the creation of a instance with class name in lowercase."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as error:
                hbnb().onecmd(f"create {model.lower()}")

            self.assertEqual(
                error.getvalue().strip(), "** class doesn't exist **"
            )

    def test_general_cmd_create_multi_and_file(self) -> None:
        """Tests the creation of multiple instances and save operation."""
        for model in known_models:
            models.storage.all().clear()

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"create {model}")

            # grab the string ID and convert it to a valid UUID for checking
            instance_id_1 = instance.get_uuid(result)

            # ensure the id is valid for the first instance
            self.assertTrue(isinstance(instance_id_1, uuid))

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"create {model}")

            # grab the string ID and convert it to a valid UUID for checking
            instance_id_2 = instance.get_uuid(result)

            # ensure the id is valid for second instance
            self.assertTrue(isinstance(instance_id_2, uuid))

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"count {model}")

            num_of_instances = int(result.getvalue().strip())

            # the number of instance must be 2 at this point
            self.assertEqual(num_of_instances, 2)

            # ensure objects dictionary is not empty after instance creation
            self.assertNotEqual(models.storage.all(), {})

            # ensure the JSON file was created
            self.assertTrue(os.path.exists(JSON_FILE_PATH))

    ##########################################################
    # The following test cases tests the `create` command.   #
    # It uses model-based syntax: <class name>.<command>().  #
    # It will also test for edge cases and potential errors  #
    # while using the create command on the all known Models #
    ##########################################################

    def test_model_based_cmd_create_instance_valid(self) -> None:
        """Tests the creation of a valid instance."""
        for model in known_models:
            models.storage.all().clear()

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"{model}.create()")

            # grab the string ID and convert it to a valid UUID for checking
            instance_id = result.getvalue().strip()
            instance_id = uuid(instance_id)

            # ensure the id is valid
            self.assertTrue(isinstance(instance_id, uuid))

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"{model}.count()")

            num_of_instances = int(result.getvalue().strip())

            # the number of instance must be 1 at this point
            self.assertEqual(num_of_instances, 1)

    def test_model_based_cmd_create_instance_incomplete(self) -> None:
        """Tests the creation of a instance with an incomplete command."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as error:
                hbnb().onecmd(f"{model}")

            self.assertEqual(
                error.getvalue().strip(), f"*** Unknown syntax: {model}"
            )

    def test_model_based_cmd_create_instance_incomplete_2(self) -> None:
        """Tests the creation of a instance with an incomplete command."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as error:
                hbnb().onecmd(f"{model}.")

            self.assertEqual(
                error.getvalue().strip(), f"*** Unknown syntax: {model}."
            )

    def test_model_based_cmd_create_instance_incomplete_3(self) -> None:
        """Tests the creation of a instance with an incomplete command."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as error:
                hbnb().onecmd(f"{model}.create")

            self.assertEqual(
                error.getvalue().strip(), f"*** Unknown syntax: {model}.create"
            )

    def test_model_based_cmd_create_instance_incomplete_4(self) -> None:
        """Tests the creation of a instance with an incomplete command."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"{model}.create(")

            self.assertEqual(
                result.getvalue().strip(),
                f"*** Unknown syntax: {model}.create(",
            )

    def test_model_based_cmd_create_instance_invalid_class(self) -> None:
        """Tests the creation of a instance with a wrong class name"""
        with patch("sys.stdout", new=StringIO()) as error:
            hbnb().onecmd("MyModel.create()")

        self.assertEqual(error.getvalue().strip(), "** class doesn't exist **")

    def test_model_based_cmd_create_instance_lowercase_class(self) -> None:
        """Tests the creation of a instance with class name in lowercase."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as error:
                hbnb().onecmd(f"{model.lower()}.create()")

            self.assertEqual(
                error.getvalue().strip(), "** class doesn't exist **"
            )

    def test_model_based_cmd_create_multi_and_file(self) -> None:
        """Tests the creation of multiple User instances and save operation."""
        for model in known_models:
            models.storage.all().clear()

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"{model}.create()")

            # grab the string ID and convert it to a valid UUID for checking
            instance_id_1 = instance.get_uuid(result)

            # ensure the id is valid for the first instance
            self.assertTrue(isinstance(instance_id_1, uuid))

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"{model}.create()")

            # grab the string ID and convert it to a valid UUID for checking
            instance_id_2 = instance.get_uuid(result)

            # ensure the id is valid for second instance
            self.assertTrue(isinstance(instance_id_2, uuid))

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"{model}.count()")

            num_of_instances = int(result.getvalue().strip())

            # the number of instance must be 2 at this point
            self.assertEqual(num_of_instances, 2)

            # ensure objects dictionary is not empty after instance creation
            self.assertNotEqual(models.storage.all(), {})

            # ensure the JSON file was created
            self.assertTrue(os.path.exists(JSON_FILE_PATH))


class TestShowCommand(TestCase):
    """Tests the `show` command on all models."""


class TestUpdateCommand(TestCase):
    """Tests the `update` command on all models."""

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
        models.storage.all().clear()

    ##########################################################
    # The following test cases tests the `update` command.   #
    # It uses general syntax: update <class name> <id>       #
    # It will also test for edge cases and potential errors  #
    # while using the create command on the all known Models #
    ##########################################################

    def test_create_update_one_attribute(self) -> None:
        """Creates an instance of each model, updates it with one attribute,
        then checks that it happened."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"create {model}")

            instance_id = instance.get_uuid(result)
            instance_key = instance.get_key(model, instance_id)
            attr_name, attr_value = instance.get_random_attribute()

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(
                    f"update {model} {instance_id} {attr_name} {attr_value}"
                )

            # the `update` command prints nothing on success, confirm that
            self.assertEqual(result.getvalue().strip(), "")

            # now let's confirm that the instance really got updated
            self.assertIn(
                attr_name, models.storage.all()[instance_key].to_dict()
            )

    def test_update_no_class_arg(self) -> None:
        """Tests the `update` command without passing a class name."""
        for _ in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd("update")

            self.assertEqual(
                result.getvalue().strip(), "** class name missing **"
            )

    def test_update_invalid_class_name(self) -> None:
        """Tests the `update` command with a wrong class name."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"update {model.upper()}")

            self.assertEqual(
                result.getvalue().strip(), "** class doesn't exist **"
            )

    def test_update_no_instance_id(self) -> None:
        """Tests the `update` command with a no instance ID."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"update {model}")

            self.assertEqual(
                result.getvalue().strip(), "** instance id missing **"
            )

    def test_update_no_attribute_name(self) -> None:
        """Tests the `update` command with a no attribute name."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"update {model} 1234-1234-1234")

            self.assertEqual(
                result.getvalue().strip(), "** attribute name missing **"
            )

    def test_update_no_attribute_value(self) -> None:
        """Tests the `update` command with a no attribute value."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"update {model} 1234-1234-1234 first_name")

            self.assertEqual(result.getvalue().strip(), "** value missing **")

    def test_update_no_instance_found(self) -> None:
        """Tests the `update` command when an instance is not found."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(
                    f"update {model} 1234-1234-1234 first_name 'John'"
                )

            self.assertEqual(
                result.getvalue().strip(), "** no instance found **"
            )

    def test_create_update_one_attribute_ignore_extra(self) -> None:
        """Creates an instance of each model, updates it with one attribute,
        then checks that it happened. Also it checks to ensure extra args are
        ignored."""
        for model in known_models:
            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(f"create {model}")

            instance_id = instance.get_uuid(result)
            instance_key = instance.get_key(model, instance_id)
            attr_name_1, attr_value_1 = instance.get_random_attribute()
            attr_name_2, attr_value_2 = "email", instance.get_email()

            with patch("sys.stdout", new=StringIO()) as result:
                hbnb().onecmd(
                    f"update {model} {instance_id} "
                    f"{attr_name_1} {attr_value_1} "
                    f"{attr_name_2} {attr_value_2}"
                )

            # the `update` command prints nothing on success, confirm that
            self.assertEqual(result.getvalue().strip(), "")

            # now let's confirm that the instance really got updated only
            # the `attr_name_1` and `attr_value_1` only
            self.assertIn(
                attr_name_1, models.storage.all()[instance_key].to_dict()
            )

            # confirm the value is really `attr_value_1`
            self.assertEqual(
                models.storage.all()[instance_key].to_dict()[attr_name_1],
                attr_value_1,
            )

            # now let's confirm that the instance the extra args
            # i.e., `attr_name_2` and `attr_value_2` were ignored
            self.assertNotIn(
                attr_name_2, models.storage.all()[instance_key].to_dict()
            )


class TestAllCommand(TestCase):
    """Tests the `all` command on all models."""


class TestDestroyCommand(TestCase):
    """Tests the `destroy` command on all models."""


class TestCountCommand(TestCase):
    """Tests the `count` command on all models."""
