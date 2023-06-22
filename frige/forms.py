from django import forms
from .models import Frige

class FrigeForm(forms.ModelForm):
    class Meta:
        model = Frige
        fields = ['name']