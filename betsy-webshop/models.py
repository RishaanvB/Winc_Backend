from peewee import (
    CharField,
    Check,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    SQL,
)


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
    stock = IntegerField(default=10)
    owner = ForeignKeyField(User, backref="products")


class Tag(BaseModel):
    name = CharField(unique=True)


class ProductTags(BaseModel):
    product = ForeignKeyField(Product)
    tag = ForeignKeyField(Tag)


class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref="transactions")
    product_bought = ForeignKeyField(Product, backref="transactions")
    amount = IntegerField()  # quantity bought ipv sold

    # class Meta:
    #     constraints = [SQL(" FOREIGN KEY(product_bought), CHECK(product(stock) > 0) ")]


# initialize db

db.connect()
db.create_tables([User, Product, Transaction])