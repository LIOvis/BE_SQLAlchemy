from flask import request, jsonify

from models.category import Categories
from db import db

def add_category():
    post_data = request.form if request.form else request.json

    fields = ['category_name']
    required_fields = ['category_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 404
        
        values[field] = field_data

    new_category = Categories(values['category_name'])

    try:
        db.session.add(new_category)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()

    category = {
        "category_id": query.category_id,
        "category_name": query.category_name
    }

    return jsonify({"message": "category created", "results": category}), 201

def get_all_categories():
    query = db.session.query(Categories).all()

    category_list = []

    for category in query:
        category_dict = {
            "category_id": category.category_id,
            "category_name": category.category_name
        }

        category_list.append(category_dict)

    return jsonify({"message": "category found", "results": category_list}), 200


def get_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category not found"}), 404
    
    category = {
        "category_id": query.category_id, "category_name": query.category_name
    }
    
    return jsonify({"message": "category found", "result": category}), 200

def update_category_by_id(category_id):
    post_data = request.form if request.form else request.json
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    query.category_name = post_data.get("category_name", query.category_name)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "category could not be updated"}), 400
    
    updated_category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    category = {
        "category_id": updated_category_query.category_id,
        "category_name": updated_category_query.category_name
    }

    return jsonify({"message": "category updated", "result": category}), 200

def delete_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category not found"}), 404
    
    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete category"}), 400
    
    return jsonify({"message": "category deleted"}), 200
