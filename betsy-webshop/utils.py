from urllib.parse import urlparse, urljoin
from flask import request, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from wtforms import ValidationError
from main import list_user_products
from app import app
from datetime import datetime


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def validate_owner_owns_product(product_name, user_id):
    current_user_products_list = list_user_products(user_id)
    for product in current_user_products_list:
        if product.name == product_name:
            return True
    return False


def validate_price_per_unit(self, price_per_unit):
    if price_per_unit.data is not None and price_per_unit.data < 0:
        raise ValidationError(
            "You want them to pay YOU?? Can't have negative numbers. "
        )
