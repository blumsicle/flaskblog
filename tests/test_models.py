"""Test the database models."""

from smoothblog.models import Blog, User


def test_user_model():
    """
    GIVEN a test app
    WHEN a User model is created
    THEN it should be represented properly
    """
    email = "test@email.com"
    username = "test"
    password = "password"
    user = User(email, username, password)

    assert user.email == email
    assert user.username == username
    assert user.password != "test"
    assert repr(user) == "<User test@email.com>"


def test_blog_model():
    """
    GIVEN a test app
    WHEN a Blog model is created
    THEN it should be represented properly
    """
    title = "Blog title"
    content = "Blog content"
    user_id = 1
    blog = Blog(title, content, user_id)

    assert blog.title == title
    assert blog.content == content
    assert blog.user_id == user_id
    assert repr(blog) == f"<Blog {title}>"
