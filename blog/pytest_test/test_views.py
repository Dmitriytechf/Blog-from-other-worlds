from http import HTTPStatus

import pytest
from django.urls import reverse

from blog.models import Post


pytestmark = pytest.mark.django_db


def test_post_blog_view(client):
    '''Тест захода на главную странцу'''
    url = reverse('home')
    response = client.get(url)
    
    assert response.status_code == HTTPStatus.OK
    
    
def test_post_detail_view_with_valid_slug(client, post):
    """
    Возвращает опубликованный пост по корректному slug.
    """
    url = reverse('post_detail', kwargs={'slug': post.slug})
    response = client.get(url)
    
    assert response.status_code == HTTPStatus.OK
    assert response.context['post'] == post
    

def test_post_detail_view_with_invalid_slug(client):
    """
    Возвращает 404 для несуществующего slug.
    """
    url = reverse('post_detail', kwargs={'slug': 'non-existent-slug'})
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_post_auth_user(auth_client, user):
    """
    Тест: авторизованный пользователь может опубликовать пост
    """
    url = reverse('create_post')
    post_data = {
        'title': 'New Post',
        'slug': 'new-post',
        'content': 'Test Bla Bla',
        'is_published': True
    }
    
    response = auth_client.post(url, data=post_data)
    assert response.status_code == HTTPStatus.FOUND
    
    post = Post.objects.get(slug='new-post')
    assert post.title == 'New Post'
    assert post.content == post_data['content']
    assert post.author == user
    assert post.is_published is True
    assert post.published_date is not None


def test_create_post_anon_user(client):
    """
    Тест: авторизованный пользователь может опубликовать пост
    """
    url = reverse('create_post')
    response = client.get(url)
    
    assert response.status_code == HTTPStatus.FOUND
    assert 'login' in response.url


def test_edit_post_by_author(auth_client, user, post):
    """
    Тест: автор может редактировать свой пост
    """
    url = reverse('edit_post', kwargs={'slug': post.slug})
    edit_data = {
        'title': 'Edit Title',
        'slug': 'edit-slug',
        'content': 'Updated content',
        'is_published': True
    }
    
    response = auth_client.post(url, data=edit_data)
    
    assert response.status_code == HTTPStatus.FOUND
    
    post.refresh_from_db()
    assert post.title == edit_data['title']
    assert post.content == edit_data['content']
    assert post.slug == edit_data['slug']
    assert post.is_published == edit_data['is_published']
    assert post.is_published is True


def test_edit_post_by_other_author(auth_client, user, another_user, post):
    """
    Тест: автор может редактировать свой пост
    """
    post.author = another_user
    post.save()

    url = reverse('edit_post', kwargs={'slug': post.slug})
    edit_data = {
        'title': 'Edit Title',
        'slug': 'edit-slug',
        'content': 'Updated content',
        'is_published': True
    }
    
    response = auth_client.post(url, data=edit_data)
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    
    post.refresh_from_db()
    assert post.title != edit_data['title']
    assert post.content != edit_data['content']
    assert post.slug != edit_data['slug']



def test_delete_post_by_author(auth_client, user, post):
    """
    Тест: автор может удалить свой пост
    """
    url = reverse('delete_post', kwargs={'slug': post.slug})
    assert Post.objects.filter(id=post.id).exists()
    
    response = auth_client.post(url)

    assert response.status_code == HTTPStatus.FOUND
    assert not Post.objects.filter(id=post.id).exists()


def test_delete_post_by_other_user(auth_client, another_user, post):
    """
    Тест: другой пользователь не может удалить чужой пост
    """
    post.author = another_user
    post.save()
    
    url = reverse('delete_post', kwargs={'slug': post.slug})
    assert Post.objects.filter(id=post.id).exists()
    
    response = auth_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Post.objects.filter(id=post.id).exists()
