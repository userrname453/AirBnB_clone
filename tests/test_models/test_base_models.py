#!/usr/bin/python3
"""
Unittests for the BaseModel class.
"""

import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
import uuid


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def setUp(self):
        """Set up test methods."""
        self.instance = BaseModel()

    def tearDown(self):
        """Tear down test methods."""
        del self.instance

    def test_id_is_str(self):
        """Test if id is a string."""
        self.assertIsInstance(self.instance.id, str)

    def test_unique_id(self):
        """Test if ids are unique."""
        instance2 = BaseModel()
        self.assertNotEqual(self.instance.id, instance2.id)

    def test_created_at_is_datetime(self):
        """Test if created_at is a datetime object."""
        self.assertIsInstance(self.instance.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test if updated_at is a datetime object."""
        self.assertIsInstance(self.instance.updated_at, datetime)

    def test_str_representation(self):
        """Test the string representation of the instance."""
        self.instance.name = "Holberton"
        string = "[BaseModel] ({}) {}".format(self.instance.id, self.instance.__dict__)
        self.assertEqual(str(self.instance), string)

    def test_save_updates_updated_at(self):
        """Test that save method updates updated_at."""
        old_updated_at = self.instance.updated_at
        sleep(0.1)
        self.instance.save()
        self.assertNotEqual(self.instance.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test conversion of instance to dictionary."""
        self.instance.name = "Holberton"
        self.instance.my_number = 89
        instance_dict = self.instance.to_dict()
        self.assertEqual(instance_dict["name"], "Holberton")
        self.assertEqual(instance_dict["my_number"], 89)
        self.assertEqual(instance_dict["__class__"], "BaseModel")
        self.assertIsInstance(instance_dict["created_at"], str)
        self.assertIsInstance(instance_dict["updated_at"], str)

    def test_to_dict_values(self):
        """Test the values in the dictionary returned from to_dict."""
        instance_dict = self.instance.to_dict()
        self.assertEqual(instance_dict["id"], self.instance.id)
        self.assertEqual(instance_dict["created_at"], self.instance.created_at.isoformat())
        self.assertEqual(instance_dict["updated_at"], self.instance.updated_at.isoformat())

    def test_kwargs_initialization(self):
        """Test initialization from kwargs."""
        instance_dict = self.instance.to_dict()
        new_instance = BaseModel(**instance_dict)
        self.assertEqual(new_instance.id, self.instance.id)
        self.assertEqual(new_instance.created_at, self.instance.created_at)
        self.assertEqual(new_instance.updated_at, self.instance.updated_at)
        self.assertEqual(new_instance.__class__.__name__, "BaseModel")

    def test_kwargs_initialization_extra(self):
        """Test initialization from kwargs with extra attributes."""
        instance_dict = self.instance.to_dict()
        instance_dict["name"] = "Holberton"
        new_instance = BaseModel(**instance_dict)
        self.assertEqual(new_instance.id, self.instance.id)
        self.assertEqual(new_instance.created_at, self.instance.created_at)
        self.assertEqual(new_instance.updated_at, self.instance.updated_at)
        self.assertEqual(new_instance.name, "Holberton")

    def test_args_ignored(self):
        """Test that args are ignored in initialization."""
        new_instance = BaseModel("Holberton")
        self.assertNotIn("Holberton", new_instance.__dict__.values())

    def test_unique_uuid(self):
        """Test that the UUIDs are unique."""
        id1 = self.instance.id
        id2 = BaseModel().id
        self.assertNotEqual(id1, id2)

    def test_datetime_attributes(self):
        """Test that the created_at and updated_at are datetime objects."""
        self.assertIsInstance(self.instance.created_at, datetime)
        self.assertIsInstance(self.instance.updated_at, datetime)

    def test_save(self):
        """Test that the save method updates the updated_at attribute."""
        old_updated_at = self.instance.updated_at
        self.instance.save()
        self.assertNotEqual(self.instance.updated_at, old_updated_at)

    def test_to_dict_output(self):
        """Test the dictionary output of to_dict method."""
        instance_dict = self.instance.to_dict()
        self.assertEqual(instance_dict["id"], self.instance.id)
        self.assertEqual(instance_dict["created_at"], self.instance.created_at.isoformat())
        self.assertEqual(instance_dict["updated_at"], self.instance.updated_at.isoformat())
        self.assertEqual(instance_dict["__class__"], "BaseModel")


if __name__ == "__main__":
    unittest.main()
