#!/usr/bin/python3
"""Defines the HBnB console interface."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arguments):
    """Parse the input arguments and return a list of tokens."""
    braces_content = re.search(r"\{(.*?)\}", arguments)
    brackets_content = re.search(r"\[(.*?)\]", arguments)
    if braces_content is None:
        if brackets_content is None:
            return [token.strip(",") for token in split(arguments)]
        else:
            lexer = split(arguments[:brackets_content.span()[0]])
            token_list = [token.strip(",") for token in lexer]
            token_list.append(brackets_content.group())
            return token_list
    else:
        lexer = split(arguments[:braces_content.span()[0]])
        token_list = [token.strip(",") for token in lexer]
        token_list.append(braces_content.group())
        return token_list


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt text.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Override default behavior to do nothing on empty input."""
        pass

    def default(self, line):
        """Handle unrecognized commands."""
        command_map = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match:
            class_name, method_call = line[:match.span()[0]], line[match.span()[1]:]
            match = re.search(r"\((.*?)\)", method_call)
            if match:
                method_name, method_args = method_call[:match.span()[0]], match.group()[1:-1]
                if method_name in command_map:
                    return command_map[method_name]("{} {}".format(class_name, method_args))
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def do_EOF(self, arg):
        """Handle EOF to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Create a new instance of a class."""
        args = parse(arg)
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(args[0])()
            print(new_instance.id)
            storage.save()

    def do_show(self, arg):
        """Show the string representation of an instance based on class and id."""
        args = parse(arg)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(args[0], args[1])])

    def do_destroy(self, arg):
        """Delete an instance based on class and id."""
        args = parse(arg)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict:
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, arg):
        """Show all instances, or all instances of a class."""
        args = parse(arg)
        if args and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            instances = []
            for obj in storage.all().values():
                if not args or args[0] == obj.__class__.__name__:
                    instances.append(str(obj))
            print(instances)

    def do_count(self, arg):
        """Count the number of instances of a class."""
        args = parse(arg)
        count = sum(1 for obj in storage.all().values() if args[0] == obj.__class__.__name__)
        print(count)

    def do_update(self, arg):
        """Update an instance by adding or updating attributes."""
        args = parse(arg)
        obj_dict = storage.all()

        if not args:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in obj_dict:
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                eval(args[2])
            except NameError:
                print("** value missing **")
                return False

        instance = obj_dict["{}.{}".format(args[0], args[1])]
        if len(args) == 4:
            attr_name = args[2]
            attr_value = args[3]
            if attr_name in instance.__class__.__dict__:
                attr_type = type(instance.__class__.__dict__[attr_name])
                instance.__dict__[attr_name] = attr_type(attr_value)
            else:
                instance.__dict__[attr_name] = attr_value
        elif isinstance(eval(args[2]), dict):
            for key, value in eval(args[2]).items():
                if key in instance.__class__.__dict__ and type(instance.__class__.__dict__[key]) in {str, int, float}:
                    attr_type = type(instance.__class__.__dict__[key])
                    instance.__dict__[key] = attr_type(value)
                else:
                    instance.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
