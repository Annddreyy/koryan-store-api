from flask import Blueprint, jsonify
from db import get_connection

get_users_blueprint = Blueprint('users', __name__)

@get_users_blueprint.route('/api/v1/users')
def get_users():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM user')

        users = cur.fetchall()
        users_json = []
        for user in users:
            users_json.append(
                {
                    'id': user[0],
                    'password': user[1],
                    'login': user[2],
                    'is_admin': user[3]
                }
            )

        return jsonify(users_json)
    
    except:
        return {
            'status': 'error',
            'code': 500,
            'message': 'Internal server error. Please try again later'
        }
    
    finally:
        cur.close()
        conn.close()


@get_users_blueprint.route('/api/v1/users/<int:user_id>')
def get_one_user(user_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM user WHERE user_id={user_id}')

        user = cur.fetchone()

        if user:
            user_json = {
                    'id': user[0],
                    'password': user[1],
                    'login': user[2],
                    'is_admin': user[3]
                }
            return jsonify(user_json)
            
        return {
            'status': 'error',
            'code': 404,
            'message': f'News with ID {user_id} not found'
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