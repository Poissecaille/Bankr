from peewee import *

from bankr.core import db

from .base_model import BaseModel


class Bank(BaseModel):
    name = CharField(unique=True)


with db:
    Bank.create_table(fail_silently=True)
