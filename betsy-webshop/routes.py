from flask.helpers import send_file
from werkzeug import exceptions
from wtforms.validators import ValidationError
from utils import is_safe_url, validate_owner_owns_product
from datetime import datetime
from app import app, db
from app import login_manager

from models import User, Product, Tag, ProductTag, Transaction
from forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    AddProductForm,
    SearchByTermForm,
    SearchByTagForm,
)

from flask import render_template, url_for, redirect, flash, request, abort
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)
from main import (
    list_products_per_tag,
    get_words_in_string,
    get_tags_per_product,
    get_products_by_name,
    list_user_products,
    get_alpha_tag_names,
    add_product_to_catalog,
)


@app.context_processor
def string_to_date_to_string():
    """
    Converts stringtime to datetime object, back to a stringtime.
    Workaround, since Sqlite stores datetimes as strings.
    """

    def format_string(date_str):
        format = "%Y-%m-%d %H:%M:%S.%f"
        dt_object = datetime.strptime(date_str, format)
        format = "%Y, %B %w, %H%Mh"
        dt_string = dt_object.strftime(format)
        return dt_string

    return dict(format_string=format_string)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    users = User.select()
    products = Product.select().order_by(Product.id.desc())
    login_form = LoginForm()
    register_form = RegistrationForm()
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm()
    search_tag_form.search_tag.choices = get_alpha_tag_names()

    return render_template(
        "index.html",
        title="Home",
        users=users,
        products=products,
        login_form=login_form,
        register_form=register_form,
        search_term_form=search_term_form,
        search_tag_form=search_tag_form,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    users = User.select()
    products = Product.select()
    login_form = LoginForm()
    register_form = RegistrationForm()
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm

    if register_form.validate_on_submit():
        password = register_form.password.data
        hashed_pw = generate_password_hash(password)
        User.create(
            username=register_form.username.data,
            email=register_form.email.data,
            password=hashed_pw,
        )
        flash(
            "Your account has been created! Please login update your profile!",
            "success",
        )
        return redirect(url_for("home"))

    flash(
        "Registration failed!!! Check if your input was correct.",
        "danger",
    )
    return render_template(
        "index.html",
        login_form=login_form,
        register_form=register_form,
        search_term_form=search_term_form,
        search_tag_form=search_tag_form,
        users=users,
        products=products,
        is_failed_register=True,
        is_failed_login=False,  # is_failed_register makes sure modal reopens after failed register
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    users = User.select()
    products = Product.select().order_by(Product.id.desc())

    login_form = LoginForm()
    register_form = RegistrationForm()
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm()
    search_tag_form.search_tag.choices = get_alpha_tag_names()

    if login_form.validate_on_submit():
        user = User.get_or_none(User.email == login_form.email.data)

        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not is_safe_url(next_page):
                return abort(400)
            flash(f"Logged in successfully. Welcome {user.username}", "success")
            return redirect(next_page or url_for("account"))

        if user and not check_password_hash(user.password, login_form.password.data):
            flash("Your password is not correct. Pleas try again.", "danger")
            return render_template(
                "index.html",
                login_form=login_form,
                register_form=register_form,
                search_term_form=search_term_form,
                search_tag_form=search_tag_form,
                products=products,
                users=users,
                is_failed_login=True,
                is_failed_register=False,
            )

    # flash(
    #     "Email address not known. Please try another one.",
    #     "danger",
    # )

    return render_template(
        "index.html",
        login_form=login_form,
        register_form=register_form,
        search_term_form=search_term_form,
        search_tag_form=search_tag_form,
        users=users,
        products=products,
        is_failed_login=True,  # is_failed_login makes sure modal reopens after failed login
        is_failed_register=False,
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out!", "success")
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    products = list_user_products(current_user.id)

    update_account_form = UpdateAccountForm(country=current_user.country)
    add_product_form = AddProductForm()
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm()
    search_tag_form.search_tag.choices = get_alpha_tag_names()
    banner_info = f"Hey {current_user.username}. This is your account."

    return render_template(
        "account.html",
        title="Account",
        add_product_form=add_product_form,
        update_account_form=update_account_form,
        search_term_form=search_term_form,
        search_tag_form=search_tag_form,
        banner_info=banner_info,
        products=products,
    )


@app.route("/account/update", methods=["GET", "POST"])
@login_required
def update_account():
    update_account_form = UpdateAccountForm(country=current_user.country)

    if update_account_form.validate_on_submit():
        user = User.get_by_id(current_user.id)

        user.first_name = update_account_form.first_name.data
        user.last_name = update_account_form.last_name.data
        user.address = update_account_form.address.data
        user.city = update_account_form.city.data
        user.country = update_account_form.country.data
        user.cc_number = update_account_form.cc_number.data
        user.username = update_account_form.username.data
        user.email = update_account_form.email.data
        user.save()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    else:
        flash("Something went wrong with your inputs. Please try again", "warning")
        return redirect(url_for("account"))


@app.route("/account/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    add_product_form = AddProductForm()
    name = add_product_form.name.data.lower()
    # price_per_unit = format(add_product_form.price_per_unit.data, ".2f")
    # stock = int(add_product_form.stock.data)
    owner = current_user.id
    # description = add_product_form.description.data

    tags_list = get_words_in_string(add_product_form.tags.data)
    product = {
        "name": add_product_form.name.data.lower(),
        "price_per_unit": format(add_product_form.price_per_unit.data, ".2f"),
        "stock": int(add_product_form.stock.data),
        "description": add_product_form.description.data,
    }

    if validate_owner_owns_product(name, owner):
        flash(f"You already own the product: {name}", "danger")
        return redirect(url_for("account"))
    else:
        if add_product_form.validate_on_submit():
            new_product = add_product_to_catalog(owner, product)
            for new_tag in tags_list:
                try:
                    tag_to_add = Tag.get_or_create(name=new_tag)
                    ProductTag.create(
                        product=Product.get_by_id(new_product.id),
                        tag=Tag.get_by_id(tag_to_add[0].id),
                    )
                except NameError:
                    raise ValidationError("somethign went wrong")
            flash(
                f"Your {add_product_form.name.data} has been added to the catalog!",
                "success",
            )
            return redirect(url_for("account"))
    flash("Something went wrong, check your inputs.", "danger")
    return redirect(url_for("account"))


@app.route("/search_name/<search_term>/", methods=["GET", "POST"])
def search_by_term(search_term):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm()
    search_tag_form.search_tag.choices = get_alpha_tag_names()
    all_products = get_products_by_name(search_term)

    return render_template(
        "search_results.html",
        all_products=all_products,
        login_form=login_form,
        register_form=register_form,
        search_term_form=search_term_form,
        search_tag_form=search_tag_form,
    )


@app.route("/search_tags/<search_tag>/", methods=["GET", "POST"])
def search_by_tag(search_tag):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm()
    search_tag_form.search_tag.choices = get_alpha_tag_names()

    # tag_id = Tag.get_or_none(Tag.name == search_term_form.search_tag.data).get_id()
    tag_id = Tag.get_or_none(Tag.name == search_tag).get_id()
    all_products = list_products_per_tag(tag_id)

    return render_template(
        "search_results.html",
        all_products=all_products,
        login_form=login_form,
        register_form=register_form,
        search_term_form=search_term_form,
        search_tag_form=search_tag_form,
    )


@app.route("/search_results", methods=["GET", "POST"])
def search():
    search_term_form = SearchByTermForm()
    search_tag_form = SearchByTagForm()
    search_tag_form.search_tag.choices = get_alpha_tag_names()
    if search_term_form.validate_on_submit():
        return redirect(
            (
                url_for(
                    "search_by_term",
                    search_term=search_term_form.search_term.data,
                )
            )
        )
    if search_tag_form.validate_on_submit():
        return redirect(
            (
                url_for(
                    "search_by_tag",
                    search_tag=search_tag_form.search_tag.data,
                )
            )
        )
    return redirect(url_for("home"))


@app.route("/product/<int:product_id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_product(product_id):
    Product.delete_by_id(product_id)
    flash("Your product has been deleted!", "success")
    return redirect(url_for("account"))


@app.route("/account/delete/<int:user_id>", methods=["GET", "DELETE"])
@login_required
def delete_user_account(user_id):
    logout()
    User.delete_instance(user_id)
    flash("Your account has been deleted!", "success")
    return redirect(url_for("home"))