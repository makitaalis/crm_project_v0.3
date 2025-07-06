from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'is_blocked']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'is_blocked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }