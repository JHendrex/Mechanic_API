from app import create_app
from app.models import db, Customers, Service_Tickets
from datetime import datetime
from app.utils.util import encode_token
import unittest


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customers(
            name="test_user",
            email="test@email.com",
            password="test",
            phone="123-456-7890"
        )
        self.service_ticket = Service_Tickets(
            VIN="1a2b3c4d5e6f7g8h9",
            service_date=datetime.strptime("2023-10-01", "%Y-%m-%d").date(),
            service_desc="Test service description.",
            customer_id="1",
            mechanics=[],
            inventory=[]
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.add(self.service_ticket)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
        
    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "password": "password123",
            "phone": "012-345-6789"
        }
        
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        
    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "password": "password123",
            "phone": "123-456-7890"
        }
        
        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])
        
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }
        
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }
        
        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
        
    def test_update_customer(self):
        update_payload = {
            "name": "Peter",
            "email": "test@email.com",
            "password": "test",
            "phone": "123-456-7890"
        }
        
        headers = {'Authorization': f'Bearer {self.test_login_customer()}'}
        
        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')  
        
    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        
    def test_get_one_customer(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')
        
    def test_get_all_tickets_for_customer(self):
        headers = {'Authorization': f'Bearer {self.test_login_customer()}'}
        
        response = self.client.get('/customers/my_tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(any(ticket['VIN'] == '1a2b3c4d5e6f7g8h9' for ticket in response.json))
        
    def test_delete_customer(self):
        headers = {'Authorization': f'Bearer {self.test_login_customer()}'}
        
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Customer id: 1, successfully deleted')