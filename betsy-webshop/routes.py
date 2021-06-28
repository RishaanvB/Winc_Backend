from flask.helpers import send_file
from wtforms.validators import ValidationError
from utils import is_safe_url

from app import app, db
from app import login_manager

from models import User, Product, Tag, ProductTag, Transaction
from forms import RegistrationForm, LoginForm, UpdateAccountForm, AddProduct, SearchForm

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
)


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
    search_form = SearchForm()

    return render_template(
        "index.html",
        title="Home",
        users=users,
        products=products,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    users = User.select()
    login_form = LoginForm()
    register_form = RegistrationForm()
    search_form = SearchForm()

    if register_form.validate_on_submit():
        password = register_form.password.data
        hashed_pw = generate_password_hash(password)
        User.create(
            username=register_form.username.data,
            email=register_form.email.data,
            password=hashed_pw,
        )
        flash(
            f"Welcome {register_form.username.data}! Your account has been created!",
            "success",
        )

    else:
        flash(
            "Registration failed!!! Check if your input was correct.",
            "danger",
        )
    # is_failed_login makes sure modal reopens after failed register
    return render_template(
        "index.html",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        users=users,
        is_failed_register=True,
        is_failed_login=False,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    users = User.select()
    login_form = LoginForm()
    register_form = RegistrationForm()
    search_form = SearchForm()
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

        else:
            flash(
                "Login failed, your email is not known to us. Please check your spelling.",
                "danger",
            )
    # is_failed_login makes sure modal reopens after failed login
    return render_template(
        "index.html",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        users=users,
        is_failed_login=True,
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
    form = UpdateAccountForm(country=current_user.country)
    search_form = SearchForm()
    banner_info = f"Hey {current_user.username}. This is your account."

    if form.validate_on_submit():
        user = User.get_by_id(current_user.id)

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.address = form.address.data
        user.city = form.city.data
        user.country = form.country.data
        user.cc_number = form.cc_number.data
        user.username = form.username.data
        user.email = form.email.data
        user.save()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))

    return render_template(
        "account.html",
        title="Account",
        update_form=form,
        search_form=search_form,
        banner_info=banner_info,
    )


@app.route("/account/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    # test purposes !!!!DELETE!!!
    products = [product for product in current_user.products]
    # test purposes !!!!DELETE!!!

    banner_info = "Add a product to your existing catalog!"
    product_form = AddProduct()
    search_form = SearchForm()

    if product_form.validate_on_submit():
        tags_list = get_words_in_string(product_form.tags.data)
        new_product = Product.create(
            name=product_form.name.data,
            price_per_unit=product_form.price_per_unit.data,
            stock=int(product_form.amount_to_add.data),
            owner=current_user.id,
            description=product_form.description.data,
        )

        for new_tag in tags_list:
            tag_to_add = Tag.get_or_create(name=new_tag)
            ProductTag.create(
                product=Product.get_by_id(new_product.id),
                tag=Tag.get_by_id(tag_to_add[0].id),
            )

        flash("New product has been added to catalog!", "success")
        return redirect(url_for("add_product"))

    return render_template(
        "add_product.html",
        product_form=product_form,
        title="Product",
        banner_info=banner_info,
        products=products,
        get_tags=get_tags_per_product,
        search_form=search_form,
    )


@app.route("/search_results/<search_term>", methods=["GET", "POST"])
def search_results(search_term):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_form = SearchForm()
    products = get_products_by_name(search_term)

    return render_template(
        "search_results.html",
        products=products,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        search_term=search_term,
    )


@app.route("/search_results", methods=["GET", "POST"])
def search():
    # register_form = RegistrationForm()
    # login_form = LoginForm()
    # users = User.select()
    search_form = SearchForm()
    if request.method == "POST" and search_form.validate_on_submit():
        return redirect(
            (url_for("search_results", search_term=search_form.search.data))
        )  # or what you want
    return redirect(url_for("search_results", search_term=search_form.search.data))
