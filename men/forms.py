from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from captcha.fields import CaptchaField, CaptchaTextInput

from .models import *


class AddPostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            validators=[RegexValidator(
                                            regex="(^[А-ЯЁ][а-яё]*)( [А-ЯЁ][а-яё]*){0,2}$",
                                            message='Каждое слово в заголовке должно начинаться \
                                            с большой буквы.')])
    content = forms.CharField(label='Статья', 
                              widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'


    class Meta:
        model = Men
        fields = ['title', 'content', 'photo', 'is_published', 'cat',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # в классе мета (как у пред.класса) в widgets все, кроме 1ого поля, нужно писать как сейчас через переменную,
    # иначе джанго не применяет почему-то к ним стили

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255,  widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-input', 'style': 'margin: 0px 5px'}))
