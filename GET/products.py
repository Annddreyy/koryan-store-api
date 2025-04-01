from flask import Blueprint, jsonify
from db import get_connection

get_products_blueprint = Blueprint('products', __name__)

@get_products_blueprint.route('/api/v1/products')
def get_products():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()


        cur.execute('SELECT * FROM product')

        products = cur.fetchall()
        products_json = []
        for product in products:
            cur.execute(f'SELECT * FROM discount WHERE product_id={product[0]}')
            discount = cur.fetchone()

            cur.execute(f'SELECT * FROM popular WHERE product_id={product[0]}')
            popular = cur.fetchone()

            cur.execute(f'SELECT * FROM new_product WHERE product_id={product[0]}')
            new_product = cur.fetchone()

            signature = ''
            new_price = ''
            if discount:
                signature = 'discount'
                new_price = discount[2]
            elif popular:
                signature = 'popular'
            elif new_product:
                signature = 'new_product'

            cur.execute(f'SELECT title FROM product_type WHERE product_type_id={product[9]}')
            product_type = cur.fetchone()

            products_json.append(
                {
                    'id': product[0],
                    'title': product[1],
                    'producer': product[2],
                    'year': product[3],
                    'short_description': product[4],
                    'description': product[5],
                    'price': product[6],
                    'amount': product[7],
                    'img_path': product[8],
                    'signature': signature,
                    'new_price': new_price,
                    'product_type': product_type[0]
                }
            )

        return jsonify(products_json)
    
    except:
        return {
            'status': 'error',
            'code': 500,
            'message': 'Internal server error. Please try again later'
        }
    
    finally:
        cur.close()
        conn.close()


@get_products_blueprint.route('/api/v1/products/<int:product_id>')
def get_one_product(product_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM product WHERE product_id={product_id}')

        product = cur.fetchone()

        if product:
            product_json = {
                    'id': product[0],
                    'title': product[1],
                    'producer': product[2],
                    'year': product[3],
                    'short_description': product[4],
                    'description': product[5],
                    'price': product[6],
                    'amount': product[7],
                    'img_path': product[8]
                }
            return jsonify(product_json)
            
        return {
            'status': 'error',
            'code': 404,
            'message': f'News with ID {product_id} not found'
        }
    
    except:
        return {
            'status': 'error',
            'code': 500,
            'message': 'Internal server error. Please try again later'
        }
    
    finally:
        cur.close()
        conn.close()