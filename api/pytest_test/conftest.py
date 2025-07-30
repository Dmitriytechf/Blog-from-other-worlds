import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from blog.models import Comment, Post


@pytest.fixture
def user():
    """Создаем тестового пользователя"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def api_client():
    """Фикстура для создания API клиента."""
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    """Создаёт авторизованный API клиент."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def simple_post(user):
    """Фикстура создает и возвращает тестовый пост."""
    return Post.objects.create(
        title='Simple post', 
        content='Bla-bla post',
        author=user
    )


@pytest.fixture
def post_with_comments(user):
    """Создания поста вместе с комментариями"""
    post = Post.objects.create(title="Test Post", content="Test Content", author=user)
    
    author1 = User.objects.create_user(username="commenter1", password="test123")
    author2 = User.objects.create_user(username="commenter2", password="test123")
    
    Comment.objects.create(post=post, author=author1, text="First comment")
    Comment.objects.create(post=post, author=author2, text="Second comment")
    
    return post
