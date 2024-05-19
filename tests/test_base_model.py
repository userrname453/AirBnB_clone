#!/usr/bin/python3
import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        """Set up test case environment."""
        self.model = BaseModel()

    def test_initialization(self):
        """Test the initialization of BaseModel."""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model.id, str)
        self.assertTrue(uuid.UUID(self.model.id))
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_str(self):
        """Test the string representation of BaseModel."""
        string = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), string)

    def test_save(self):
        """Test the save method updates updated_at attribute."""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)
        self.assertTrue(self.model.updated_at > old_updated_at)

    def test_to_dict(self):
        """Test the to_dict method."""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['id'], self.model.id)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['created_at'], self.model.created_at.isoformat())
        self.assertEqual(model_dict['updated_at'], self.model.updated_at.isoformat())
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    def test_to_dict_with_additional_attributes(self):
        """Test to_dict with additional attributes."""
        self.model.name = "My First Model"
        self.model.my_number = 89
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict['name'], "My First Model")
        self.assertEqual(model_dict['my_number'], 89)
        self.assertIsInstance(model_dict['name'], str)
        self.assertIsInstance(model_dict['my_number'], int)

if __name__ == "__main__":
    unittest.main()
