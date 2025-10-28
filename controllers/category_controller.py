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