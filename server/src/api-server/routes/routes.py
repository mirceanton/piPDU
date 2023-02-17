from flask import Blueprint
from routes.v1.v1 import v1_blueprint

api_blueprint = Blueprint('api', __name__)
api_blueprint.register_blueprint(v1_blueprint, url_prefix="/v1")
