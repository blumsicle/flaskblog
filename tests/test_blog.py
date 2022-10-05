"""Test the blog routes."""

import pytest
from flask_login import current_user
from smoothblog.models import Blog, User


def test_index(client):
    """
    GIVEN a test client
    WHEN a request to "/" is made
    THEN it should redirect to "/home"
    """
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"


def test_home(client):
    """
    GIVEN a test client
    WHEN a request to "/home" is made
    THEN it should display the home page
    """
    response = client.get("/home")
    assert response.status_code == 200
    assert "Welcome to Smoothblog!" in response.text


def test_about(client):
    """
    GIVEN a test client
    WHEN a request to "/about" is made
    THEN it should display the about page
    """
    response = client.get("/about")
    assert response.status_code == 200
    assert "About Us" in response.text


def test_create_not_logged_in(client):
    """
    GIVEN a test client not logged in
    WHEN a request to "/create" is made
    THEN it should redirect to "/auth/login" with info message
    """
    response = client.get("/create", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/auth/login"
    assert "Please log in to access this page" in response.text


def test_delete_not_logged_in(client):
    """
    GIVEN a test client not logged in
    WHEN a request to "/delete/1" is made
    THEN it should redirect to "/auth/login" with info message
    """
    response = client.get("/delete/1", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/auth/login"
    assert "Please log in to access this page" in response.text


def test_create_logged_in(client, auth):
    """
    GIVEN a test client loggged in
    WHEN a request to "/create" is made
    THEN it should display the create page
    """
    auth.login()
    response = client.get("/create")
    assert "Create a Blog" in response.text


def test_create_logged_in_post(client, auth):
    """
    GIVEN a test client loggged in
    WHEN a post request to "/create" is made
    THEN it should create a blog
    """
    title = "This is the new test blog"
    content = "This is some content"

    with client:
        auth.login()
        assert not Blog.query.filter_by(title=title).all()
        response = client.post(
            "/create",
            data={"title": title, "content": content},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.request.path == "/home"
        assert "Blog successfully created!" in response.text
        assert Blog.query.filter_by(title=title).first()


@pytest.mark.parametrize(
    ("title", "content", "message"),
    [
        ("", "content", "title: This field is required"),
        ("title", "", "content: This field is required"),
    ],
)
def test_create_post_validate_input(client, auth, title, content, message):
    """
    GIVEN a test client
    WHEN a post request to "/create" is made with invalid data
    THEN it should display an error
    """
    auth.login()
    response = client.post("/create", data={"title": title, "content": content})
    assert message in response.text


def test_delete_logged_in_matches(client, auth):
    """
    GIVEN a test client loggged in
    WHEN a request to "/delete/<logged in user blog id>" is made
    THEN it should delete the blog
    """
    with client:
        auth.login()
        blog = Blog.query.filter_by(user_id=current_user.id).first()
        client.get(f"/delete/{blog.id}")
        assert Blog.query.get(blog.id) is None


def test_delete_logged_in_not_matches(client, auth):
    """
    GIVEN a test client loggged in
    WHEN a request to "/delete/<other user blog id>" is made
    THEN it should redirect to "/home" and not delete blog
    """
    with client:
        auth.login()
        other_user = User.query.filter_by(email="other@email.com").first()
        blog = Blog.query.filter_by(user_id=other_user.id).first()
        response = client.get(f"/delete/{blog.id}", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/home"
        assert "Blog cannot be deleted" in response.text
        assert Blog.query.get(blog.id) is not None
