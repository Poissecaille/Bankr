from peewee import Model, AutoField
from playhouse.shortcuts import model_to_dict

from bankr.core import db


class BaseModel(Model):
    id = AutoField()

    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
