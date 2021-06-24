from peewee import (
    CharField,
    Check,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    DateField,
)
from datetime import datetime

db = SqliteDatabase("betsy.db", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


# add constraints to all models


class User(BaseModel):
    name = CharField(index=True, max_length=30)
    # last_name = CharField(max_length=120)
    # address = CharField(max_length=200)
    # city = CharField(max_length=50)
    # country = CharField(max_length=50)
    # cc_number = CharField(unique=True, max_length=20)  # uuid field??
    # username = CharField(index=True, max_length=30, default=first_name)
    # email = CharField(index=True, max_length=380, unique=True)
    # password = CharField(max_length=20)


class Product(BaseModel):
    name = CharField(max_length=50)
    description = TextField(null=True)
    price_per_unit = DecimalField(
        constraints=[Check("price_per_unit >= 0")],
        decimal_places=2,
        auto_round=True,
        null=True,  # null=True, als je gratis iets aanbiedt.
        default=0,
        max_digits=10,
    )
    stock = IntegerField(default=1)
    owner = ForeignKeyField(User, backref="products")
    date_posted = DateField(formats="%Y-%m-%d", default=datetime.utcnow())


Product.add_index(Product.name, Product.description)


class Tag(BaseModel):
    name = CharField(unique=True, max_length=30)


# moet zorgen dat je niet dezelfde producttags kunt maken. add distinct in query
class ProductTags(BaseModel):
    product = ForeignKeyField(Product, index=True, backref="tags")
    tag = ForeignKeyField(Tag, index=True, backref="products")


class Transaction(BaseModel):
    buyer = ForeignKeyField(User, backref="transactions", index=True)
    product_bought = ForeignKeyField(Product, index=True)
    amount = IntegerField()  # quantity bought ipv sold
    transaction_date = DateField(formats="%Y-%m-%d %H:%M", default=datetime.utcnow())


db.connect()
db.create_tables([User, Product, Tag, ProductTags, Transaction])
# data = [
#     {'facid': 9, 'name': 'Spa', 'membercost': 20, 'guestcost': 30,
#      'initialoutlay': 100000, 'monthlymaintenance': 800},
#     {'facid': 10, 'name': 'Squash Court 2', 'membercost': 3.5,
#      'guestcost': 17.5, 'initialoutlay': 5000, 'monthlymaintenance': 80}]
# res = Facility.insert_many(data).execute()

# with db.atomic():
#     MyModel.insert_many(data, fields=fields).execute()