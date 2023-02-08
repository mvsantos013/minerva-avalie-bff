import traceback
from flask import Flask, jsonify, request as req
from flask_cors import CORS
from src.lib.utils import JSONEncoder
from src.app.departments import controller as departments_controller
from src.app.professors import controller as professors_controller
from src.app.testimonials import controller as testimonials_controller
from src.app.auth.groups import controller as groups_controller
from src.app.auth.permissions import controller as permissions_controller
from src.app.ratings import controller as ratings_controller

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.json_encoder = JSONEncoder

# Register routes
app.register_blueprint(groups_controller.blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(permissions_controller.blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(departments_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(professors_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(testimonials_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(ratings_controller.blueprint, url_prefix='/api/v1')

# Returns a error in a standard way if endpoint crashes.
@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return jsonify({'error': str(e)}), 500


# Ignore this route
@app.route('/favicon.ico')
def favicon():
    return ''
