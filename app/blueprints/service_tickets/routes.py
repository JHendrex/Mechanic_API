from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from app.extensions import cache
from marshmallow import ValidationError
from app.models import Service_Tickets, Mechanics,db
from sqlalchemy import select


#Create new service_ticket
@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_Tickets(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

#Get all service_tickets
@service_tickets_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_service_tickets():
    query = select(Service_Tickets)
    service_tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(service_tickets)

#Get Specific service_ticket
@service_tickets_bp.route("/<int:service_ticket_id>", methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    
    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket), 200
    return jsonify({"error": "service_ticket not found."}), 404

#Add mechanic to specific service_ticket
@service_tickets_bp.route("/<int:service_ticket_id>/add_mechanic/<int:mechanic_id>", methods=['PUT'])
def add_mechanic_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not service_ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found."}), 404
    
    if mechanic not in service_ticket.mechanics:
        service_ticket.mechanics.append(mechanic)
        
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

#Remove mechanic from specific service_ticket
@service_tickets_bp.route("/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not service_ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found."}), 404
    
    if mechanic in service_ticket.mechanics:
        service_ticket.mechanics.remove(mechanic)
        
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200