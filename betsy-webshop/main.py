__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import User, Product, Tag, ProductTags, Transaction

"""


-Search for products based on a term. Searching for 'sweater' should yield all products that have the word 'sweater' in the name. This search should be case-insensitive

-Handle a purchase between a buyer and a seller for a given product"""


def search(term):
    ...


def list_user_products(user_id) -> list[User.products]:
    user_products = Product.select().join(User).where(Product.owner == user_id)
    return [product.name for product in user_products]


def list_products_per_tag(tag_id) -> list[Tag.name]:
    products_with_tag = (
        Product.select().join(ProductTags).join(Tag).where(Tag.id == tag_id)
    )
    return [product.name for product in products_with_tag]


def add_product_to_catalog(user_id, product) -> None:
    user = User.get_by_id(user_id)
    Product.create(name=product, owner=user)


def update_stock(product_id, new_quantity) -> None:
    product = Product.get_by_id(product_id)
    product.quantity_in_stock = new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):
    ...


def remove_product(product_id):
    Product.delete().where(Product.id == product_id).execute()
