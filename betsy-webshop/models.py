# importing db for access to actual peewee database and db_wrapper to access Model

from enum import unique
from flask_login.mixins import UserMixin
from app import db_wrapper, db
from datetime import datetime

from peewee import (
    CharField,
    Check,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    DateTimeField,
)


class BaseModel(db_wrapper.Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    first_name = CharField(index=True, max_length=30, null=True)
    last_name = CharField(max_length=120, null=True)
    address = CharField(max_length=200, null=True)
    city = CharField(max_length=50, null=True)
    country = CharField(max_length=50, null=True)
    cc_number = IntegerField(unique=True, null=True)
    username = CharField(index=True, max_length=30, unique=True)
    email = CharField(index=True, max_length=50, unique=True)
    password = CharField(max_length=20)


class Product(BaseModel):
    name = CharField(max_length=50)
    description = TextField(null=True)
    price_per_unit = DecimalField(
        constraints=[Check("price_per_unit >= 0")],
        decimal_places=2,
        auto_round=True,
        null=True,
        default=0,
        max_digits=10,
    )
    stock = IntegerField(default=1)
    owner = ForeignKeyField(User, backref="products")
    date_posted = DateTimeField(formats="%Y-%m-%d", default=datetime.utcnow())


Product.add_index(Product.name, Product.description)


class Tag(BaseModel):
    name = CharField(unique=True, max_length=30)


# moet zorgen dat je niet dezelfde producttags kunt maken. add distinct in query
# rename singular?--> ProductTag hoeft niet, gewoon vantevoren tags erin gooien.
class ProductTag(BaseModel):
    product = ForeignKeyField(Product, index=True, backref="tags")
    tag = ForeignKeyField(Tag, index=True, backref="products")


class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref="transactions", index=True)
    product_bought = ForeignKeyField(Product, index=True)
    amount_bought = IntegerField()
    transaction_date = DateTimeField(
        formats="%Y-%m-%d %H:%M", default=datetime.utcnow()
    )


# db.connect()
# db.create_tables([User, Product, Tag, ProductTags, Transaction])
