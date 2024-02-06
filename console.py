#!/usr/bin/python3

"""Implements the command interpreter."""


import cmd


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter."""

    prompt = "(hbnb) "

    @staticmethod
    def do_quit(_) -> bool:
        """Quit command to exit the program"""
        return True

    # `EOF` and `quit` do about the same thing so... B-)
    do_EOF = do_quit

    def emptyline(self) -> None:
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
