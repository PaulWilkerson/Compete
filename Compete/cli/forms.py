from django.contrib.auth.forms import UserCreationForm as UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import Account

class CompetitorSignup(UserCreationForm):
    username = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=PasswordInput, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('firstname', 'lastname', 'about', 'website')