#!/usr/bin/python3

"""Implements the command interpreter."""

import cmd
import json
import os
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter."""

    prompt = "(hbnb) "
    doc_header = "hbnb console commands (type help <command>)"
    ruler = "+"
    __file_path = "file_storage.json"
    __models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    @staticmethod
    def do_quit(_) -> bool:
        """Quit command to exit the program."""
        return True

    do_exit = do_quit

    @staticmethod
    def do_eof(_) -> bool:
        """Handles the Ctrl+D signal (EOF)."""
        print()
        return True

    def emptyline(self) -> None:
        pass

    def default(self, line: str) -> None:
        print(f" ** unknown command **: {line.split()[0]}")

    def precmd(self, line):
        if line and line == "EOF":
            return line.lower()

        if (
            line
            and shlex.split(line)[0] in ["help", "?"]
            and len(line.split()) > 1
        ):
            print()

        return line

    def postcmd(self, stop, line) -> None:
        if (
            line
            and shlex.split(line)[0] in ["help", "?"]
            and len(line.split()) > 1
        ):
            print()

        return stop

    def is_valid_args(
        self, line, check_class=False, check_id=False, check_attributes=False
    ) -> None:
        """
        Performs simple checks on the line received from the command line.

        This method checks for the presence of the class and id arguments in
        the `line`. Also, as an extra step, it checks to see if the class
        name in the `line` is known. Alternatively, it can check for the
        presence of attribute name and value arguments in the `line`.

        Args:
            line (str): The string received from the command line.

            check_class (bool, optional): Determines whether to check the
            presence and validity of a class name. Defaults to False.

            check_id (bool, optional): Determines whether to check the presence
            of the `id` argument. Defaults to False.

            check_attributes (bool): Determines whether to check the presence
            of the attribute name and attribute value arguments.
            Defaults to False.

        Returns:
            bool: `True` if the line is okay and contains the required
            arguments needed for the command, `False` otherwise.
        """
        if check_class:
            if not line:
                print("** class name missing **")
                return False

            if shlex.split(line)[0] not in self.__models:
                print("** class doesn't exist **")
                return False

        if check_id:
            if len(shlex.split(line)) == 1:
                print("** instance id missing **")
                return False

        if check_attributes:
            if len(shlex.split(line)) < 3:
                print("** attribute name missing **")
                return False

            if len(shlex.split(line)) < 4:
                print("** value missing **")
                return False

        return True

    @staticmethod
    def search_instance(
        instance_class: str, instance_id: str
    ) -> "object | None":
        """
        Searches for an instance by ID.

        Args:
            instance_class (str): The name of instance's class.
            instance_id (str): The ID of the instance to search for.

        Returns:
            object | None: The instance (object) of the searched `instance_id`
            and `instance_class` if found, otherwise None.
        """
        all_objects = storage.all()

        for obj in all_objects.values():
            if (
                obj.id == instance_id
                and obj.__class__.__name__ == instance_class
            ):
                return obj

        return None

    def do_create(self, line: str) -> None:
        """
        Creates a new instance of a model and saves it to a JSON file.

        Args:
            line (str): The command line argument received.
        """
        if not self.is_valid_args(line, check_class=True):
            return

        obj = self.__models[line]()
        obj.save()
        print(obj.id)

    @staticmethod
    def help_create() -> None:
        """Prints the help info for the `create` command."""
        print(
            "Creates an  instance of a model and saves it to a JSON file."
            "Usage: create <class name>",
            sep="\n",
        )

    def do_show(self, line) -> None:
        """
        Prints the string representation of an instance based on the class
        name and id

        Args:
            line (str): The command line argument received.
        """
        if not self.is_valid_args(line, check_class=True, check_id=True):
            return

        instance_class = instance_id = ""

        try:
            instance_class, instance_id = shlex.split(line)
        except ValueError:
            print("** too many arguments **")
            return

        instance = self.search_instance(instance_class, instance_id)
        if instance:
            print(instance)
        else:
            print("** no instance found **")

    @staticmethod
    def help_show() -> None:
        """Prints the help info for the `show` command."""
        print(
            "Prints the string representation of an instance based on the "
            "class name and id",
            "Usage: show <class name> <id>",
            sep="\n",
        )

    def do_destroy(self, line) -> None:
        """
        Deletes an instance base on the class name and id

        Args:
            line (str): The command line argument received.
        """
        instance_class = instance_id = ""

        if not self.is_valid_args(line, check_class=True, check_id=True):
            return

        try:
            instance_class, instance_id = shlex.split(line)
        except ValueError:
            print("** too many arguments **")
            return

        instance = self.search_instance(instance_class, instance_id)
        if instance:
            objects = storage.all()

            # delete the current instance
            del objects[f"{instance.__class__.__name__}.{instance.id}"]

            # serialize and save the updated objects dictionary
            instances = {}

            for class_id, obj in objects.items():
                instances[class_id] = obj.to_dict()

            with open(self.__file_path, "w", encoding="utf-8") as json_file:
                json.dump(instances, json_file)
        else:
            print("** no instance found **")

    @staticmethod
    def help_destroy() -> None:
        """Prints the help info for the `show` command."""
        print(
            "Deletes an instance base on the class name and id",
            "Usage: destroy <class name> <id>",
            sep="\n",
        )

    def do_all(self, model_name: str) -> None:
        """Prints the string representation for all or some model instances."""
        if model_name and shlex.split(model_name)[0] not in self.__models:
            print("** class doesn't exist")
            return

        objects = storage.all()

        # print the instances for a specific model, if provided
        if model_name:
            for obj in objects.values():
                if obj.__class__.__name__ == model_name:
                    print(obj)
        else:
            # print all the instances available
            for obj in objects.values():
                print(obj)

    @staticmethod
    def help_all() -> None:
        """Prints the help info for the `all` command."""
        print(
            "Prints the string representation for all or a specified model's "
            "instances.",
            "Usage: all [<class name>]",
            sep="\n",
        )

    def do_update(self, arg: str) -> None:
        """
        Updates an instance based on the class name and id by adding or
        updating attributes.

        After a successful update, it is saved.

        Args:
            arg (str): The command line argument.
        """
        if not self.is_valid_args(
            arg, check_class=True, check_id=True, check_attributes=True
        ):
            return

        instance_class, instance_id, attr_name, attr_val = shlex.split(arg)[:4]

        instance = self.search_instance(instance_class, instance_id)

        if instance:
            instance.__dict__[attr_name] = attr_val
            instance.save()
        else:
            print(" ** no instance found **")

    @staticmethod
    def help_update() -> None:
        """Prints the help info for the `update` command."""
        print(
            "Updates an instance based on the class name and id by adding or "
            "updating attributes.",
            'update <class name> <id> <attribute name> "<attribute value>"',
            sep="\n",
        )

    @staticmethod
    def do_clear(_) -> None:
        """Clears the console screen."""
        os.system("clear")

    @staticmethod
    def do_shell(line) -> None:
        """Invokes the builtin shell program to execute a command."""
        if line:
            os.system(line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
