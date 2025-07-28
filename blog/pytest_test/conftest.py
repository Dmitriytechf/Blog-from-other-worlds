import pytest
from django.contrib.auth import get_user_model

from blog.models import Post, Comment

User = get_user_model()


@pytest.fixture
def user():
    """Фикстура: создает тестового пользователя."""
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def auth_client(client, user):
    """Фикстура: возвращает аутентифицированный клиент"""
    client.force_login(user=user)
    return client


@pytest.fixture
def another_user():
    """Другой тестовый пользователь"""
    return User.objects.create_user(
        username='otheruser',
        password='testpass123'
    )


@pytest.fixture
def post(user):
    """Фикстура: создает опубликованный пост"""
    return Post.objects.create(
        title='Test Post',
        slug='test-post',
        content='Test content',
        author=user,
        is_published=True
    )


@pytest.fixture
def unpublished_post(user):
    """Фикстура: создает неопубликованный пост"""
    return Post.objects.create(
        title='Unpublished Post',
        slug='unpublished-post',
        content='Unpublished content',
        author=user,
        is_published=False
    )


@pytest.fixture
def comment(user, post):
    return Comment.objects.create(
        post=post,
        author=user,
        text='Test comment text'
    )
