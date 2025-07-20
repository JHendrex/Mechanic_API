from flask import request, jsonify
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from app.extensions import limiter, cache
from marshmallow import ValidationError
from app.models import Mechanics, db
from sqlalchemy import select


#Create new mechanic
@mechanics_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour") #only 3 new mechanics can be added per hour
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanics).where(Mechanics.email == mechanic_data['email'])
    existing_mechanic_email = db.session.execute(query).scalars().all()
    if existing_mechanic_email:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    query = select(Mechanics).where(Mechanics.phone == mechanic_data['phone'])
    existing_mechanic_phone = db.session.execute(query).scalars().all()
    if existing_mechanic_phone:
        return jsonify({"error": "Phone number already associated with an account."}), 400
    
    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

#Get all mechanics
@mechanics_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_mechanics():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)

#Get Specific mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404

#Update Specific mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#Delete Specific mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Mechanic id: {mechanic_id}, successfully deleted'}), 200