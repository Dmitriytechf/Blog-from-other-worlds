from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import TemplateView

from .forms import CommentForm, CustomUserCreationForm, PostForm
from .models import Comment, Like, Post


def post_blog(request):
    '''Главная страница с постами'''
    search_query = request.GET.get('q', '') # получаем поисковой запрос
    # Что показываем на странице
    posts = Post.objects.filter(is_published=True).order_by('-published_date')

    # Фильтрация поиска, если запрос существует
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog.html', 
                  {'page_obj': page_obj,
                   'search_query': search_query})


def post_detail(request, slug):
    '''Страница с отдельным постом'''
    post = get_object_or_404(Post, slug=slug, is_published=True)
    next_post = Post.objects.filter(created_date__gt=post.created_date).order_by('created_date').first()
    previous_post = Post.objects.filter(created_date__lt=post.created_date).order_by('-created_date').first()

    comments = post.comments.filter(parent__isnull=True)

    # Проверка лайка для поста
    is_liked = False
    if request.user.is_authenticated:
        is_liked=post.is_liked_by(request.user)
    
    for comment in comments:
        comment._current_user = request.user
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    pass
            
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', 
                  {'post': post,
                   'user': request.user,
                   'comments': comments,
                   'form': form,
                   'is_liked': is_liked,
                   'next_post': next_post,
                   'previous_post': previous_post})


def delete_comment(request, comment_id):
    '''
    Удаляет комментарий если пользователь автор или суперюзер.
    '''
    comment = get_object_or_404(Comment, id=comment_id)
    post_slug = comment.post.slug 
    
    if  request.user == comment.author or request.user.is_superuser:
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', slug=post_slug)
    return redirect('post_detail', slug=post_slug)


class OProjectView(TemplateView):
    '''Статичная страница о проекте'''
    template_name = 'o_proj.html'


@login_required
def create_post(request):
    '''Создание поста'''
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # Временно не сохраняем
            post.author = request.user # Автоматически назначаем автора
            if post.is_published:  # Если выбрана публикация
                post.published_date = timezone.now()
            post.save()
            return redirect(post.get_absolute_url())           
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})    
    

@login_required
def edit_post(request, slug):
    '''Редактирование поста'''
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.is_published and not post.published_date:
                post.published_date = timezone.now()
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, slug):
    '''Удаление поста'''
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/blog.html', {'post': post})


def custom_page_not_found(request, exception):
    '''Кастомная 404 ошибка'''
    return render(request, '404.html', status=404)


def register(request):
    if request.method == 'POST':
        form =  CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form =  CustomUserCreationForm()
        
    return render(request, 'blog/register.html', {'form': form})


def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = Post.objects.get(id=post_id)
    content_type = ContentType.objects.get_for_model(Post)
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=post.id
    )
    if not created:
        like.delete() 
    
    return JsonResponse({
            'like_count': post.like_count,
            'is_liked': created
        })


def toggle_comment_like(request, comment_id):
    if not request.user.is_authenticated:
        return redirect('login')
    comment = Comment.objects.get(id=comment_id)
    content_type = ContentType.objects.get_for_model(Comment)
    
    like, created = Like.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=comment.id
    )
    if not created:
        like.delete() 
    
    return JsonResponse({
        'like_count': comment.like_count,
        'is_liked': created
    })
