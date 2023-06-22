from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import CustomUser


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
