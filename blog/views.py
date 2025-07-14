from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,  get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CustomUserCreationForm, CommentForm
from django.utils import timezone
from django.contrib.auth import login
from django.views.generic import TemplateView


def post_blog(request):
    '''Главная страница с постами'''
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/blog.html', {'posts': posts})


def post_detail(request, slug):
    '''Страница с отдельным постом'''
    post = get_object_or_404(Post, slug=slug, is_published=True)
    comments = post.comments.all() # Все комментарии к посту
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', 
                  {'post': post,
                   'comments': comments,
                   'form': form})


class OProjectView(TemplateView):
    template_name = 'blog/o_proj.html'


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if  request.user == comment.author or request.user.is_superuser:
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', slug=post_slug)
    return redirect('post_detail', slug=post_slug)


@login_required
def create_post(request):
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

