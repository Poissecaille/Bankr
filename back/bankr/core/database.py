from peewee import PostgresqlDatabase

from .config import config

db = PostgresqlDatabase(
    'bankr',
    user='bankr',
    password='bankr',
    host=config['database']['host'],
    autorollback=True
)
