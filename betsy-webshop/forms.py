from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    ValidationError,
    BooleanField,
    SelectField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

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
        user = User.get_or_none(User.username == username.data)
        if user:
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


class UpdateAccountForm(FlaskForm):
    first_name = StringField("Name", validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField(
        "Surname", validators=[InputRequired(), Length(min=2, max=120)]
    )
    address = StringField(
        "Address", validators=[InputRequired(), Length(min=8, max=200)]
    )
    city = StringField("City", validators=[InputRequired(), Length(min=2, max=50)])
    country = SelectField(
        "Country",
        choices=["...", "Netherlands", "Belgium", "Germany", "France", "Other"],
        validators=[InputRequired()],
    )
    cc_number = StringField(
        "Credit Card Number", validators=[InputRequired(), Length(min=2, max=50)]
    )
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=25)],
    )
    email = StringField("Email", validators=[InputRequired(), Length(max=50), Email()])
    # password = PasswordField("Password", validators=[InputRequired()])

    # image_file = FileField(
    #     "Change Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    # )
    update = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:

            user = User.get_or_none(User.username == username.data)
            if user:
                raise ValidationError(
                    f"Username: {username.data} is taken. Please choose another username"
                )

    def validate_email(self, email):
        if email.data != current_user.email:

            user_email = User.get_or_none(User.email == email.data)
            if user_email:
                raise ValidationError(
                    f"A user with email: {email.data} already exists."
                )
