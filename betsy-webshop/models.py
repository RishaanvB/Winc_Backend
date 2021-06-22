from peewee import (
    CharField,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)
from peewee import *

db = SqliteDatabase("betsy.db")


class BaseModel(Model):
    class Meta:
        database = db


# add constraints to all models


class User(BaseModel):
    first_name = CharField()
    # last_name = CharField()
    # address = CharField()
    # city = CharField()
    # country = CharField()
    # cc_number = CharField(unique=True)  # mss hashen? ivm privacy? :)


class Product(BaseModel):
    name = CharField()
    # description = TextField()
    price_per_unit = DecimalField(decimal_places=2, auto_round=True, default=10.50)
    quantity_in_stock = IntegerField(default=10)
    owner = ForeignKeyField(User, backref="products")


class Tag(BaseModel):
    name = CharField(unique=True)


class ProductTags(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref="transactions")
    purchased_product = ForeignKeyField(Product, backref="transactions")
    quantity_sold = IntegerField()


# initialize db