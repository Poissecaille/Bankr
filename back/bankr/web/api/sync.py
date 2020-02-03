from flask import request
from flask_restful import Resource
from bankr.tasks.accounts import retrieve_accounts


class SyncWeboob(Resource):
    def get(self):
        retrieve_accounts().delay()
        return {'msg': 'lauched!'}