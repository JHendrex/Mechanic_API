from app.models import Customers
from app.extensions import ma
from marshmallow import fields

#Customer Schema
class CustomersSchema(ma.SQLAlchemyAutoSchema):
    service_tickets = fields.Nested("Service_TicketsSchema", many=True, only=["id", "VIN", "service_date", "service_desc"])
    class Meta:
        model = Customers
        
customer_schema = CustomersSchema()
customers_schema = CustomersSchema(many=True)
login_schema = CustomersSchema(exclude=['name', 'phone'])