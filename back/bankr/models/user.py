from peewee import *

from bankr.core import db

from .base_model import BaseModel


class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True)
    password = CharField()

    def get_identity(self):
        return {"id": self.id, "username": self.username}


with db:
    User.create_table(fail_silently=True)
