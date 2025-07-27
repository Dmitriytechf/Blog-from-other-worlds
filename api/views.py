from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import filters

from blog.models import Post, Comment
from .serializers import PostSerializers, CommentSerializers
from .permissions import IsAuthorOrReadOnly


class PostAPIView(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра постов. Доступен всем пользователям.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    # Добавляем пагинацию 
    pagination_class = LimitOffsetPagination
    # Добавляем разрешения для пользователей
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class CommentAPIView(viewsets.ModelViewSet):
    """
    API для работы с комментариями к посту.
    Только автор может редактировать/удалять свои комментарии.
    """
    serializer_class = CommentSerializers
    # Добавление кастомного пермишена
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return get_object_or_404(Post, id=self.kwargs['post_id'])
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Comment.objects.none() 
        return Comment.objects.filter(
            post_id=self.kwargs['post_id']
        ).select_related('author').order_by('created_at')
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, 
            post=self.get_post()
        )
