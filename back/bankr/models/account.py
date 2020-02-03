from peewee import *

from bankr.core import db

from .base_model import BaseModel
from .user import User
from .bank import Bank


class Account(BaseModel):
    bank = ForeignKeyField(Bank)
    account_id = CharField()
    user = ForeignKeyField(User)
    label = CharField()
    balance = FloatField()


with db:
    Account.create_table(fail_silently=True)
