from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone


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
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Если slug не задан
            self.slug = slugify(self.title)  # Генерируем из title
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-published_date']
    