__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from models import User, Product, Tag, ProductTag, Transaction
from flask import abort


def get_products_by_name(term) -> Product:
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


def get_products_per_tag(tag_name) -> Product:
    products_with_tag = (
        Product.select()
        .join(ProductTag)
        .join(Tag)
        .distinct()
        .where(Tag.name == tag_name)
    )
    return products_with_tag


def add_product_to_catalog(user_id, product) -> Product:

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
    seller_id = product.owner.id
    validate_product_purchase(
        product=product, buyer_id=buyer_id, seller_id=seller_id, quantity=quantity
    )

    new_quantity = product.stock - quantity
    Transaction.create(
        buyer=buyer_id, product_bought=product_id, amount_bought=quantity
    )
    update_stock(product_id, new_quantity)


# non assignment functions


def get_unique_words_in_string(string) -> list:
    """
    Takes in string, removes all duplicates, whitespace, non-alpha characters and
    words containing non-alpha characters.
    Separate the words by space and retuns list of strings in all lowercase.
    """
    words_list = " ".join(string.split()).split()
    return list(set([word.lower() for word in words_list if word.isalpha()]))


def get_tags_per_product(product_id) -> list[Tag.name]:
    tags_per_product = (
        Tag.select().join(ProductTag).join(Product).where(Product.id == product_id)
    )
    return [tag.name for tag in tags_per_product]


def get_alpha_tag() -> list[Tag]:
    tags = Tag.select().order_by(Tag.name)
    return [tag for tag in tags]


def get_tagnames() -> list:
    tags = Tag.select()
    return [tag.name for tag in tags]


def get_alpha_tag_names() -> tuple[Tag]:
    """
    Returns a list of tuples (Tag.name, Tag.name)
    With an additional tuple containing (None, "Choose")
    Used to dynamically determine available tags for the selectfield in the searchbar.
    """
    tags = Tag.select().order_by(Tag.name)
    tag_list = [(tag.name, tag.name) for tag in tags]
    tag_list.insert(0, ("All", "All Categories"))
    return tag_list


def create_tag_from_list(tag_list):
    for tag in tag_list:
        Tag.create(name=tag)


def create_producttags(product_id, tag_list) -> None:
    for tag in tag_list:
        added_tag = Tag.get(name=tag)
        ProductTag.create(product=product_id, tag_id=added_tag.id)
    return


def delete_producttags_from_product(product_id):
    ProductTag.delete().where(ProductTag.product.id == product_id).execute()


def validate_product_purchase(seller_id, buyer_id, product, quantity):
    if seller_id == buyer_id:
        abort(403, "You trying to buy your own stuff???")

    if product.stock < quantity:
        abort(
            404,
            "The amount you tried to buy does not exist. I should just disable the buy button. Since these errors are not very userfriendly.",
        )


def check_tags_in_list(tag_list, product_taglist):
    """
    Sorts both listed alphabetically, then compares items in each list
    and returns a string with the index of the identical items found in both lists
    in the form of 'tags-index'. Used for enabling checked attribute in update_product_form
    """
    duplicated_items = []
    tag_list = sorted(tag_list)
    product_taglist = sorted(product_taglist)
    for index, tag in enumerate(tag_list):
        if tag in product_taglist:
            duplicated_items.append(f"tags-{index}")
    return duplicated_items


# from app import db
# from models import User, Product, Tag, ProductTag
# from main import create_producttags