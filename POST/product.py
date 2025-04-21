from flask import Blueprint, request
from db import get_connection
import hashlib
import base64

post_product_blueprint = Blueprint('post_product', __name__)

@post_product_blueprint.route('/api/v1/product', methods=['POST'])
def post_user():
    conn = get_connection()
    cur = conn.cursor()
    try:

        product = request.get_json()

        title = product['title']
        short_description = product['short-description']
        year = product['year']
        description = product['description']
        price = product['price']
        amount = product['amount']
        producer = product['producer']
        main_image = product['main-image']
        mini_image = product['mini-image']

        main_image = create_image(main_image, 'product/', '.png')

        cur.execute('INSERT INTO product(title, producer, year, short_description, ' \
        'description, price, amount, img_path) ' +
        f"VALUES('{title}', '{producer}', {year}, \
        '{short_description}', '{description}', {price}, \
        {amount}, '{main_image}')")
        
        print('ok')
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

def create_image(image_path, folder, file_type):
    image_bytes = bytes(image_path)

    github_token = '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'

    g = Github(github_token)

    repo = g.get_user().get_repo('koreyan-store-images')
    file_name = generate_random_filename(16) + file_type
    repo.create_file(folder + file_name, 'Add file', image_bytes)

    return file_name

def generate_random_filename(length=16):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))