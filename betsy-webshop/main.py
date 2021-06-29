__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from models import User, Product, Tag, ProductTag, Transaction


def get_products_by_name(term) -> list[Product]:
    query_by_name = Product.name.contains(term)
    query_by_description = Product.description.contains(term)
    query_all_products = Product.select().where(query_by_name | query_by_description)
    return query_all_products


def list_user_products(user_id) -> list[User.products]:
    user_products = Product.select().join(User).where(Product.owner == user_id)
    return [product for product in user_products]


# add distinct
def list_products_per_tag(tag_id) -> list[Product.name]:
    products_with_tag = (
        Product.select().join(ProductTag).join(Tag).where(Tag.id == tag_id)
    )
    return [product.name for product in products_with_tag]


def add_product_to_catalog(user_id, product) -> None:
    user = User.get_by_id(user_id)
    Product.create(name=product, owner=user)


def update_stock(product_id, new_quantity) -> None:
    product = Product.get_by_id(product_id)
    product.stock = new_quantity
    product.save()


# moet zorgen dat je niet van jezelf kunt kopen...
def purchase_product(product_id, buyer_id, quantity) -> None:
    product = Product.get_by_id(product_id)
    if product.stock < quantity:
        raise ValueError("Amount not available in stock")
    Transaction.create(buyer=buyer_id, product_bought=product_id, amount=quantity)
    product.stock -= quantity
    product.save()


def remove_product(product_id) -> None:
    Product.delete().where(Product.id == product_id).execute()


# non assignment functions


def get_words_in_string(string) -> list:
    """
    Takes in string of words, removes all duplicates, whitespace, non-alpha characters and
    words containing non-alpha characters.
    Returns the words in all lowerscase as list
    """
    words_list = " ".join(string.split()).split()
    # add in removes duplicates
    return list(set([word.lower() for word in words_list if word.isalpha()]))


def get_tags_per_product(product_id):
    tags_per_product = (
        Tag.select().join(ProductTag).join(Product).where(Product.id == product_id)
    )
    return [tag.name for tag in tags_per_product]
