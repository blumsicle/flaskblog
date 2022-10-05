"""Authentication related routes."""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from .database import db
from .forms import LoginForm, RegisterForm
from .login_manager import logout_required
from .models import Blog, User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    """Register a new user."""
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User(email, username, password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("User with the same username or email already exists.", "danger")
        else:
            login_user(new_user)
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("blog.home"))

    for field, errors in form.errors.items():
        flash(f"{field}: {' '.join(errors)}", "danger")

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    """Login an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=remember)
                flash(f"Welcome back, {user.username}!", "success")
                if user.is_admin:
                    return redirect(url_for("auth.admin"))
                return redirect(url_for("blog.home"))

            flash("Incorrect password, try again.", "danger")
        else:
            flash("User does not exist.", "danger")

    for field, errors in form.errors.items():
        flash(f"{field}: {' '.join(errors)}", "danger")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    return redirect(url_for("blog.home"))


@bp.route("/admin")
@login_required
def admin():
    """View all users."""
    if current_user.is_admin:
        users = User.query.all()
        return render_template("auth/admin.html", users=users)

    flash("You do not have permissions to access that page.", "danger")
    return redirect(url_for("blog.home"))


@bp.route("/admin/delete/<int:user_id>")
@login_required
def delete(user_id):
    """Delete specified user and all associated blogs."""
    if current_user.is_admin:
        Blog.query.where(Blog.user_id == user_id).delete()

        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            flash("User does not exist", "danger")

        return redirect(url_for("auth.admin"))

    flash("You do not have permissions to access that page.", "danger")
    return redirect(url_for("blog.home"))
