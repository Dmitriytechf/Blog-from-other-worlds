from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from blog.models import Comment, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializers, PostSerializers


class PostAPIView(viewsets.ReadOnlyModelViewSet):
    """
    API для просмотра списка постов или конкретного поста. 
    Доступен всем пользователям.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    # Добавляем пагинацию 
    pagination_class = LimitOffsetPagination
    # Добавляем разрешения для пользователей
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    # Кешируем данные API
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CommentAPIView(viewsets.ModelViewSet):
    """
    API для работы с комментариями к посту.
    Только автор может редактировать/удалять/создавать
    свои комментарии. Нужна авторизация для выполнения действий
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

    # Кешируем данные API
    @method_decorator(cache_page(33))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(33))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
