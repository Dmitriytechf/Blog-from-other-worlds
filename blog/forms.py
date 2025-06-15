from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published']  # Какие поля включить
        widgets = {  # Как отображать поля
            'content': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {  # Какие подписи использовать
            'is_published': 'Опубликовать сразу'
        }
