from django.contrib.auth.forms import UserCreationForm as UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import Account

class CompetitorSignup(UserCreationForm):
    username = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class UpdateProfile(forms.ModelForm):
    firstname = forms.CharField(
        max_length=40, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
            'class': 'form-control'
        })
    )
    lastname = forms.CharField(
        max_length=40, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name',
            'class': 'form-control'
        })
    )
    about = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about yourself and your cybersecurity interests...',
            'class': 'form-control',
            'rows': 5
        })
    )
    website = forms.URLField(
        max_length=90, 
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://yourwebsite.com',
            'class': 'form-control'
        })
    )
    class Meta:
        model = Account
        fields = ('firstname', 'lastname', 'about', 'website')