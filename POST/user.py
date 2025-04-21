from flask import Blueprint, request
from db import get_connection
import hashlib

def sha256_hash(message):
    message = message.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(message)
    hash_code = sha256.hexdigest()
    return hash_code


post_user_blueprint = Blueprint('post_user', __name__)

@post_user_blueprint.route('/api/v1/users', methods=['POST'])
def post_user():
    conn = get_connection()
    cur = conn.cursor()
    try:
    

        user = request.get_json()

        login = user['login']
        password = user['password']

        password = sha256_hash(password)

        cur.execute('INSERT INTO user(login, password, is_admin) ' +
                    f"VALUES('{login}', '{password}', 0)")
                    
        conn.commit()

        cur.execute(f"SELECT user_id FROM user WHERE login='{login}' AND password='{password}'")
        user_id = int(cur.fetchone()[0])

        return {
            'status': 'ok',
            'id': user_id
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
    finally:
        cur.close()
        conn.close()

