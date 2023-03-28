import json
import traceback
from flask import Flask, jsonify, request as req
from flask_cors import CORS
from flasgger import Swagger
from src.lib.jwt_verifier import validate_jwt_token
from src.lib.utils import JSONEncoder
from src.app.auth.groups import controller as groups_controller
from src.app.auth.permissions import controller as permissions_controller
from src.app.organizations import controller as organizations_controller
from src.app.departments import controller as departments_controller
from src.app.professors import controller as professors_controller
from src.app.professors.testimonials import controller as testimonials_controller
from src.app.professors.ratings import controller as ratings_controller

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.json_encoder = JSONEncoder

# Register routes
app.register_blueprint(groups_controller.blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(permissions_controller.blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(organizations_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(departments_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(professors_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(testimonials_controller.blueprint, url_prefix='/api/v1')
app.register_blueprint(ratings_controller.blueprint, url_prefix='/api/v1')

# Load user details into request object
@app.before_request
def set_user():
    try:
        bearer_token = req.headers.get('Authorization')
        if(bearer_token is None):
            req.user = None
            return

        req.user = {}
        claims, user_data = validate_jwt_token(bearer_token)
        claims['token'] = bearer_token.replace('Bearer ', '')
        claims['id'] = claims['sub']
        claims['name'] = claims['name'] if 'name' in claims else claims['email'].split('@')[0]
        claims['email'] = claims['email']
        claims['groups'] = user_data.get('groups', [])
        claims['permissions'] = user_data.get('permissions', [])
        req.user = claims
    except Exception as e:
        pass

# Returns a error in a standard way if endpoint crashes.
@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return jsonify({'error': str(e)}), 500


# Ignore this route
@app.route('/favicon.ico')
def favicon():
    return ''


app.config['SWAGGER'] = {
    'title': 'Minerva Avalie API Documentation',
    'description': '',
    'termsOfService': '',
    'uiversion': 1,
}

swagger = Swagger(
    app,
    config={
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
            ('Access-Control-Allow-Credentials', "true"),
            ('Access-Control-Allow-Headers', "Content-Type, Authorization, X-Requested-With, Accept"),
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": f'/api/docs/specs.json',
            }
        ],
        "swagger_ui": False,
    },
)

BASE_HTML = '''
<!DOCTYPE html>
<html>
<link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.12.1/swagger-ui.css">
<style>body{margin:0}.swagger-ui .topbar{background-color:#635c5c}.topbar-wrapper a span{display:none}.topbar-wrapper a:after{content:'Minerva Avalie';margin-left:1rem}.swagger-ui .topbar .download-url-wrapper input[type=text]{border:solid 2px #82b5ed}.swagger-ui .topbar .download-url-wrapper .download-url-button{background:#82b5ed}.scheme-container{display:none}#operations-tag-default{display:none}</style>
<head>
    <title>Minerva Avalie API Documentation</title>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@3.12.1/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@3.12.1/swagger-ui-standalone-preset.js"></script>
    <script>window.onload=function(){const e=SwaggerUIBundle({spec:%SPEC%,dom_id:"#swagger-ui",presets:[SwaggerUIBundle.presets.apis,SwaggerUIStandalonePreset],layout:"StandaloneLayout"});window.ui=e};</script>
</head>
<body>
</body>
</html>
'''

# Docs endpoint
@app.route('/api/docs', methods=['GET'])
def docs():
    with swagger.app.app_context():
        specs = swagger.get_apispecs()
    base_url = req.base_url.replace('/api/docs', '')
    specs['host'] = base_url.split('//')[1]
    html = BASE_HTML.replace('BASEURL', base_url).replace('%SPEC%', json.dumps(specs))
    return html