from peewee import *

from bankr.core import db

from .base_model import BaseModel


class Category(BaseModel):
    label = CharField()


with db:
    Category.create_table(fail_silently=True)