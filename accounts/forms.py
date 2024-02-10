from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Логин'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control mb-2', 'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']
