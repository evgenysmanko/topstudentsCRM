from django import forms
from django.forms import PasswordInput


class AuthorizationForm(forms.Form):
    login = forms.CharField(max_length=200)
    password = forms.CharField(widget=PasswordInput())
