from app.models import Mechanics
from app.extensions import ma
from marshmallow import fields

#Mechanics Schema
class MechanicsSchema(ma.SQLAlchemyAutoSchema):
    service_tickets = fields.Nested("Service_TicketsSchema", many=True, only=["id", "VIN", "service_date"])
    class Meta:
        model = Mechanics
        
mechanic_schema = MechanicsSchema()
mechanics_schema = MechanicsSchema(many=True)