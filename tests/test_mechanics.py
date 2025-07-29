from app import create_app
from app.models import db, Mechanics
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanics(
            name="test_user",
            email="test@email.com",
            phone="123-456-7890",
            salary="70000.00"
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "012-345-6789",
            "salary": "75000.00"
        }
        
        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        
    def test_update_mechanic(self):
        update_payload = {
            "name": "Peter",
            "email": "test@email.com",
            "phone": "123-456-7890",
            "salary": "70000.00"
        }
        
        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')
        
    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Mechanic id: 1, successfully deleted')
        
    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_get_one_mechanic(self):
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')
        
    def test_get_sorted_mechanics(self):
        response = self.client.get('/mechanics/popular')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)