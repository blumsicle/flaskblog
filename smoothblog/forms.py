"""WTForms classes used throughout app."""

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, TextAreaField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .models import Blog, User


def _get_max_length(column):
    return column.property.columns[0].type.length


class RegisterForm(FlaskForm):
    """Form to register a new user."""

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=_get_max_length(User.email))],
    )
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=_get_max_length(User.username))],
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), EqualTo("confirm")]
    )
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form to login an existing user."""

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=_get_max_length(User.email))],
    )
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember me", default=False)


class CreateBlogForm(FlaskForm):
    """Form to create a new blog."""

    title = StringField(
        "Title", validators=[InputRequired(), Length(max=_get_max_length(Blog.title))]
    )
    content = TextAreaField("Content", validators=[InputRequired()])
