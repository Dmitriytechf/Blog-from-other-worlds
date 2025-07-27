from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from blog.models import Post

from .serializers import PostSerializers


class PostAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    # Добавляем пагинацию 
    pagination_class = LimitOffsetPagination
    # Добавляем разрешения для пользователей
    permission_classes = [AllowAny]
