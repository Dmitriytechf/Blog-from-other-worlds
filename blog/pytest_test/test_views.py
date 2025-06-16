import pytest
from django.urls import reverse
from blog.models import Post
from http import HTTPStatus

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
    
    