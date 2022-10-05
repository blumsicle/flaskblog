"""Creates the global database."""

from functools import wraps

from flask import flash, redirect, url_for
from flask_login import LoginManager, current_user

from .models import User

lm = LoginManager()


@lm.user_loader
def load_user(id_):
    """Callback used to reload the user object from the session."""

    return User.query.get(id_)


def logout_required(func):
    """Decorator that redirects to `blog.home` if user is logged in."""

    @wraps(func)
    def view(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in", "danger")
            return redirect(url_for("blog.home"))

        return func(*args, **kwargs)

    return view
