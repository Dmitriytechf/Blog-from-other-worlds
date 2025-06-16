from django import forms
from .models import Post
from django.utils.text import slugify
import re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published', 'image']  # Какие поля включить
        widgets = {  # Как отображать поля
            'content': forms.Textarea(attrs={'rows': 5}),
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
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Имя"),
        error_messages={
            'required': _('Это поле обязательно для заполнения.'),
        }
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Улучшаем подсказки для полей
        self.fields['username'].widget.attrs.update({'placeholder': 'Придумайте логин'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Создайте пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user
        
        
    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),
    }
    
    username = forms.CharField(
        label=_("Имя пользователя"),
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