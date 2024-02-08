#!/usr/bin/python3

"""Implements the command interpreter."""

import cmd


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter."""

    prompt = "(hbnb) "

    @staticmethod
    def do_quit(_) -> bool:
        """Quit command to exit the program."""
        return True

    @staticmethod
    def do_eof(_) -> bool:
        """Handles the Ctrl+D signal (EOF)."""
        print()
        return True

    def emptyline(self) -> None:
        pass

    def default(self, line: str) -> None:
        print(f"Unknown command: {line}")

    def precmd(self, line):
        if line and line == "EOF":
            return line.lower()
        return line


if __name__ == "__main__":
    HBNBCommand().cmdloop()
