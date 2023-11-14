from django.forms import ModelForm
from django import forms
from .models import Food, Ingredients

from django import forms

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'ui active button', 'style': 'display: none;', 'id': 'imageUpload'}),
        label=''
    )

    class Meta:
        model = Food
        fields = ['image']

class IngredientForm(forms.ModelForm):
    ingredients = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'margin: 0; max-width: 100%; flex: 1 0 auto; outline: 0; -webkit-tap-highlight-color: rgba(255,255,255,0); text-align: left; line-height: 1.21428571em; font-family: "Lato", "Helvetica Neue", Arial, Helvetica, sans-serif; padding: 0.67857143em 1em; background: #fff; border: 1px solid rgba(34,36,38,.15); color: rgba(0,0,0,.87); border-radius: 0.28571429rem; transition: box-shadow .1s ease, border-color .1s ease; box-shadow: none;',
        }),
        label=''
    )

    class Meta:
        model = Ingredients
        fields = ['ingredients']


