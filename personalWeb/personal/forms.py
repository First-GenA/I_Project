from django.forms import ModelForm
from django import forms
from .models import UserInfo


class Profile(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['u_avatar', 'u_name', 'u_phone', 'u_address']

    u_avatar = forms.ImageField(widget=forms.FileInput)