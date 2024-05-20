#!/usr/bin/python3
"""
Unittests for the FileStorage class.
"""

import unittest
import os
import json
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test cases for the FileStorage class."""

    def setUp(self):
        """Set up test methods."""
        self.storage = FileStorage()
        self.file_path = FileStorage._FileStorage__file_path
        self.objects = FileStorage._FileStorage__objects

    def tearDown(self):
        """Tear down test methods."""
        try:
            os.remove(self.file_path)
        except Exception:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        """Test that all method returns the __objects dictionary."""
        self.assertIsInstance(self.storage.all(), dict)
        self.assertIs(self.storage.all(), self.objects)

    def test_new_adds_object(self):
        """Test that new method adds an object to __objects."""
        obj = BaseModel()
        self.storage.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, self.objects)
        self.assertEqual(self.objects[key], obj)

    def test_save_creates_file(self):
        """Test that save method creates a file."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_save_saves_to_file(self):
        """Test that save method serializes __objects to the file."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, data)
        self.assertEqual(data[key]["id"], obj.id)

    def test_reload_loads_from_file(self):
        """Test that reload method deserializes the file to __objects."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, self.storage.all())
        self.assertIsInstance(self.storage.all()[key], BaseModel)

    def test_reload_no_file(self):
        """Test that reload method does nothing if no file exists."""
        try:
            self.storage.reload()
        except Exception as e:
            self.fail(f"reload raised {type(e).__name__} unexpectedly!")

    def test_reload_invalid_json(self):
        """Test that reload method handles invalid JSON file correctly."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("{invalid json}")
        try:
            self.storage.reload()
        except Exception as e:
            self.fail(f"reload raised {type(e).__name__} unexpectedly!")

    def test_classes_method(self):
        """Test that classes method returns the correct class references."""
        classes = self.storage.classes()
        self.assertIn("BaseModel", classes)
        self.assertIn("User", classes)
        self.assertEqual(classes["BaseModel"], BaseModel)
        self.assertEqual(classes["User"], User)

    def test_attributes_method(self):
        """Test that attributes method returns the correct attributes."""
        attributes = self.storage.attributes()
        self.assertIn("BaseModel", attributes)
        self.assertIn("User", attributes)
        self.assertEqual(attributes["BaseModel"]["id"], str)
        self.assertEqual(attributes["User"]["email"], str)

if __name__ == "__main__":
    unittest.main()
