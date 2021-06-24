from peewee import IntegrityError
from app import app, db
from flask import render_template, url_for, redirect, flash, request, abort, is_safe_url
from models import User, Product, Tag, ProductTag, Transaction
from forms import RegistrationForm, LoginForm
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (
    login_user,
    current_user,
    login_required,
    logout_user,
)
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.route("/")
@app.route("/home")
def home():
    users = User.select()
    return render_template("index.html", title="Home", users=users)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        hashed_pw = generate_password_hash(password)

        User.create(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )

        flash(f"Welcome {form.username.data}! Your account has been created!")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not is_safe_url(next_page):
                return abort(400)
            flash(f"Logged in successfully. Welcome {user.username}")
            return redirect(next_page or url_for("home"))

    return render_template("login.html", title="Login", form=form)
