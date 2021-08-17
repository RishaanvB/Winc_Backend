from flask import render_template, url_for, redirect, flash, request, abort
from flask.globals import session
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)
from werkzeug.utils import secure_filename
from wtforms import SelectField
from playhouse.flask_utils import get_object_or_404, object_list

from app import app, login_manager
from main import (
    delete_all_products_from_user,
    delete_picture_data,
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
    is_safe_url,
    check_user_owns_product_by_name,
    check_user_owns_product_by_product,
    get_name_on_cc,
    create_hidden_cc,
    create_dynamic_formselect,
    get_user_transactions,
    save_picture_data,
)
from models import User, Product, Tag, ProductTag
from forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    AddProductForm,
    SearchForm,
    UpdateProductForm,
    ProductAmountForm,
)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    login_form = LoginForm(prefix="login_form")
    register_form = RegistrationForm(prefix="register_form")
    search_form = SearchForm(prefix="search_form")
    search_form.search_tag.choices = get_alpha_tag_names()

    return render_template(
        "index.html",
        title="Home",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        all_products=Product.select(),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    login_form = LoginForm(prefix="login_form")
    register_form = RegistrationForm(prefix="register_form")
    search_form = SearchForm(prefix="search_form")

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
        is_failed_register=True,  # is_failed_register makes sure modal reopens after failed register
        is_failed_login=False,
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    login_form = LoginForm(prefix="login_form")
    register_form = RegistrationForm(prefix="register_form")
    search_form = SearchForm(prefix="search_form")
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
                is_failed_login=True,
                is_failed_register=False,
            )
    return render_template(
        "index.html",
        title="Login",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        is_failed_login=True,  # is_failed_login makes sure modal reopens after failed login
        is_failed_register=False,
    )


@app.route("/logout")
@login_required
def logout():
    session.pop("cart", None)
    logout_user()
    flash("Successfully logged out!", "success")
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_account_form = UpdateAccountForm(
        prefix="update_account",
        country=current_user.country,
        profile_pic=current_user.profile_pic,
    )
    add_product_form = AddProductForm(prefix="add-product")
    search_form = SearchForm(prefix="search_form")

    search_form.search_tag.choices = get_alpha_tag_names()
    user_products = list_user_products(current_user.id)
    profile_pic = url_for(
        "static", filename=f"/profile_pics/{current_user.profile_pic}"
    )
    return render_template(
        "account.html",
        add_product_form=add_product_form,
        update_account_form=update_account_form,
        search_form=search_form,
        user_products=user_products,
        all_products=Product.select(),
        profile_pic=profile_pic,
    )


@app.route("/account/update", methods=["GET", "POST"])
@login_required
def update_account():
    update_account_form = UpdateAccountForm(
        prefix="update_account",
        country=current_user.country,
        profile_pic=current_user.profile_pic,
    )

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
        if update_account_form.profile_pic.data:
            delete_picture_data(current_user.id)
            user.profile_pic = save_picture_data(update_account_form.profile_pic.data)
        user.save()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    else:
        flash("Something went wrong with your inputs. Please try again", "warning")
        return render_template(
            "account.html",
            add_product_form=AddProductForm(prefix="add-product"),
            update_account_form=update_account_form,
            search_form=SearchForm(prefix="search_form"),
            user_products=list_user_products(current_user.id),
        )


@app.route("/account/transactions")
@login_required
def account_transactions():
    update_account_form = UpdateAccountForm(
        prefix="update_account", country=current_user.country
    )
    add_product_form = AddProductForm(prefix="add-product")
    search_form = SearchForm(prefix="search_form")

    search_form.search_tag.choices = get_alpha_tag_names()
    user_transactions = get_user_transactions(current_user.id)
    return render_template(
        "account_transactions.html",
        add_product_form=add_product_form,
        update_account_form=update_account_form,
        search_form=search_form,
        user_transactions=user_transactions,
        user_products=list_user_products(current_user.id),
    )


@app.route(
    "/search_results/<search_term>/<search_tag>/",
    methods=["GET", "POST"],
)
def search_results(search_term, search_tag):
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    search_form = SearchForm(prefix="search_form")
    search_form.search_tag.choices = get_alpha_tag_names()

    page = request.args.get("page", 1, type=int)
    if current_user.is_anonymous:
        user = None
    else:
        user = User.get(current_user.id)

    if search_term == "All" and search_tag == "All":
        all_products_on_search = Product.select()
    elif search_term == "All":
        all_products_on_search = get_products_per_tag(search_tag)
    elif search_tag == "All":
        all_products_on_search = get_products_by_name(search_term)
    else:
        all_products_on_search = (
            get_products_by_name(search_term)
            .join(ProductTag)
            .join(Tag)
            .where(Tag.name == search_tag)
        )
    product_count = all_products_on_search.count()
    all_products_on_search = all_products_on_search
    if product_count == 0:
        flash(
            f"We couldn't find any results for '{search_tag}' and '{search_term}'",
            "danger",
        )
        return redirect(request.referrer)
    return object_list(
        "search_results.html",
        query=all_products_on_search,
        context_variable="product_list",
        paginate_by=10,
        page=page,
        title="Search",
        product_count=product_count,
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        user=user,
        all_products=Product.select(),
        search_tuple=(search_term, search_tag),
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    search_form = SearchForm(prefix="search_form")
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
    add_product_form = AddProductForm(prefix="add-product")
    update_account_form = UpdateAccountForm(
        prefix="update_account", country=current_user.country
    )
    product_name = add_product_form.name.data.lower()
    product = {
        "name": product_name,
        "price_per_unit": add_product_form.price_per_unit.data,
        "stock": add_product_form.stock.data,
        "description": add_product_form.description.data,
    }

    if check_user_owns_product_by_name(product_name, current_user.id):
        flash(
            f"You already own a product with the same name: '{product_name}'", "danger"
        )
        return render_template(
            "account.html",
            add_product_form=add_product_form,
            update_account_form=update_account_form,
            search_form=SearchForm(prefix="search_form"),
            user_products=list_user_products(current_user.id),
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
        search_form=SearchForm(prefix="search_form"),
        user_products=list_user_products(current_user.id),
    )


@app.route("/product/<int:product_id>")
@login_required
def update_product_page(product_id):
    products = Product.select().where(Product.id == product_id)
    product = get_object_or_404(products, (Product.id == product_id))
    if current_user.id != Product.get(product_id).owner.id:
        abort(403)

    search_form = SearchForm(prefix="search_form")
    search_form.search_tag.choices = get_alpha_tag_names()
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    update_account_form = UpdateAccountForm(
        prefix="update_account", country=current_user.country
    )
    add_product_form = AddProductForm(prefix="add-product")

    checked_tags = check_tags_in_list(get_tagnames(), get_tags_per_product(product_id))
    update_product_form = UpdateProductForm(
        prefix="update-product", description=product.description, stock=product.stock
    )

    return render_template(
        "update_product_page.html",
        title=product.name,
        product=product,
        all_products=Product.select(),
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        update_product_form=update_product_form,
        update_account_form=update_account_form,
        add_product_form=add_product_form,
        checked_tags=checked_tags,
        user_products=list_user_products(current_user.id),
    )


@app.route("/product/<int:product_id>/update", methods=["GET", "POST"])
@login_required
def update_product(product_id):
    product = Product.get(product_id)
    if current_user.id != Product.get(product_id).owner.id:
        abort(403)

    update_product_form = UpdateProductForm(
        prefix="update-product",
    )
    login_form = LoginForm(prefix="login_form")
    register_form = RegistrationForm(prefix="register_form")
    search_form = SearchForm(prefix="search_form")
    update_account_form = UpdateAccountForm(
        prefix="update_account", country=current_user.country
    )
    add_product_form = AddProductForm(prefix="add-product")

    if update_product_form.validate_on_submit():

        product.name = update_product_form.name.data
        product.price_per_unit = update_product_form.price_per_unit.data
        product.stock = update_product_form.stock.data
        product.description = update_product_form.description.data
        delete_producttags_from_product(product_id)
        create_producttags(product_id, update_product_form.tags.data)
        product.save()
        flash(f"'{product.name}' has been updated!", "success")
        return redirect(url_for("account"))
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
    product_name = Product.get(product_id).name
    if current_user.id != Product.get(product_id).owner.id:
        abort(403)
    delete_product_by_id(product_id)
    flash(f"Your product '{product_name}' has been deleted!", "success")
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
    if not current_user.is_anonymous:
        if user_id == current_user.id:
            return redirect(url_for("account"))
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    search_form = SearchForm(prefix="search_form")

    user_products = list_user_products(user_id)

    search_form.search_tag.choices = get_alpha_tag_names()

    users = User.select().where(User.id == user_id)
    user = get_object_or_404(users, User.id == user_id)
    profile_pic = (url_for("static", filename=f"/profile_pics/{user.profile_pic}"),)
    return render_template(
        "user_profile.html",
        title=user.username,
        user=user,
        user_products=user_products,
        all_products=Product.select(),
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        bannerinfo={
            "banner_bg": "user-profile-banner",
            "banner_h1": "Welcome!",
            "banner_text": f"Here you can find the products and info for user '{user.username}'",
        },
        profile_pic=profile_pic,
    )


@app.route("/handle_product_in_cart/<int:product_id>", methods=["GET", "POST"])
@login_required
def handle_product_in_cart(product_id):
    product = get_object_or_404(Product, (Product.id == product_id))
    check_user_owns_product_by_product(current_user.id, product)
    if "cart" not in session:
        session["cart"] = []

    if product.id in session["cart"]:
        session["cart"].remove(product.id)
        session.modified = True
        flash(f"'{product.name.capitalize()}' removed from cart.", "info")
        return redirect(request.referrer)

    elif product.id not in session["cart"]:
        session["cart"].append(product.id)
        session.modified = True
        flash(f"'{product.name.capitalize()}' added to cart.", "info")
        return redirect(
            request.referrer
        )  # is flask versie van request.headers.get("Referer")
    else:
        flash("Something went wrong", "danger")
        return redirect(request.referrer)


@app.route("/checkout")
@login_required
def checkout_page():
    create_dynamic_formselect(session, ProductAmountForm, SelectField)
    login_form = LoginForm(prefix="login_form")
    register_form = RegistrationForm(prefix="register_form")
    search_form = SearchForm(prefix="search_form")
    search_form.search_tag.choices = get_alpha_tag_names()
    update_account_form = UpdateAccountForm(
        prefix="update_account", country=current_user.country
    )
    add_product_form = AddProductForm(prefix="add-product")

    return render_template(
        "checkout.html",
        login_form=login_form,
        register_form=register_form,
        search_form=search_form,
        update_account_form=update_account_form,
        add_product_form=add_product_form,
        all_products=Product.select(),
        get_name_on_cc=get_name_on_cc,
        create_hidden_cc=create_hidden_cc,
        product_amount_form=ProductAmountForm(prefix="product_amount"),
    )


@app.route("/payment", methods=["GET", "POST"])
@login_required
def checkout_payment():
    product_amount_form = ProductAmountForm(prefix="product_amount")
    if product_amount_form.validate_on_submit():
        for id in session["cart"]:
            amount_bought = product_amount_form["product_id-" + str(id)].data
            purchase_product(id, current_user.id, amount_bought)
        flash(f"products bought ", "success")
        session.pop("cart", None)
        return redirect(url_for("home"))
    abort(500)


@app.errorhandler(400)
def error_400(error):
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    search_form = SearchForm(prefix="search_form")
    search_form.search_tag.choices = get_alpha_tag_names()

    message = "Bad Request"
    error_type = 400
    return (
        render_template(
            "error.html",
            title="400 Error",
            message=message,
            login_form=login_form,
            register_form=register_form,
            search_form=search_form,
            error_type=error_type,
            error=error,
            all_products=Product.select(),
        ),
        404,
    )


@app.errorhandler(404)
def error_404(error):
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    search_form = SearchForm(prefix="search_form")
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
            all_products=Product.select(),
        ),
        404,
    )


@app.errorhandler(403)
def error_403(error):
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    search_form = SearchForm(prefix="search_form")
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
            all_products=Product.select(),
        ),
        403,
    )


@app.errorhandler(500)
def error_500(error):
    register_form = RegistrationForm(prefix="register_form")
    login_form = LoginForm(prefix="login_form")
    search_form = SearchForm(prefix="search_form")
    search_form.search_tag.choices = get_alpha_tag_names()

    message = "Oops, something went wrong!"
    error_type = 500

    return (
        render_template(
            "error.html",
            title="500 Error",
            message=message,
            login_form=login_form,
            register_form=register_form,
            search_form=search_form,
            error=error,
            error_type=error_type,
            all_products=Product.select(),
        ),
        500,
    )
