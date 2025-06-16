import pytest
from blog.models import Post
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.fixture
def user():
    """Фикстура: создает тестового пользователя."""
    return User.objects.create_user(
        username='testuser',
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