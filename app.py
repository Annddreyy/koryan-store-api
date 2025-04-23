from flask import Flask
from flask_cors import CORS

from GET.products import get_products_blueprint
from GET.users import get_users_blueprint
from GET.product_images import get_product_images_blueprint

from POST.user import post_user_blueprint
from POST.product import post_product_blueprint


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config['SECRET_KEY'] = '12foefwjf039423wd2808d'

app.register_blueprint(get_products_blueprint)
app.register_blueprint(get_users_blueprint)
app.register_blueprint(get_product_images_blueprint)

app.register_blueprint(post_user_blueprint)
app.register_blueprint(post_product_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
