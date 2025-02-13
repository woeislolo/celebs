from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
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
    author = forms.CharField(label='Имя',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Email',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Комментарий', 
                              widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    
    class Meta:
        model = Comment
        fields = ['author', 'email', 'content']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', 
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', 
                             widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', 
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', 
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется.')
        return data


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', 
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', 
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', 
                           max_length=255, 
                           widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', 
                             widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Сообщение', 
                              widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class': 'form-input', 
                                                          'style': 'margin: 0px 5px'}))


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32, 
                                 label='Имя',
                                 widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=32, 
                                label='Фамилия',
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(max_length=32, 
                            label='Email',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'photo']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email уже используется.')
        return data
