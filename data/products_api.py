import flask
from flask import jsonify

from data import db_session
from data.product import Product

blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/product')
def get_news():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    return jsonify(
        {
            'products':
                [item.to_dict(only=('name', 'price', 'about'))
                 for item in products]
        }
    )


@blueprint.route('/api/product/<int:product_id>', methods=['GET'])
def get_one_news(product_id):
    db_sess = db_session.create_session()
    products = db_sess.query(Product).get(product_id)
    if not products:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'products': products.to_dict(only=(
                'name', 'price', 'about'))
        }
    )

