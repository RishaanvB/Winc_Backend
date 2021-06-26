from utils import is_safe_url

from app import app, db
from app import login_manager

from models import User, Product, Tag, ProductTag, Transaction
from forms import RegistrationForm, LoginForm, UpdateAccountForm

from flask import render_template, url_for, redirect, flash, request, abort
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    users = User.select()
    login_form = LoginForm()
    register_form = RegistrationForm()
    return render_template(
        "index.html",
        title="Home",
        users=users,
        login_form=login_form,
        register_form=register_form,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    users = User.select()
    login_form = LoginForm()
    register_form = RegistrationForm()
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
        users=users,
        is_failed_register=True,
        is_failed_login=False,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    users = User.select()
    login_form = LoginForm()
    register_form = RegistrationForm()
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
    form = UpdateAccountForm()
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
        "account.html", title="Account", update_form=form, banner_info=banner_info
    )
