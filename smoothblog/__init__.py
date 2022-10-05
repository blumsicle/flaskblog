"""A Flask based app that allows users to create blogs. """

import os
from logging.config import dictConfig

from dotenv import load_dotenv
from flask import Flask

from . import auth, blog
from .cli import init_db_command
from .database import db
from .login_manager import lm

load_dotenv()


def create_app(test_config=None):
    """Initialize the app and configure it."""
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY=os.environ["SECRET_KEY"],
            SQLALCHEMY_DATABASE_URI="sqlite:///"
            + os.path.join(app.instance_path, os.environ["DATABASE_NAME"]),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            ADMIN_EMAIL=os.environ["ADMIN_EMAIL"],
            ADMIN_USERNAME=os.environ["ADMIN_USERNAME"],
            ADMIN_PASSWORD=os.environ["ADMIN_PASSWORD"],
        )

        os.makedirs(app.instance_path, exist_ok=True)

        _init_logging(app)

    db.init_app(app)
    app.cli.add_command(init_db_command)

    lm.login_view = "auth.login"
    lm.login_message_category = "info"
    lm.init_app(app)

    app.register_blueprint(blog.bp, url_prefix="/")
    app.register_blueprint(auth.bp, url_prefix="/auth")

    return app


def _init_logging(app):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                    "level": "WARNING",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": os.path.join(app.instance_path, os.environ["LOG_FILE"]),
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "root": {"level": "INFO", "handlers": ["wsgi", "file"]},
        }
    )
