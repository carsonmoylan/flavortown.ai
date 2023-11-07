from django.forms import ModelForm
from django import forms
from .models import Food

from django import forms

class UploadForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'ui active button', 'style': 'display: none;', 'id': 'imageUpload'}),
        label=''
    )

    class Meta:
        model = Food
        fields = ['image']

