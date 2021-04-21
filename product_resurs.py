from flask_restful import Resource, reqparse, abort
from flask import jsonify
from data import db_session
from data.product import Product


def abort_if_news_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")


class ProductResource(Resource):
    def get(self, product_id):
        abort_if_news_not_found(product_id)
        session = db_session.create_session()
        products = session.query(Product).get(product_id)
        return jsonify({'products': products.to_dict(
            only=('name', 'price', 'about'))})


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('price', required=True)


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        products = session.query(Product).all()
        return jsonify({'products': [item.to_dict(
            only=('name', 'price', 'about')) for item in products]})
