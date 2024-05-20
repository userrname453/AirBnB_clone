#!/usr/bin/python3
"""
Unittests for the HBNB console.
"""

import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
import os


class TestHBNBCommand(unittest.TestCase):
    """Tests the HBNBCommand class."""

    def setUp(self):
        """Sets up the test environment."""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tears down the test environment."""
        if os.path.isfile('file.json'):
            os.remove('file.json')
        storage.__objects = {}

    def test_emptyline(self):
        """Test empty line input."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("")
            self.assertEqual(output.getvalue(), "")

    def test_quit(self):
        """Test quit command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.console.onecmd("quit"))
            self.assertEqual(output.getvalue(), "")

    def test_EOF(self):
        """Test EOF command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.assertTrue(self.console.onecmd("EOF"))
            self.assertEqual(output.getvalue().strip(), "")

    def test_create(self):
        """Test create command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("create BaseModel")
            output_str = output.getvalue().strip()
            self.assertTrue(output_str)
            self.assertIn("BaseModel.{}".format(output_str), storage.all())

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("create NonExistentClass")
            self.assertEqual(output.getvalue().strip(), "** class doesn't exist **")

    def test_show(self):
        """Test show command."""
        new_instance = BaseModel()
        new_instance.save()
        instance_id = new_instance.id

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("show BaseModel {}".format(instance_id))
            self.assertIn(instance_id, output.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("show BaseModel 12345")
            self.assertEqual(output.getvalue().strip(), "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("show NonExistentClass {}".format(instance_id))
            self.assertEqual(output.getvalue().strip(), "** class doesn't exist **")

    def test_destroy(self):
        """Test destroy command."""
        new_instance = BaseModel()
        new_instance.save()
        instance_id = new_instance.id

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("destroy BaseModel {}".format(instance_id))
            self.assertNotIn("BaseModel.{}".format(instance_id), storage.all())

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual(output.getvalue().strip(), "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("destroy NonExistentClass {}".format(instance_id))
            self.assertEqual(output.getvalue().strip(), "** class doesn't exist **")

    def test_all(self):
        """Test all command."""
        new_instance1 = BaseModel()
        new_instance1.save()
        new_instance2 = BaseModel()
        new_instance2.save()

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("all")
            self.assertIn(new_instance1.id, output.getvalue().strip())
            self.assertIn(new_instance2.id, output.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("all BaseModel")
            self.assertIn(new_instance1.id, output.getvalue().strip())
            self.assertIn(new_instance2.id, output.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("all NonExistentClass")
            self.assertEqual(output.getvalue().strip(), "** class doesn't exist **")

    def test_count(self):
        """Test count command."""
        new_instance1 = BaseModel()
        new_instance1.save()
        new_instance2 = BaseModel()
        new_instance2.save()

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("count BaseModel")
            self.assertEqual(output.getvalue().strip(), "2")

    def test_update(self):
        """Test update command."""
        new_instance = BaseModel()
        new_instance.save()
        instance_id = new_instance.id

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd('update BaseModel {} name "Holberton"'.format(instance_id))
            self.assertIn('Holberton', storage.all()["BaseModel.{}".format(instance_id)].__dict__.values())

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("update BaseModel 12345 name 'Holberton'")
            self.assertEqual(output.getvalue().strip(), "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as output:
            self.console.onecmd("update NonExistentClass {} name 'Holberton'".format(instance_id))
            self.assertEqual(output.getvalue().strip(), "** class doesn't exist **")

if __name__ == "__main__":
    unittest.main()
