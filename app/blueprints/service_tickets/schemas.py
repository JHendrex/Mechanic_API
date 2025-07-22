from app.models import Service_Tickets
from app.extensions import ma
from marshmallow import fields

#Service Tickets Schema        
class Service_TicketsSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Integer(required=True)
    customer = fields.Nested("CustomersSchema", only=["id", "name"])
    mechanics = fields.Nested("MechanicsSchema", many=True, only=["id", "name"])
    inventory = fields.Nested("InventorySchema", many=True, only=["id", "name", "price"])
    class Meta:
        model = Service_Tickets

class Edit_TicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")
        
class Item_TicketSchema(ma.Schema):
    add_item_ids = fields.List(fields.Int(), required=True)
    remove_item_ids = fields.List(fields.Int(), required=True)
        
service_ticket_schema = Service_TicketsSchema()
service_tickets_schema = Service_TicketsSchema(many=True)
edit_ticket_schema = Edit_TicketSchema()
item_ticket_schema = Item_TicketSchema()