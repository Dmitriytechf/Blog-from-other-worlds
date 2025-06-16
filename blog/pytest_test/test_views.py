import pytest
from django.urls import reverse
from blog.models import Post
from http import HTTPStatus


@pytest.mark.django_db
def test_post_blog_view(client):
    '''Тест захода на главную странцу'''
    url = reverse('home')
    response = client.get(url)
    
    assert response.status_code == HTTPStatus.OK