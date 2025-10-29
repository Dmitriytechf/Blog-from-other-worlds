from http import HTTPStatus

import pytest
from django.urls import reverse

from blog.models import Comment, Post

pytestmark = pytest.mark.django_db


def test_api_get_postlist(api_client):
    """
    Тест получение списка постов через API.
    """
    url = reverse('post-list')
    response = api_client.get(url)
    data = response.json()
    
    assert response.status_code == HTTPStatus.OK
    assert 'count' in data
    assert 'results' in data


def test_api_get_post_pk(auth_client, simple_post):
    """
    Тест получение конкретного поста по ID.
    """
    url = reverse('post-detail', kwargs={'pk': simple_post.pk})
    response = auth_client.get(url)
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data['title'] == simple_post.title
    assert data['content'] == simple_post.content
    

def test_api_get_commentlist_pk(api_client, post_with_comments):
    """
    Тест проверяет:
    1. Получение списка комментариев для поста
    2. Доступ без авторизации
    3. Корректное количество комментариев
    """
    url = reverse('comments-list', kwargs={
        'post_id': post_with_comments.pk
    })
    response = api_client.get(url)
    data = response.json()
    
    assert response.status_code == HTTPStatus.OK
    assert data['count'] == 2
    assert data['results'][0]['text'] == "First comment"
    assert data['results'][1]['text'] == "Second comment"



def test_api_get_comment_pk(api_client, post_with_comments):
    """Тест првоеряет: 
    1. Анонимный пользователь может получить один комментарий
    2. Текст комментария совпадает с оригиналом
    """
    comment = Comment.objects.first()
    url = reverse('comments-detail', kwargs={
        'post_id': post_with_comments.pk,
        'pk': comment.pk
    })
    response = api_client.get(url)
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()['text'] == comment.text


def test_create_comment_authenticated(auth_client, post_with_comments):
    """
    Тест успешного создания комментария авторизованным пользователем
    """
    now_count = Comment.objects.count()
    url = reverse('comments-list', kwargs={'post_id': post_with_comments.pk})
    data = {
        'text': 'New test comment'
    }
    response = auth_client.post(url, data)
    
    assert response.status_code == HTTPStatus.CREATED
    assert Comment.objects.count() == now_count + 1
    assert response.json()['text'] == data['text']


def test_create_comment_unauthenticated(api_client, post_with_comments):
    """
    Тест попытки создания комментария без авторизации
    """
    now_count = Comment.objects.count()
    url = reverse('comments-list', kwargs={'post_id': post_with_comments.pk})
    data = {
        'text': 'Anon test comment'
    }
    response = api_client.post(url, data)
    
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert Comment.objects.count() == now_count
