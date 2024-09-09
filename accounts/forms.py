from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Authors,Article,NewUser,Login
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter author details'}),
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            'author_name': forms.Select(attrs={'class': 'form-control'}),
            'article_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article name'}),
            'article_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'article_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your article here'}),
            'published_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }
        help_texts = {
            'username': None,  # Remove help text for username
            'password1': None,  # Remove help text for password1
            'password2': None,  # Remove help text for password2
        }
        error_messages = {
            'password_mismatch': {
                'message': 'Passwords must match.',
            },
            'password2': {
                'required': 'Please confirm your password.',
            },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2



class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = "__all__"
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        }
