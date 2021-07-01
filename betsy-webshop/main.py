__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from models import User, Product, Tag, ProductTag, Transaction


def get_products_by_name(term) -> list[Product]:
    query_by_name = Product.name.contains(term)
    query_by_description = Product.description.contains(term)
    query_all_products = Product.select().where(query_by_name | query_by_description)
    return query_all_products


def list_user_products(user_id) -> list[Product]:
    user_products = (
        Product.select()
        .join(User)
        .where(Product.owner == user_id)
        .order_by(Product.id.desc())
    )
    return user_products


# add distinct
def list_products_per_tag(tag_id) -> list[Product]:
    products_with_tag = (
        Product.select().join(ProductTag).join(Tag).where(Tag.id == tag_id)
    )
    return [product for product in products_with_tag]


def add_product_to_catalog(user_id, product) -> None:

    new_product = Product.create(
        name=product["name"],
        price_per_unit=product["price_per_unit"],
        stock=product["stock"],
        description=product["description"],
        owner=user_id,
    )
    return new_product


def update_stock(product_id, new_quantity) -> None:
    product = Product.get_by_id(product_id)
    product.stock = new_quantity
    product.save()


# moet zorgen dat je niet van jezelf kunt kopen...
def purchase_product(product_id, buyer_id, quantity) -> None:
    product = Product.get_by_id(product_id)
    new_quantity = product.stock - quantity
    if product.stock < quantity:
        raise ValueError("Amount not available in stock")
    Transaction.create(buyer=buyer_id, product_bought=product_id, amount=quantity)
    update_stock(product_id, new_quantity)


# non assignment functions


def get_words_in_string(string) -> list:
    """
    Takes in string of words, removes all duplicates, whitespace, non-alpha characters and
    words containing non-alpha characters.
    Separate the words by space and retuns list of strings in all lowerscase.
    """
    words_list = " ".join(string.split()).split()
    return list(set([word.lower() for word in words_list if word.isalpha()]))


def get_tags_per_product(product_id):
    tags_per_product = (
        Tag.select().join(ProductTag).join(Product).where(Product.id == product_id)
    )
    return [tag.name for tag in tags_per_product]


def get_alpha_tag() -> list[Tag]:
    tags = Tag.select().order_by(Tag.name)
    return [tag for tag in tags]


def get_alpha_tag_names() -> tuple[Tag]:
    """
    Returns a list of tuples (Tag.name, Tag.name)
    With an additional tuple containing (None, "Choose")
    Used to dynamically determine available tags for the selectfield in the searchbar.
    """
    tags = Tag.select().order_by(Tag.name)
    tag_list = [(tag.name, tag.name) for tag in tags]
    tag_list.insert(0, (None, "Categories..."))
    return tag_list


def create_producttags(product_model, tag_list):
    for tag in tag_list:
        added_tag = Tag.get_or_create(name=tag)
        ProductTag.create(
            product=Product.get_by_id(product_model), tag=Tag.get_by_id(added_tag[0].id)
        )
