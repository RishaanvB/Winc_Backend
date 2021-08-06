__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


from models import User, Product, Tag, ProductTag, Transaction
from flask import abort
from urllib.parse import urlparse, urljoin
from flask import request


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


def purchase_product(product_id, buyer_id, quantity) -> None:
    product = Product.get_by_id(product_id)
    new_quantity = product.stock - quantity
    Transaction.create(
        buyer=buyer_id, product_bought=product_id, amount_bought=quantity
    )
    update_stock(product_id, new_quantity)


# non assignment functions


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
    delete_query = (
        ProductTag.select().join(Product).where(ProductTag.product.id == product_id)
    )
    for query in delete_query:
        query.delete_instance()


def check_tags_in_list(tag_list, part_of_tag_list):
    """
    Sorts both lists alphabetically, then compares items in each list
    and returns a string with the index of the identical items found in the first list
    in the form of 'tags-index'. Used for enabling checked attribute in update_product_page.html
    """
    duplicated_items = []
    tag_list = sorted(tag_list)
    part_of_tag_list = sorted(part_of_tag_list)
    for index, tag in enumerate(tag_list):
        if tag in part_of_tag_list:
            duplicated_items.append(f"update-product-tags-{index}")
    return duplicated_items


def delete_product_by_id(product_id):
    product = Product.get(product_id)
    product.delete_instance(recursive=True, delete_nullable=True)


def delete_all_products_from_user(user_id):
    for product in list_user_products(user_id):
        delete_product_by_id(product.id)


def delete_user(user_id):
    user = User.get(user_id)
    user.delete_instance(recursive=True, delete_nullable=True)


def get_user_sold_transactions(user_id) -> list[Transaction]:
    transactions = (
        Transaction.select()
        .join(Product)
        .join(User)
        .where(Transaction.product_bought.owner.id == user_id)
    )
    return [transaction for transaction in transactions]


def get_user_bought_transactions(user_id) -> list[Transaction]:
    transactions = (
        Transaction.select().join(User).where(Transaction.buyer.id == user_id)
    )
    return [transaction for transaction in transactions]


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


# def validate_price_per_unit(self, price_per_unit):
#     if price_per_unit.data is not None and price_per_unit.data < 0:
#         raise ValidationError(
#             "You want them to pay YOU?? Can't have negative numbers. "
#         )


def check_user_owns_product_by_name(product_name, user_id) -> bool:
    """
    Checks if user already owns the product with the same name. If so, returns True,
    otherwise returns False. Used for checking duplicating names in updating product-info.
    """
    for product in list_user_products(user_id):
        if product.name == product_name:
            return True
    return False


def check_user_owns_product_by_product(user_id, product_model) -> None:
    """
    Checks if user already owns the product by checking the list of products the user owns.
    If so, aborts to 403, otherwise does nothing.
    Used to check buyer can't buy his own products.
    """
    if product_model in list_user_products(user_id):
        abort(403, "You can't buy your own products")


def get_name_on_cc(user_id):
    user = User.get(user_id)
    first_name = user.first_name
    last_name = user.last_name
    full_name = first_name[0] + ". " + last_name
    return full_name


def create_hidden_cc(password):
    return str(password)[-4:].rjust(len(str(password)), "*")


def create_dynamic_formselect(session, form, field):
    if session.get("cart"):
        for product_id in session["cart"]:
            stock = Product.get(product_id).stock
            setattr(
                form,
                str(f"product_id-{product_id}"),
                field("Amount", choices=[i for i in range(1, stock + 1)], coerce=int),
            )


# from app import db
# from models import User, Product, Tag, ProductTag
# from main import create_producttags