from flask import render_template, url_for, redirect, flash, request, abort
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)
from playhouse.flask_utils import get_object_or_404

from app import app, login_manager
from main import (
    delete_all_products_from_user,
    delete_producttags_from_product,
    delete_user,
    get_products_per_tag,
    get_tagnames,
    get_tags_per_product,
    get_products_by_name,
    list_user_products,
    get_alpha_tag_names,
    add_product_to_catalog,
    create_producttags,
    purchase_product,
    check_tags_in_list,
    delete_product_by_id,
    get_user_sold_transactions,
    get_user_bought_transactions,
)
from models import User, Product, Tag, ProductTag, Transaction
from forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    AddProductForm,
    SearchForm,
    UpdateProductForm,
)

from utils import is_safe_url, validate_duplicate_product


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
    search_form.search_tag.choices = get_alpha_tag_names()

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
    products = Product.select()
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
        title="Register",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        users=users,
        products=products,
        is_failed_register=True,  # is_failed_register makes sure modal reopens after failed register
        is_failed_login=False,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    users = User.select()
    products = Product.select().order_by(Product.id.desc())

    login_form = LoginForm()
    register_form = RegistrationForm()
    search_form = SearchForm()
    search_form.search_tag.choices = get_alpha_tag_names()

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
                search_form=search_form,
                products=products,
                users=users,
                is_failed_login=True,
                is_failed_register=False,
            )
    return render_template(
        "index.html",
        title="Login",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
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
    update_account_form = UpdateAccountForm(country=current_user.country)
    add_product_form = AddProductForm()
    search_form = SearchForm()

    search_form.search_tag.choices = get_alpha_tag_names()
    products = list_user_products(current_user.id)

    return render_template(
        "account.html",
        add_product_form=add_product_form,
        update_account_form=update_account_form,
        search_form=search_form,
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
        return render_template(
            "account.html",
            add_product_form=AddProductForm(),
            update_account_form=update_account_form,
            search_form=SearchForm(),
            products=list_user_products(current_user.id),
        )


@app.route(
    "/search_results/<search_term>/<search_tag>/",
    methods=["GET", "POST"],
)
def search_results(search_term, search_tag):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_form = SearchForm()
    search_form.search_tag.choices = get_alpha_tag_names()
    if current_user.is_anonymous:
        user = None
    else:
        user = User.get(current_user.id)

    if search_term == "All" and search_tag == "All":
        all_products = Product.select()
    elif search_term == "All":
        all_products = get_products_per_tag(search_tag)
    elif search_tag == "All":
        all_products = get_products_by_name(search_term)
    else:
        all_products = (
            get_products_by_name(search_term)
            .join(ProductTag)
            .join(Tag)
            .distinct()
            .where(Tag.name == search_tag)
        )
    flash(f"Results for '{search_term}' and categories '{search_tag}' ", "success")

    return render_template(
        "search_results.html",
        title=search_term,
        all_products=all_products,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        user=user,
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    search_form = SearchForm()
    search_form.search_tag.choices = get_alpha_tag_names()

    if search_form.validate_on_submit():
        if search_form.search_term.data == "":
            search_term = "All"
        else:
            search_term = search_form.search_term.data
        return redirect(
            (
                url_for(
                    "search_results",
                    search_term=search_term,
                    search_tag=search_form.search_tag.data,
                )
            )
        )
    flash("something went wrong", "danger")
    return redirect(url_for("home"))


@app.route("/account/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    add_product_form = AddProductForm()
    update_account_form = UpdateAccountForm(country=current_user.country)
    product_name = add_product_form.name.data.lower()
    product = {
        "name": product_name,
        "price_per_unit": add_product_form.price_per_unit.data,
        "stock": add_product_form.stock.data,
        "description": add_product_form.description.data,
    }

    if validate_duplicate_product(product_name, current_user.id):
        flash(
            f"You already own a product with the same name: '{product_name}'", "danger"
        )
        return render_template(
            "account.html",
            add_product_form=add_product_form,
            update_account_form=update_account_form,
            search_form=SearchForm(),
            products=list_user_products(current_user.id),
        )

    if add_product_form.validate_on_submit():
        new_product = add_product_to_catalog(current_user.id, product)

        if add_product_form.tags.data:
            create_producttags(new_product.id, add_product_form.tags.data)
        flash(
            f"Your product '{add_product_form.name.data}' has been added to the catalog!",
            "success",
        )
        return redirect(url_for("account"))

    flash(
        "Something went wrong with the product inputs, check your inputs.",
        "danger",
    )
    return render_template(
        "account.html",
        add_product_form=add_product_form,
        update_account_form=update_account_form,
        search_form=SearchForm(),
        products=list_user_products(current_user.id),
    )


@app.route("/product/<int:product_id>")
@login_required
def update_product_page(product_id):
    if current_user.id != Product.get(product_id).owner.id:
        abort(403)

    search_form = SearchForm()
    search_form.search_tag.choices = get_alpha_tag_names()
    register_form = RegistrationForm()
    login_form = LoginForm()
    update_account_form = UpdateAccountForm(country=current_user.country)
    add_product_form = AddProductForm()

    products = Product.select().where(Product.id == product_id)
    product = get_object_or_404(products, (Product.id == product_id))
    checked_tags = check_tags_in_list(get_tagnames(), get_tags_per_product(product_id))
    update_product_form = UpdateProductForm(
        description=product.description, stock=product.stock
    )

    return render_template(
        "update_product_page.html",
        title=product.name,
        product=product,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        update_product_form=update_product_form,
        update_account_form=update_account_form,
        add_product_form=add_product_form,
        checked_tags=checked_tags,
    )


@app.route("/product/<int:product_id>/update", methods=["GET", "POST"])
@login_required
def update_product(product_id):
    product = Product.get(product_id)
    if current_user.id != Product.get(product_id).owner.id:
        abort(403)

    update_product_form = UpdateProductForm()
    login_form = LoginForm()
    register_form = RegistrationForm()
    search_form = SearchForm()
    update_account_form = UpdateAccountForm(country=current_user.country)
    add_product_form = AddProductForm()

    if update_product_form.validate_on_submit():

        product.name = update_product_form.name.data
        product.price_per_unit = update_product_form.price_per_unit.data
        product.stock = update_product_form.stock.data
        product.description = update_product_form.description.data
        delete_producttags_from_product(product_id)
        create_producttags(product_id, update_product_form.tags.data)
        product.save()
        flash(f"{product.name} has been updated!", "success")
        return redirect(url_for("update_product_page", product_id=product_id))
    flash(
        "Something went wrong with updating the product. Please check your input.",
        "danger",
    )
    return render_template(
        "update_product_page.html",
        title=product.name,
        product=product,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        update_product_form=update_product_form,
        update_account_form=update_account_form,
        add_product_form=add_product_form,
        checked_tags=check_tags_in_list(
            get_tagnames(), get_tags_per_product(product_id)
        ),
    )


@app.route("/product/<int:product_id>/delete", methods=["GET", "DELETE"])
@login_required
def delete_product(product_id):
    if current_user.id != Product.get(product_id).owner.id:
        abort(403)
    delete_product_by_id(product_id)
    flash("Your product has been deleted!", "success")
    return redirect(url_for("account"))


@app.route("/product/<int:user_id>/delete_all", methods=["GET", "DELETE"])
@login_required
def delete_all_products(user_id):
    if current_user.id != user_id:
        abort(403)
    delete_all_products_from_user(current_user.id)
    flash("Your products have been deleted!", "success")
    return redirect(url_for("account"))


@app.route("/account/delete/<int:user_id>", methods=["GET", "DELETE"])
@login_required
def delete_user_account(user_id):
    if current_user.id != user_id:
        abort(403)
    logout_user()
    delete_user(user_id)
    flash("Your account has been deleted!", "success")
    return redirect(url_for("home"))


@app.route("/users/<int:user_id>")
def user_profile(user_id):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_form = SearchForm()

    user_products = list_user_products(user_id)

    search_form.search_tag.choices = get_alpha_tag_names()

    users = User.select().where(User.id == user_id)
    user = get_object_or_404(users, User.id == user_id)

    return render_template(
        "user_profile.html",
        title=user.username,
        user=user,
        user_products=user_products,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        transactions_sold=get_user_sold_transactions(user_id),
        transactions_bought=get_user_bought_transactions(user_id),
        bannerinfo={
            "banner_bg": "user-profile-banner",
            "banner_h1": "Welcome!",
            "banner_text": f"Here you can find the products and info for user '{user.username}'",
        },
    )


@app.route("/buy_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def buy_product(product_id):
    get_object_or_404(Product, (Product.id == product_id))

    # check if buyer is not owner of product
    buyer_id = current_user.id
    quantity = 1  # needs to change dynamically

    purchase_product(product_id, buyer_id, quantity)
    flash("Product bought")
    return redirect(url_for(request.referrer))
    return redirect(url_for("home"))


@app.errorhandler(404)
def error_404(error):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_form = SearchForm()
    search_form.search_tag.choices = get_alpha_tag_names()

    message = "Oops! Page not found."
    error_type = 404
    return (
        render_template(
            "error.html",
            title="404 Error",
            message=message,
            login_form=login_form,
            register_form=register_form,
            search_form=search_form,
            error_type=error_type,
            error=error,
        ),
        404,
    )


@app.errorhandler(403)
def error_403(error):
    register_form = RegistrationForm()
    login_form = LoginForm()
    search_form = SearchForm()
    search_form.search_tag.choices = get_alpha_tag_names()

    message = "You dont'have access to this page!"
    error_type = 403

    return (
        render_template(
            "error.html",
            title="403 Error",
            message=message,
            login_form=login_form,
            register_form=register_form,
            search_form=search_form,
            error=error,
            error_type=error_type,
        ),
        403,
    )
