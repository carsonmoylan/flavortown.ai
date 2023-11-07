from django.forms import ModelForm
from django import forms
from .models import Food

class UploadForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class' : 'ui active button'}))
    class Meta:
        model = Food
        fields = ['image']
