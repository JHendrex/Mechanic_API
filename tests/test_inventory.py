from app import create_app
from app.models import db, Inventory, Service_Tickets
from datetime import datetime
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.item = Inventory(
            name="Test Item",
            price="70.00"
        )
        self.service_ticket = Service_Tickets(
            VIN="1a2b3c4d5e6f7g8h9",
            service_date=datetime.strptime("2023-10-01", "%Y-%m-%d").date(),
            service_desc="Test service description.",
            customer_id="1",
            mechanics=[],
            inventory=[self.item]
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.item)
            db.session.add(self.service_ticket)
            db.session.commit()
        self.client = self.app.test_client()
        
    def test_create_item(self):
        item_payload = {
            "name": "New Item",
            "price": "50.00"
        }
        
        response = self.client.post('/inventory/', json=item_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "New Item")
        
    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        
    def test_get_item(self):
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Test Item")
        
    def test_get_tickets_for_item(self):
        response = self.client.get('/inventory/1/tickets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertTrue(any(ticket['VIN'] == '1a2b3c4d5e6f7g8h9' for ticket in response.json))
        
    def test_update_item(self):
        item_payload = {
            "name": "Updated Item",
            "price": "60.00"
        }
        
        response = self.client.put('/inventory/1', json=item_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Item")
        
    def test_delete_item(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item id: 1, successfully deleted')