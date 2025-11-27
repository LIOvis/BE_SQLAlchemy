from flask import request, jsonify

from models.warranty import Warranties
from models.product import Products
from db import db

def add_warranty():
    post_data = request.form if request.form else request.json

    fields = ['product_id', 'warranty_months']
    required_fields = ['product_id', 'warranty']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 404
        
        values[field] = field_data

    product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()

    if not product_query:
        return jsonify({"message": "product not found"}), 404
    
    new_warranty = Warranties(values['product_id'], values['warranty_months'])

    try:
        db.session.add(new_warranty)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Warranties).filter(Warranties.product_id == values['product_id']).first()


    product_dict = {
        "product_id": query.product.product_id,
        "product_name": query.product.product_name,
        "description": query.product.description,
        "price": query.product.price,
        "active": query.product.active,
    }

    warranty = {
        "warranty_id": query.warranty_id,
        "product_id": query.product_id,
        "warranty_months": query.warranty_months,
        "product": product_dict
    }

    return jsonify({"message": "warranty created", "result": warranty}), 201


def get_all_warranties():
    query = db.session.query(Warranties).all()

    warranty_list = []

    for warranty in query:
        product_dict = {
            "product_id": warranty.product.product_id,
            "product_name": warranty.product.product_name,
            "description": warranty.product.description,
            "price": warranty.product.price,
            "active": warranty.product.active,
        }

        warranty_dict = {
            "warranty_id": warranty.warranty_id,
            "product_id": warranty.product_id,
            "warranty_months": warranty.warranty_months,
            "product": product_dict
        }

        warranty_list.append(warranty_dict)

    return jsonify({"message": "warranties found", "results": warranty_list}), 200


def get_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404
    

    product_dict = {
        "product_id": query.product.product_id,
        "product_name": query.product.product_name,
        "description": query.product.description,
        "price": query.product.price,
        "active": query.product.active,
    }

    warranty_dict = {
        "warranty_id": query.warranty_id,
        "product_id": query.product_id,
        "warranty_months": query.warranty_months,
        "product": product_dict
    }


    return jsonify({"message": "warranty found", "result": warranty_dict}), 200


def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404 

    query.warranty_months = post_data.get("warranty_months", query.warranty_months)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "warranty could not be updated"}), 400
    
    updated_warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    product_dict = {
        "product_id": updated_warranty_query.product.product_id,
        "product_name": updated_warranty_query.product.product_name,
        "description": updated_warranty_query.product.description,
        "price": updated_warranty_query.product.price,
        "active": updated_warranty_query.product.active,
    }

    warranty_dict = {
        "warranty_id": updated_warranty_query.warranty_id,
        "product_id": updated_warranty_query.product_id,
        "warranty_months": updated_warranty_query.warranty_months,
        "product": product_dict
    }


    return jsonify({"message": "warranty updated", "result": warranty_dict}), 200


def delete_warranty_by_id(warranty_id):
    query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete warranty"}), 400
    
    return jsonify({"message": "warranty deleted"}), 200