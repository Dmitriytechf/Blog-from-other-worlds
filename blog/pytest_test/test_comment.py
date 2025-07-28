from http import HTTPStatus

import pytest
from django.urls import reverse

from blog.models import Comment, Like


pytestmark = pytest.mark.django_db


def test_comment_creation_authenticated_user(auth_client, post):
    """
    Тест: авторизованный пользователь может создать комментарий
    """
    comment_now = Comment.objects.count()
    url = reverse('post_detail', kwargs={'slug': post.slug})
    comment_data = {
        'text': 'Fun text'
    }
    
    response = auth_client.post(url, data=comment_data)
    
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == url
    
    assert Comment.objects.count() == comment_now + 1


def test_delete_comment_by_author(auth_client, user, comment):
    """
    Тест: автор может удалить свой комментарий
    """
    comment.author = user
    comment.save()
    
    url = reverse('delete_comment', kwargs={'comment_id': comment.id})
    response = auth_client.post(url)
    
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


def test_delete_comment_by_superuser(auth_client, user, comment):
    """
    Тест: суперпользователь может удалить любой комментарий
    """
    user.is_superuser = True
    user.save()
    
    url = reverse('delete_comment', kwargs={'comment_id': comment.id})
    response = auth_client.post(url)
    
    assert response.status_code == HTTPStatus.FOUND
    assert not Comment.objects.filter(id=comment.id).exists()


def test_delete_comment_by_other_user(auth_client, another_user, post, comment):
    """
    Тест: другой пользователь не может удалять комменты
    """
    comment = Comment.objects.create(
        post=post,
        author=another_user,
        text='another comment'
    )
    response = auth_client.post(reverse('delete_comment', kwargs={'comment_id': comment.id}))
    
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.filter(id=comment.id).exists()


def test_toggle_comment_like_authenticated(auth_client, user, comment):
    """
    Тест: авторизованный пользователь может ставить/убирать лайк
    """
    url = reverse('toggle_comment_like', kwargs={'comment_id': comment.id})
    
    # Первый запрос - ставим лайк
    response = auth_client.post(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['is_liked'] == True
    # Второй запрос - убираем лайк
    response = auth_client.post(url)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['is_liked'] == False


def test_toggle_comment_like_unauthenticated(client, user, comment):
    """
    Тест: неавторизованный пользователь может ставить/убирать лайк
    """
    likes_now = Like.objects.filter(object_id=comment.id).count()
    url = reverse('toggle_comment_like', kwargs={'comment_id': comment.id})
    
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert Like.objects.filter(object_id=comment.id).count() == likes_now
