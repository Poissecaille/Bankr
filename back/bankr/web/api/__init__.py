from flask import Blueprint
from flask_restful import Api

from bankr.core import db
from .accounts import Accounts
from .. import app

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


@api_bp.before_request
def before_request():
    db.connect(reuse_if_open=True)
    pass


@api_bp.teardown_request
def after_request(exception=None):
    db.close()

api.add_resource(Accounts, '/accounts')

app.register_blueprint(api_bp, url_prefix="/api/v1")
