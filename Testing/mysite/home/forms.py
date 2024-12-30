from dataclasses import field, fields
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django import forms

class SignUpForm(UserCreationForm):
    gender = forms.CharField(
        max_length= 7
    )

    contact = forms.CharField(
        max_length=11
    )
    class Meta:
        model = MyUser
        fields="__all__"