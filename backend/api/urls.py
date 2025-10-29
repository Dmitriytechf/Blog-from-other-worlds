from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentAPIView, PostAPIView

v1_router = DefaultRouter()
v1_router.register('post', PostAPIView, basename='post')
v1_router.register(
    r'post/(?P<post_id>\d+)/comments',
    CommentAPIView,
    basename='comments'
    )

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
