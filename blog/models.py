from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


User = get_user_model() 
        
        
class Post(models.Model):
    '''Класс модели постов'''
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=33, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User,  on_delete=models.CASCADE, verbose_name="Автор")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Изображение")
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Если slug не задан
            self.slug = slugify(self.title)  # Генерируем из title
            
            if not self.slug:
                self.slug = f"post-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            # Делаем slug уникальным
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-published_date']


class Comment(models.Model):
    '''Класс комментарие к постам'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} - {self.post}'
