"""Test the auth routes."""

import pytest
from flask_login import current_user
from smoothblog.models import Blog, User


def test_register(client):
    """
    GIVEN a test client
    WHEN a request to "/auth/register" is made
    THEN it should display the login page
    """
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert "Register a new account" in response.text


@pytest.mark.parametrize(
    ("email", "username", "password", "confirm", "message"),
    [
        ("", "newuser", "123", "123", "email: This field is required"),
        ("invalid", "newuser", "123", "123", "email: Invalid email address"),
        ("newuser@email.com", "", "123", "123", "username: This field is required"),
        ("newuser@email.com", "newuser", "", "123", "password: This field is required"),
        ("newuser@email.com", "newuser", "123", "", "confirm: This field is required"),
        (
            "newuser@email.com",
            "newuser",
            "123",
            "456",
            "password: Field must be equal to confirm",
        ),
    ],
)
def test_register_post_validate_input(
    client, email, username, password, confirm, message
):
    """
    GIVEN a test client
    WHEN a post request to "/auth/register" is made with invalid data
    THEN it should display an error
    """
    response = client.post(
        "/auth/register",
        data={
            "email": email,
            "username": username,
            "password": password,
            "confirm": confirm,
        },
        follow_redirects=True,
    )
    assert message in response.text


def test_register_post(client):
    """
    GIVEN a test client
    WHEN a post request to "/auth/register" is made
    THEN it should create the user
    """
    email = "newuser@email.com"

    with client:
        client.get("/auth/register")
        assert not User.query.filter_by(email=email).first()

        response = client.post(
            "/auth/register",
            data={
                "email": email,
                "username": "newuser",
                "password": "newpassword",
                "confirm": "newpassword",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert response.request.path == "/home"
        assert "Welcome, newuser!" in response.text
        assert User.query.filter_by(email=email).first()


def test_register_post_existing_user(client):
    """
    GIVEN a test client
    WHEN a post request to "/auth/register" is made for existing user
    THEN it should display an error message
    """
    email = "test@email.com"

    with client:
        client.get("/auth/register")
        assert User.query.filter_by(email=email).first()

        response = client.post(
            "/auth/register",
            data={
                "email": email,
                "username": "newuser",
                "password": "newpassword",
                "confirm": "newpassword",
            },
            follow_redirects=True,
        )

        assert "User with the same username or email already exists" in response.text


def test_login(client):
    """
    GIVEN a test client
    WHEN a request to "/auth/login" is made
    THEN it should display the login page
    """
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert "Login to your account" in response.text


def test_login_post(client, auth):
    """
    GIVEN a test client
    WHEN a post request to "/auth/login" is made
    THEN it should log the user in
    """
    with client:
        auth.login()
        assert current_user.is_authenticated


def test_login_already_logged_in(client, auth):
    """
    GIVEN a logged in test client
    WHEN a request to "/auth/login" is made
    THEN it should redirect to "/home" with info message
    """
    auth.login()
    response = client.get("/auth/login", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"
    assert "You are already logged in" in response.text


def test_login_admin(client, auth):
    """
    GIVEN a test client
    WHEN a post request to "/auth/login" is made for admin
    THEN it should log the admin user in
    """
    with client:
        auth.login("admin@email.com", "admin")
        assert current_user.is_authenticated
        assert current_user.is_admin


@pytest.mark.parametrize(
    ("email", "password", "message"),
    [
        ("invalid@email.com", "123", "User does not exist"),
        ("test@email.com", "invalid", "Incorrect password, try again"),
        ("", "123", "email: This field is required"),
        ("invalid", "123", "email: Invalid email address"),
        ("test@email.com", "", "password: This field is required"),
    ],
)
def test_login_post_validate_input(auth, email, password, message):
    """
    GIVEN a test client
    WHEN a post request to "/auth/login" is made with invalid data
    THEN it should display an error
    """
    response = auth.login(email, password)
    assert message in response.text


def test_logout(client, auth):
    """
    GIVEN a logged in test client
    WHEN a request to "/auth/logout" is made
    THEN it should log the user out
    """
    with client:
        auth.login()
        assert current_user.is_authenticated
        auth.logout()
        assert not current_user.is_authenticated


def test_logout_not_logged_in(client):
    """
    GIVEN a non logged in test client
    WHEN a request to "/auth/logout" is made
    THEN it should redirect to "/auth/login" with info message
    """
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/auth/login"
    assert "Please log in to access this page" in response.text


def test_admin_not_admin_user(client, auth):
    """
    GIVEN a logged in non-admin test client
    WHEN a request to "/auth/admin" is made
    THEN it should redirect to "/home" with info message
    """
    with client:
        auth.login()
        response = client.get("/auth/admin", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/home"
        assert "You do not have permissions to access that page" in response.text


def test_admin_not_logged_in(client):
    """
    GIVEN a test client
    WHEN a request to "/auth/admin" is made
    THEN it should redirect to "/home" with info message
    """
    response = client.get("/auth/admin", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/auth/login"
    assert "Please log in to access this page" in response.text


def test_admin_logged_in(auth):
    """
    GIVEN a logged in admin test client
    WHEN a request to "/auth/admin" is made
    THEN it should display the page
    """
    response = auth.login("admin@email.com", "admin", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/auth/admin"
    assert "Users" in response.text


def test_delete_not_admin_user(client, auth):
    """
    GIVEN a logged in non-admin test client
    WHEN a request to "/auth/admin/delete/<user_id>" is made
    THEN it should redirect to "/home" with info message
    """
    with client:
        auth.login()
        response = client.get("/auth/admin/delete/2", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/home"
        assert "You do not have permissions to access that page" in response.text


def test_delete_admin_user(client, auth):
    """
    GIVEN a logged in admin test client
    WHEN a request to "/auth/admin/delete/<user_id>" is made
    THEN it should delete the user and associated blog posts
    """
    with client:
        auth.login("admin@email.com", "admin")
        user = User.query.filter_by(email="test@email.com").first()
        assert user
        assert Blog.query.filter_by(user_id=user.id).all()

        client.get(f"/auth/admin/delete/{user.id}")
        assert not Blog.query.filter_by(user_id=user.id).all()
        assert not User.query.get(user.id)


def test_delete_admin_user_non_existent_user(client, auth):
    """
    GIVEN a logged in admin test client
    WHEN a request to "/auth/admin/delete/<non_existent_user_id>" is made
    THEN it should redirect to "/auth/admin" and display an error message
    """
    non_existent_user_id = 1000

    with client:
        auth.login("admin@email.com", "admin")
        assert not User.query.get(non_existent_user_id)
        response = client.get(
            f"/auth/admin/delete/{non_existent_user_id}", follow_redirects=True
        )
        assert response.status_code == 200
        assert response.request.path == "/auth/admin"
        assert "User does not exist" in response.text
