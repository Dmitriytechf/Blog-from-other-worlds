from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,  get_object_or_404
from .models import Post
from .forms import PostForm
from django.utils import timezone


def post_blog(request):
    '''Главная страница с постами'''
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/blog.html', {'posts': posts})


def post_detail(request, slug):
    '''Страница с отдельным постом'''
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
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
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/blog.html', {'post': post})
    
    
def custom_page_not_found(request, exception):
    '''Кастомная 404 ошибка'''
    return render(request, '404.html', status=404)
