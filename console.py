#!/usr/bin/python3

"""Implements the command interpreter."""

import re
import os
import cmd
import shlex
from ast import literal_eval
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter."""

    prompt = "(hbnb) "
    __models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def emptyline(self) -> None:
        """Ensures empty command lines are handled properly."""

    def default(self, line: str) -> None:
        """Handles unknown commands and model-based commands.

        It looks out for the model-based command syntaxes (e.g. User.all()),
        then calls the appropriate method to handle it.

        If the command `line` does not match a model-based syntax, then it is
        ruled out an unknown command.

        Args:
            line (str): The command line received.
        """
        if re.match(r"(\w+)\.(\w+)\((.*)\)", line):
            line = self.__handle_model_based_cmd(line)
            self.onecmd(line.strip())
        else:
            print(f"*** Unknown syntax: {line.strip()}")

    def __handle_model_based_cmd(self, line: str) -> str:
        """Handles the model-based command syntax.

        Args:
            line (str): The command line received.

        Returns:
            str: The updated line for further processing.
        """
        get_regex = list(re.match(r"(\w+)\.(\w+)\((.*)\)", line).groups())

        # get rid of empty lines in the returned pattern
        if get_regex[-1] == "":
            get_regex.pop()

        if get_regex:
            if len(get_regex) >= 2:
                class_name, user_cmd = get_regex[0], get_regex[1]
                line = f"{user_cmd} {class_name}"

                try:
                    obj_dict = re.findall(r"\{.*?\}", get_regex[2])[0]

                    if user_cmd == "update" and obj_dict:

                        obj_dict = literal_eval(obj_dict)
                        instance_id = shlex.split(get_regex[2])[0]
                        instance_id = instance_id.replace(",", "")

                        line += f" {instance_id} {obj_dict}"
                        return line
                except IndexError:
                    pass

                # try and preserve a list if it exists
                if len(get_regex) >= 3:
                    list_data = re.findall(r"\[.*\]", get_regex[2])
                    if list_data:
                        get_regex[2] = get_regex[2].replace(
                            str(list_data[0]), ""
                        )

                try:
                    extra_args = shlex.split(get_regex[2])
                    line += " "
                    line += " ".join(extra_args).replace(",", "")
                    line += f" {list_data or ''}"
                except (ValueError, IndexError):
                    pass

        return line.strip()

    def precmd(self, line) -> str:
        """Modifies the command line received before it is interpreted.

        The job of this method is two folds

            - It performs a mini case-insensitivity for the 'EOF' string
            when received on the command line.
            - It aids in adding new lines before printing the help messages
            for commands.

        Args:
            line (str): The command line to modify

        Returns:
            str: The modified command if touched, else it returned as received.
        """
        if line and line == "EOF":
            return line.lower()

        try:
            if (
                line
                and shlex.split(line)[0] in ["help", "?"]
                and len(line.split()) > 1
            ):
                print()
        except (ValueError, IndexError):
            self.onecmd(f"{line}")
            return ""

        return line

    def postcmd(self, stop: bool, line: str) -> bool:
        """Adds a newline after the help message for commands.

        Args:
            stop (bool): Determines whether the console should keep running.
            line (str): The command line received.

        Returns:
            bool: True if the console should exit, else False.
        """
        if (
            line
            and shlex.split(line)[0] in ["help", "?"]
            and len(line.split()) > 1
        ):
            print()

        return stop

    def completedefault(self, *text) -> "list[str]":
        """Performs the name completion for model names.

        Returns:
            list[str]: The list of model names.
        """
        if not text:
            completions = list(self.__models.keys())[:]
        else:
            completions = [
                model for model in self.__models if model.startswith(text[0])
            ]

        return completions

    def __is_valid_args(
        self, line, check_class=False, check_id=False, check_attributes=False
    ) -> bool:
        """Performs simple checks on the line received from the command line.

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
        try:
            args = shlex.split(line)
        except ValueError:
            args = ""

        def __is_valid_args_helper(args: str) -> bool:
            """A simple helper function for `__is_valid_args()`."""
            if check_class:
                if not args:
                    print("** class name missing **")
                    return False

                if args[0] not in self.__models:
                    print("** class doesn't exist **")
                    return False

            if check_id:
                if len(args) == 1:
                    print("** instance id missing **")
                    return False

            if check_attributes:
                if len(re.findall(r"\{[^}]*$", line)) != 0 or len(args) < 3:
                    print("** attribute name missing **")
                    return False

                if len(args) < 4:
                    print("** value missing **")
                    return False

            return True

        return __is_valid_args_helper(args)

    @staticmethod
    def __search_instance(
        instance_class: str, instance_id: str
    ) -> "object | None":
        """Searches for an instance by it's id and class name.

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

    @staticmethod
    def do_quit(_) -> bool:
        """Quit command to exit the console."""
        return True

    @staticmethod
    def do_eof(_) -> bool:
        """Exits the console gracefully."""
        print()
        return True

    def do_create(self, class_name: str) -> None:
        """Creates a new instance of a model and saves it to a JSON file.

        Args:
            class_name (str): The expected class name.
        """
        if not self.__is_valid_args(class_name, check_class=True):
            return

        obj = self.__models[shlex.split(class_name)[0]]()
        obj.save()
        print(obj.id)

    @staticmethod
    def help_create() -> None:
        """Prints the help info for the `create` command."""
        print(
            "Creates an  instance of a model and saves it to a JSON file.",
            "Usage:",
            "\tOption 1: create <class name>",
            "\tOption 2: <class name>.create()",
            sep="\n",
        )

    def do_show(self, line) -> None:
        """Prints the string representation of an instance based on the class
        name and id.

        Args:
            line (str): The command line argument received.
        """
        if not self.__is_valid_args(line, check_class=True, check_id=True):
            return

        instance_class = instance_id = ""

        try:
            instance_class, instance_id = shlex.split(line)
        except ValueError:
            print("** too many arguments **")
            return

        instance = self.__search_instance(instance_class, instance_id)
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
            "Usage:",
            "\tOption 1: show <class name> <id>",
            "\tOption 2: <class name>.show(<id>)",
            sep="\n",
        )

    def do_destroy(self, line) -> None:
        """Deletes an instance base on the class name and id

        Args:
            line (str): The command line argument received.
        """
        instance_class = instance_id = ""

        if not self.__is_valid_args(line, check_class=True, check_id=True):
            return

        instance_class, instance_id = shlex.split(line)

        instance = self.__search_instance(instance_class, instance_id)
        if instance:
            objects = storage.all()

            # delete the current instance
            del objects[f"{instance.__class__.__name__}.{instance.id}"]

            # save the updated objects dictionary
            storage.save()
        else:
            print("** no instance found **")

    @staticmethod
    def help_destroy() -> None:
        """Prints the help info for the `show` command."""
        print(
            "Deletes an instance based on the class name and id",
            "Usage:",
            "\tOption 1: destroy <class name> <id>",
            "\tOption 2: <class name>.destroy(<id>)",
            sep="\n",
        )

    def do_all(self, model_name: str) -> None:
        """Prints the string representation for all or some model instances."""
        if model_name and shlex.split(model_name)[0] not in self.__models:
            print("** class doesn't exist **")
            return

        objects = storage.all()
        instances = []

        # print the instances for a specific model, if provided
        if model_name:
            for obj in objects.values():
                if obj.__class__.__name__ == model_name:
                    instances.append(str(obj))
        else:
            # print all the instances available
            for obj in objects.values():
                instances.append(str(obj))

        print(instances)

    @staticmethod
    def help_all() -> None:
        """Prints the help info for the `all` command."""
        print(
            "Prints the string representation for all or a specified model's "
            "instances.",
            "Usage:",
            "\tOption 1: all [<class name>]",
            "\tOption 2: <class name>.all()",
            sep="\n",
        )

    def do_update(self, arg: str) -> None:
        """Updates an instance based on the class name and id by adding or
        updating attributes.

        After a successful update, it is saved to a JSON file. In the event no
        instances are found for the provided class name and id, nothing is done
        and an error is printed on the screen.

        Args:
            arg (str): The command line argument.
        """
        if not self.__is_valid_args(
            arg, check_class=True, check_id=True, check_attributes=True
        ):
            return

        # grab the four expected arguments, all other arguments are ignored
        instance_class, instance_id, attr_name = shlex.split(arg)[:3]

        instance = self.__search_instance(instance_class, instance_id)

        if instance:
            try:
                attr_val = re.findall(r"\{.*\}", arg)[0]
            except IndexError:
                attr_val = shlex.split(arg)[3]

            try:
                # evaluating the value based on its default builtin type
                attr_val = literal_eval(attr_val)
            except (ValueError, SyntaxError):
                # well, looks like we'd have to save it as it was received
                instance.__dict__[attr_name] = attr_val
            else:
                if isinstance(attr_val, dict):
                    instance.__dict__.update(attr_val)
                else:
                    instance.__dict__[attr_name] = attr_val

            instance.save()
        else:
            print("** no instance found **")

    @staticmethod
    def help_update() -> None:
        """Prints the help info for the `update` command."""
        print(
            "Updates an instance based on the class name and id by adding or "
            "updating attributes.",
            "Usage:",
            "\tOption 1: "
            'update <class name> <id> <attribute name> "<attribute value>"',
            "\tOption 2: "
            "<class name>.update(<id>, <attribute name>, <attribute value>)",
            "\tOption 3: "
            "<class name>.update(<id>, <dictionary representation>)",
            sep="\n",
        )

    def do_count(self, model_name) -> None:
        """Prints the number of instances for a particular model."""
        if not self.__is_valid_args(model_name, check_class=True):
            return

        objects = storage.all()
        instance_count = 0

        for obj in objects.values():
            if obj.__class__.__name__ == model_name:
                instance_count += 1

        print(instance_count)

    @staticmethod
    def help_count() -> None:
        """Prints the help info for the `count` command."""
        print(
            "Prints the number of instances for a particular model.",
            "Usage:",
            "\tOption 1: count <class name>",
            "\tOption 2: <class name>.count()",
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
