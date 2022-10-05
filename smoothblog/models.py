"""Models used to represent database tables."""

from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash

from .database import db


class User(db.Model, UserMixin):
    """The User model relates to the user table."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(
        # 102 is the length returned from `generate_password_hash`
        db.String(102),
        nullable=False,
    )
    blogs = db.relationship("Blog", back_populates="user")
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, username, password_str, is_admin=False):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password_str)
        self.is_admin = is_admin

    def __repr__(self):
        return rf"<User {self.email}>"


class Blog(db.Model):
    """The Blog model relates to the blog table."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return rf"<Blog {self.title}>"
