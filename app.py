from flask import Flask
from flask_cors import CORS

from GET.products import get_products_blueprint


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] = '12foefwjf039423wd2808d'

app.register_blueprint(get_products_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
