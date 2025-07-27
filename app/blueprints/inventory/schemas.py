from app.models import Inventory
from app.extensions import ma
from marshmallow import fields

#Inventory Schema
class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)