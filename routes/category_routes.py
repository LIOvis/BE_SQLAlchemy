from flask import Blueprint

import controllers

category = Blueprint("category", __name__)

@category.route('/category', methods=["POST"])
def add_category_route():
    return controllers.add_category()