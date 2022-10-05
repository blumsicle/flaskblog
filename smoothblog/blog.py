"""Blog related routes."""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .database import db
from .forms import CreateBlogForm
from .models import Blog, User

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Just redirect to the home page."""
    return redirect(url_for("blog.home"))


@bp.route("/home")
def home():
    """Main page that shows all blogs."""
    order = Blog.date.desc()  # pylint: disable=no-member
    blogs = Blog.query.order_by(order).join(User).all()

    return render_template("blog/home.html", blogs=blogs)


@bp.route("/about")
def about():
    """About page."""
    return render_template("blog/about.html")


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new blog."""
    form = CreateBlogForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_blog = Blog(title, content, current_user.id)
        db.session.add(new_blog)
        db.session.commit()

        flash("Blog successfully created!", "success")
        return redirect(url_for("blog.home"))

    for field, errors in form.errors.items():
        flash(f"{field}: {' '.join(errors)}", "danger")

    return render_template("blog/create.html", form=form)


@bp.route("/delete/<int:blog_id>")
@login_required
def delete(blog_id):
    """Delete the specific blog."""
    blog = Blog.query.get(blog_id)
    if blog and (current_user.is_admin or current_user.id == blog.user_id):
        db.session.delete(blog)
        db.session.commit()
    else:
        flash("Blog cannot be deleted.", "danger")

    return redirect(url_for("blog.home"))
