from app import create_app
from app.models import db, Service_Tickets, Mechanics, Inventory
from datetime import datetime
import unittest


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.service_ticket = Service_Tickets(
            VIN="1a2b3c4d5e6f7g8h9",
            service_date=datetime.strptime("2023-10-01", "%Y-%m-%d").date(),
            service_desc="Test service description.",
            customer_id="1",
            mechanics=[],
            inventory=[]
        )
        self.mechanic = Mechanics(
            name="test_user",
            email="test@email.com",
            phone="123-456-7890",
            salary="70000.00"
        )
        self.item = Inventory(
            name="Test Item",
            price="70.00"
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.service_ticket)
            db.session.add(self.mechanic)
            db.session.add(self.item)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_service_ticket(self):
        service_ticket_payload = {
            "VIN": "1a2b3c4d5e6f7g8h9",
            "service_date": "2023-10-02",
            "service_desc": "New service description.",
            "customer_id": "1"
        }
        
        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['VIN'], "1a2b3c4d5e6f7g8h9")
        
    def test_get_service_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        
    def test_get_one_service_tickets(self):
        response = self.client.get('/service_tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['VIN'], "1a2b3c4d5e6f7g8h9")
        
    def test_add_mechanic(self):
        edit_payload = {
            "add_mechanic_ids": [1],
            "remove_mechanic_ids": []
        }
        
        response = self.client.put('/service_tickets/1/edit', json=edit_payload)
        self.assertEqual(response.status_code, 200)
        mechanics = response.json['mechanics']
        self.assertTrue(any(mechanic['id'] == 1 for mechanic in mechanics))
        
    def test_remove_mechanic(self):
        edit_payload = {
            "add_mechanic_ids": [],
            "remove_mechanic_ids": [1]
        }
        
        response = self.client.put('/service_tickets/1/edit', json=edit_payload)
        self.assertEqual(response.status_code, 200)
        mechanics = response.json['mechanics']
        self.assertFalse(any(mechanic['id'] == 1 for mechanic in mechanics))
        
    def test_add_item(self):
        item_payload = {
            "add_item_ids": [1],
            "remove_item_ids": []
        }
        
        response = self.client.put('/service_tickets/1/item', json=item_payload)
        self.assertEqual(response.status_code, 200)
        items = response.json['inventory']
        self.assertTrue(any(mechanic['id'] == 1 for mechanic in items))
        
    def test_remove_item(self):
        item_payload = {
            "add_item_ids": [],
            "remove_item_ids": [1]
        }
        
        response = self.client.put('/service_tickets/1/item', json=item_payload)
        self.assertEqual(response.status_code, 200)
        items = response.json['inventory']
        self.assertFalse(any(mechanic['id'] == 1 for mechanic in items))