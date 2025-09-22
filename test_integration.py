import unittest
from flask_testing import TestCase
from cognigrasp_demo import app, db
from models import StudyMaterial
import json


class CogniGraspIntegrationTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_full_integration(self):
        # Step 1: Access homepage
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Step 2: Process study material
        test_input = "The quadratic formula is used to solve quadratic equations."
        response = self.client.post('/process', data={'study_material': test_input})
        self.assertEqual(response.status_code, 200)

        # Step 3: Verify data was saved
        material = StudyMaterial.query.first()
        self.assertIsNotNone(material)
        self.assertEqual(material.input_text, test_input)

        # Step 4: Access the material via API
        response = self.client.get(f'/api/materials/{material.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['subject'], 'math')

        # Step 5: Access stats via API
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_materials'], 1)


if __name__ == '__main__':
    unittest.main()