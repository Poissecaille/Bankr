from peewee import *

from bankr.core import db

from .base_model import BaseModel
from .account import Account
from .category import Category


class Transaction(BaseModel):
    account = ForeignKeyField(Account)
    label = CharField()
    amount = FloatField()
    seen = CharField

    def get_small_data(self):
        return {'id': self.id, 'account': self.account.label, 'bank': self.account.bank.name, 'label': self.label,
                'amount': self.amount}


with db:
    Transaction.create_table(fail_silently=True)
