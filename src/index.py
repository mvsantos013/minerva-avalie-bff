import traceback
import jwt
import json
from flask import Flask, jsonify, request as req
from flask_cors import CORS
from src.app.professors import controller as professors_controller

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False


# Register routes
app.register_blueprint(professors_controller.blueprint, url_prefix='/api/v1')

# # Load user into request for every endpoint
# @app.before_request
# def set_user():
#     try:
#         req.user = {}
#         token = req.headers.get('Authorization').replace('Bearer ', '')
#         # Authorization token was already validated by API Gateway authorizer
#         user = jwt.decode(token, options={"verify_signature": False})
#         user_data = json.loads(user['userData'])
#         user['token'] = token
#         user['id'] = user['sub']
#         user['name'] = user['name'] if 'name' in user else user['email'].split('@')[0]
#         user['email'] = user['email']
#         user['groups'] = user_data['groups']
#         user['permissions'] = user_data['permissions']
#         req.user = user
#     except Exception as e:
#         pass


# Returns a error in a standard way if endpoint crashes.
@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return jsonify({'error': str(e)}), 500


# Ignore this route
@app.route('/favicon.ico')
def favicon():
    return ''
