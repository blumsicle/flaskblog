"""Fixtures used for testing."""

import os
import tempfile

import pytest
from smoothblog import create_app
from smoothblog.cli import init_db
from smoothblog.database import db
from smoothblog.models import Blog, User


@pytest.fixture
def app():
    """Initializes the app and database and cleans up after."""
    db_fd, db_path = tempfile.mkstemp(suffix=".sqlite")

    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "testing",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "ADMIN_EMAIL": "admin@email.com",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD": "admin",
        }
    )

    with app.app_context():
        init_db()
        db.session.add_all(
            [
                User("test@email.com", "test", "test"),
                User("other@email.com", "other", "other"),
            ]
        )
        db.session.commit()

        test_user = User.query.filter_by(email="test@email.com").first()
        other_user = User.query.filter_by(email="other@email.com").first()

        db.session.add_all(
            [
                Blog("test title", "test content", test_user.id),
                Blog("other title", "other content", other_user.id),
            ]
        )
        db.session.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Returns the test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Returns the test CLI runner."""
    return app.test_cli_runner()


class AuthActions:
    """Class to easily login/logout user."""

    def __init__(self, client):
        self._client = client

    def login(self, email="test@email.com", password="test", **kwargs):
        """Login user."""
        return self._client.post(
            "/auth/login",
            data={"email": email, "password": password},
            **kwargs,
        )

    def logout(self):
        """Logout user."""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """Returns a client that can login/logout."""
    return AuthActions(client)
