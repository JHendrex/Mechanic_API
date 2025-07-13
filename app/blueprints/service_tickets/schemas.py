from app.models import Service_Tickets
from app.extensions import ma
from marshmallow import fields

#Service Tickets Schema        
class Service_TicketsSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Integer(required=True, load_only=True)
    
    class Meta:
        model = Service_Tickets
        
service_ticket_schema = Service_TicketsSchema()
service_tickets_schema = Service_TicketsSchema(many=True)