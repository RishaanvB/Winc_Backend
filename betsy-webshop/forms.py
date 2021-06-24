from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    BooleanField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo

from models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=30)],
    )

    email = StringField(
        "Email", validators=[InputRequired(), Length(min=5, max=50), Email()]
    )
    password = PasswordField(
        "Set Password",
        validators=[
            InputRequired(),
            EqualTo(
                "password_confirm", message="Password must be identical in both inputs"
            ),
            Length(min=5, max=20),
        ],
    )
    password_confirm = PasswordField("Confirm Password")
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        username = User.get_or_none(User.username == username.data)
        if username:
            raise ValidationError("Username is taken. Please choose another username")

    def validate_email(self, email):
        email = User.get_or_none(User.email == email.data)
        if email:
            raise ValidationError("A user with this email already exists.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[InputRequired(), Length(min=5, max=50), Email()]
    )
    password = PasswordField("Your Password", validators=[InputRequired()])
    login = SubmitField("Login!")
