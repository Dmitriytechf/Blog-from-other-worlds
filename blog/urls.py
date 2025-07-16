from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', post_blog, name='home'),
    
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('create/', create_post, name='create_post'),
    path('oproject', OProjectView.as_view() , name='o_proj'),
    path('post/<slug:slug>/edit/', edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', toggle_like, name='toggle_like'),
    path('comment/<int:comment_id>/like/', toggle_comment_like, name='toggle_comment_like'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

