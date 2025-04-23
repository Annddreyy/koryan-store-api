from flask import Blueprint, request
from db import get_connection
import hashlib
import base64
import requests
import string
import random

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
        product_type_id = product['product_type']

        main_image = create_image(main_image, 'product/', '.png')

        cur.execute('INSERT INTO product(title, producer, year, short_description, description, price, amount, img_path, product_type_id) ' +
        f"VALUES('{title}', '{producer}', {year}, '{short_description}', '{description}', {price}, {amount}, '{main_image}', {product_type_id})")
        conn.commit()

        cur.execute(f"SELECT product_id FROM product ORDER BY product_id DESC LIMIT 1")
        product_id = int(cur.fetchone()[0])

        for i in range(len(mini_image)):
            print(mini_image[i])
            main_image = create_image(mini_image[i], 'product/', '.png')
            cur.execute('INSERT INTO product_image(product_id, image_path) ' +
            f"VALUES({product_id}, '{main_image}')")
            conn.commit()
        
        return {
        'status': 'ok',
        'id': product_id
    }

    finally:
        cur.close()
        conn.close()


def create_image(base64_image, folder, file_type):
    image_bytes = base64.b64decode(base64_image)

    github_token = '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'
    repo_owner = 'Annddreyy'
    repo_name = 'koreyan-store-images'

    file_name = generate_random_filename(16) + file_type
    path_in_repo = folder + file_name

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path_in_repo}'
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    content_base64 = base64.b64encode(image_bytes).decode('utf-8')

    payload = {
        'message': 'Add image via API',
        'content': content_base64
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code not in (200, 201):
        raise Exception(f'GitHub API error: {response.status_code} - {response.text}')

    return file_name

def generate_random_filename(length=16):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))