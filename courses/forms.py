from django import forms
from .models import Article, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'youtube_link', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'youtube_link': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select bg-dark text-light'
            })
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light'
            })
        }

