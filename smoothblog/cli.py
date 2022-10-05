"""Adds commands to the `flask` cli."""

import click
from flask import current_app

from .database import db
from .models import User


def init_db():
    """Drops previous database and initializes a new one."""
    db.drop_all()
    db.create_all()

    email = current_app.config["ADMIN_EMAIL"]
    username = current_app.config["ADMIN_USERNAME"]
    password = current_app.config["ADMIN_PASSWORD"]

    admin = User(email, username, password, is_admin=True)

    db.session.add(admin)
    db.session.commit()


@click.command("init-db")
def init_db_command():
    """Creates a CLI command to initialize the database."""
    init_db()
    click.echo("Initialized the database.")
