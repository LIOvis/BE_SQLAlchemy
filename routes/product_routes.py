from flask import Blueprint

import controllers

product = Blueprint('product', __name__)

@product.route('/product', methods=["POST"])
def add_product_route():
    return controllers.add_product()

@product.route('/products', methods=["GET"])
def get_all_products_route():
    return controllers.get_all_products()

@product.route('/product/category', methods=["POST"])
def add_product_to_category_route():
    return controllers.add_product_to_category()