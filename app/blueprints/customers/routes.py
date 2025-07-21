from flask import request, jsonify
from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from app.blueprints.service_tickets.schemas import service_tickets_schema
from app.extensions import cache
from marshmallow import ValidationError
from app.models import Customers, Service_Tickets, db
from sqlalchemy import select
from app.utils.util import encode_token, token_required


@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customers).where(Customers.email == email)
    customer = db.session.execute(query).scalars().first()
    
    if customer and customer.password == password:
        token = encode_token(customer.id)
        
        response = {
            "status": "success",
            "message": "successfully logged in",
            "token": token
        }
        
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 401

#Create new customer
@customers_bp.route("/", methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customers).where(Customers.email == customer_data['email'])
    existing_customer_email = db.session.execute(query).scalars().all()
    if existing_customer_email:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    query = select(Customers).where(Customers.phone == customer_data['phone'])
    existing_customer_phone = db.session.execute(query).scalars().all()
    if existing_customer_phone:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_customer = Customers(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#Get all customers
@customers_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    query = select(Customers)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers)

#Get Specific Customer
@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    
    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

@customers_bp.route("/my_tickets", methods=['GET'])
@token_required
def my_tickets(customer_id):
    query = select(Service_Tickets).where(Service_Tickets.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets)

#Update Specific Customer
@customers_bp.route("/", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200

#Delete Specific Customer
@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {customer_id}, successfully deleted'}), 200