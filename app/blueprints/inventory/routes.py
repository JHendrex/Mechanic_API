from flask import request, jsonify
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema
from app.blueprints.service_tickets.schemas import service_tickets_schema
from app.extensions import cache
from marshmallow import ValidationError
from app.models import Inventory, Service_Tickets, db
from sqlalchemy import select

#Create new item in inventory
@inventory_bp.route("/", methods=['POST'])
def create_item():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_item = Inventory(**inventory_data)
    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201

#Get all items in inventory
@inventory_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_inventory():
    try:
        page = request.args.get('page')
        per_page = int(request.args.get('per_page'))
        query = select(Inventory)
        items = db.paginate(query, page=page, per_page=per_page)
        return inventories_schema.jsonify(items), 200
    except:    
        query = select(Inventory)
        items = db.session.execute(query).scalars().all()
        return inventories_schema.jsonify(items), 200
    
#Get specific item in inventory
@inventory_bp.route("/<int:inventory_id>", methods=['GET'])
def get_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    
    if item:
        return inventory_schema.jsonify(item), 200
    return jsonify({"error": "Item not found."}), 404

#Get all service tickets for an item
@inventory_bp.route("/<int:inventory_id>/tickets", methods=['GET'])
def item_tickets(inventory_id):
    query = select(Service_Tickets).join(Service_Tickets.inventory).where(Inventory.id == inventory_id)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200

#Update specific item
@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
def update_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    
    if not item:
        return jsonify({"error": "Item not found."}), 404
    
    try:
        item_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in item_data.items():
        setattr(item, key, value)
        
    db.session.commit()
    return inventory_schema.jsonify(item), 200

#Delete specific item
@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)
    
    if not item:
        return jsonify({"error": "Item not found."}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f'Item id: {inventory_id}, successfully deleted'}), 200