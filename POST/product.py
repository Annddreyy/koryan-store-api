from flask import Blueprint, request
from db import get_connection
import hashlib

def sha256_hash(message):
    message = message.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(message)
    hash_code = sha256.hexdigest()
    return hash_code


post_product_blueprint = Blueprint('post_product', __name__)

@post_product_blueprint.route('/api/v1/product', methods=['POST'])
def post_user():
    try:
        conn = get_connection()
        cur = conn.cursor()

        product = request.get_json()

        title = product['title']
        short_description = product['short-description']
        year = product['year']
        description = product['description']
        price = product['price']
        amount = product['amount']
        main_image = product['main-image']
        producer = product['producer']

        cur.execute('INSERT INTO user(title, producer, year, short-description, ' \
        'description, price, amount, img_path) ' +
        f"VALUES('{title}', '{producer}', {year}, \
        '{short_description}', '{description}', {price}, \
        {amount}, '{main_image}')")
                    
        conn.commit()

        cur.execute(f"SELECT product_id FROM product ORDER BY product_id DESC LIMIT 1")
        product_id = int(cur.fetchone()[0])

        return {
            'status': 'ok',
            'id': product_id
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    finally:
        cur.close()
        conn.close()

