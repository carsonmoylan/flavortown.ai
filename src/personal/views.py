from django.shortcuts import render
from .forms import ImageForm, IngredientForm
from .imageClassification import getImageInfo
import json
import sys
from . import getCommonRecipes

# Create your views here.
def home_screen_view(request):
    if request.method == 'POST':
        if 'ingredients' in request.POST:
            ingredients = request.POST.getlist('ingredients')
            rec_recipes = getCommonRecipes.getRecRecipes(ingredients)

        imageForm = ImageForm(request.POST, request.FILES)
        imageName = request.FILES[u'image'].name

        if imageForm.is_valid():
            imageForm.save()
            getImageInfo(imageName)
    else:
        imageForm = ImageForm()


    return render(request, "personal/home.html", {'imageForm' : ImageForm, 'ingredientForm' : IngredientForm})
