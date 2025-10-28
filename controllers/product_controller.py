from flask import request, jsonify

from models.category import Categories
from models.product import Products
from db import db

def add_product():
    post_data = request.form if request.form else request.json

    fields = ['company_id', 'product_name', 'description', 'price', 'active']
    required_fields = ['company_id', 'product_name', 'price']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 404
        
        values[field] = field_data

    new_product = Products(values['company_id'], values['product_name'], values['description'], values['price'], values['active'])

    try:
        db.session.add(new_product)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    
    query = db.session.query(Products).filter(Products.product_name == values['product_name']).first()

    company_dict = {
        "company_id": query.company.company_id,
        "company_name": query.company.company_name
    }
    
    categories_list = []

    for category in query.categories:
        category_dict = {
            "category_id": category.category_id,
            "category_name": category.category_name
        }

        categories_list.append(category_dict)

    if query.warranty:
        warranty_dict = {
            "warranty_id": query.warranty.warranty_id,
            "warranty_months": query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    product = {
        "product_id":
        query.product_id,
        "product_name":
        query.product_name,
        "description": query.description,
        "price": query.price,
        "active": query.active,
        "company": company_dict,
        "categories": categories_list,
        "warranty": warranty_dict
    }

    return jsonify({"message": "product created", "result": product}), 201


def get_all_products():
    query = db.session.query(Products).all()

    product_list = []

    for product in query:
        company_dict = {
        "company_id": product.company.company_id,
        "company_name": product.company.company_name
        }
    
        categories_list = []

        for category in product.categories:
            category_dict = {
                "category_id": category.category_id,
                "category_name": category.category_name
            }

            categories_list.append(category_dict)

        if product.warranty:
            warranty_dict = {
                "warranty_id": product.warranty.warranty_id,
                "warranty_months": product.warranty.warranty_months
            }
        else:
            warranty_dict = {}

        product_dict = {
            "product_id":
            product.product_id,
            "product_name":
            product.product_name,
            "description": product.description,
            "price": product.price,
            "active": product.active,
            "company": company_dict,
            "categories": categories_list,
            "warranty": warranty_dict
        }

        product_list.append(product_dict)

    return jsonify({"message": "products found", "results": product_list}), 200


def add_product_to_category():
    post_data = request.form if request.form else request.json

    fields = ['product_id', 'category_id']
    required_fields = ['product_id', 'category_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 404
        
        values[field] = field_data

    product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

    if product_query and category_query:
        product_query.categories.append(category_query)

        db.session.commit()
        
        company_dict = {
        "company_id": product_query.company.company_id,
        "company_name": product_query.company.company_name
        }
    
        categories_list = []

        for category in product_query.categories:
            category_dict = {
                "category_id": category.category_id,
                "category_name": category.category_name
            }

            categories_list.append(category_dict)

        product_dict = {
            "product_id":
            product_query.product_id,
            "product_name":
            product_query.product_name,
            "description": product_query.description,
            "price": product_query.price,
            "active": product_query.active,
            "company": company_dict,
            "categories": categories_list,
        }

    return jsonify({"message": "product added to category", "results": product_dict}), 200
