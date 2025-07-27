from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostAPIView

v1_router = DefaultRouter()
v1_router.register('post', PostAPIView)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
