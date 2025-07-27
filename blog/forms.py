import re

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].label = False
        self.fields['image'].label = False
        self.fields['content'].label = False
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published', 'image']  # Какие поля включить
        widgets = {  # Как отображать поля
            'content': forms.Textarea(attrs={'rows': 8}),
        }
        labels = {  # Какие подписи использовать
            'is_published': 'Опубликовать сразу'
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if not re.search(r'[а-яА-Яa-zA-Z]', title):  # Есть хотя бы одна буква
            raise forms.ValidationError("Название должно содержать буквы!")
        return title


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_('Email'), required=True, 
                             widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}))
    captcha = CaptchaField(label="Введите текст с картинки",
                           error_messages={'invalid': _('Неправильный текст с картинки')})
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Улучшаем подсказки для полей
        self.fields['username'].widget.attrs.update({'placeholder': 'Придумайте логин'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Создайте пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})
        
        
    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),
    }
    
    username = forms.CharField(
        label=_("Имя странника"),
        error_messages={
            'required': _('Это поле обязательно для заполнения.'),
            'max_length': _('Не более 150 символов.'),
            'invalid': _('Только буквы, цифры и @/./+/-/_.'),
        },
        help_text=_('Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_.')
    )
    
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Это поле обязательно для заполнения.'),
        },
        help_text=_(
            '<h6>Каким должен быть пароль: </h6>'
            '<ul>'
            '<li>Ваш пароль не должен быть слишком похож на другую личную информацию.</li>'
            '<li>Пароль должен содержать не менее 8 символов.</li>'
            '<li>Пароль не должен быть слишком простым.</li>'
            '<li>Пароль не может состоять только из цифр.</li>'
            '</ul>'
        )
    )
    
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Это поле обязательно для заполнения.'),
        }
    )

  
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['text'].label = False
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,  
                'class': 'form-control',
                'placeholder': 'Пишите здесь...'
            }),
        }
