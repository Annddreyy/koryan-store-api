from flask import Blueprint, jsonify
from db import get_connection

get_product_images_blueprint = Blueprint('product_images', __name__)

@get_product_images_blueprint.route('/api/v1/product/images/<int:product_id>')
def get_products(product_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT image_path FROM product_image WHERE product_id={product_id}')
    products = cur.fetchall()
    products_json = []
    for product in products:
        products_json.append(
            {
                'img': product[0],
            }
        )
    return jsonify(products_json)
    
    return {
        'status': 'error',
        'code': 500,
        'message': str(ex)
    }

    cur.close()
    conn.close()