from django import forms
from .models import Todo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TodoForm(forms.ModelForm):
    class Meta():
        model=Todo
        fields = ['title', 'task_content']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']