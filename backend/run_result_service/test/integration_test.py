import os
import unittest
import json
from backend.run_result_service.source import create_app, db
from backend.run_result_service.source.models import Tool
from datetime import datetime


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.create_sample_data()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_sample_data(self):
        tool1 = Tool(name="tool1", schema={"project": "str", "field2": "int"})
        tool2 = Tool(name="tool2", schema={"project": "str", "fieldB": "list[int]"})
        db.session.add(tool1)
        db.session.add(tool2)
        db.session.commit()

    def test_get_tools(self):
        response = self.client.get('/get_tools')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'tool1')
        self.assertEqual(data[1]['name'], 'tool2')

    def test_add_tool(self):
        response = self.client.post('/admin/add_tool',
                                    json={'name': 'tool3', 'schema': {'fieldX': 'str', 'fieldY': 'bool'}})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)

        response = self.client.post('/admin/add_tool',
                                    json={'name': 'tool3', 'schema': {'fieldX': 'str', 'fieldY': 'bool'}})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_filtered_data(self):
        response = self.client.get('/get_filtered_data', query_string={'per_page': 2})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('data', data)
        self.assertIn('last_id', data)

    def test_add_data(self):
        data = {
            "tool": "tool1",
            "data": {"project": "value1", "field2": 123},
            "time": datetime.utcnow().isoformat() + 'Z'
        }
        response = self.client.post('/run_result', json=data)
        self.assertEqual(response.status_code, 200)
        kafka_metadata = response.json["kafka_metadata"]
        self.assertIn('topic', kafka_metadata)


if __name__ == '__main__':
    unittest.main()
