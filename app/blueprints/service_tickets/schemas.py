from app.models import Service_Tickets
from app.extensions import ma
from marshmallow import fields

#Service Tickets Schema        
class Service_TicketsSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Integer(required=True)
    customer = fields.Nested("CustomersSchema")
    mechanics = fields.Nested("MechanicsSchema", many=True, only=["id", "name"])
    class Meta:
        model = Service_Tickets

class Edit_TicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")
        
service_ticket_schema = Service_TicketsSchema()
service_tickets_schema = Service_TicketsSchema(many=True)
edit_ticket_schema = Edit_TicketSchema()