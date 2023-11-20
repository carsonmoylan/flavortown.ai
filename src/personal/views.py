from django.shortcuts import render, redirect, reverse
from .forms import ImageForm, IngredientForm
from .models import Food
from .imageClassification import getImageInfo
import json
import sys
from django.conf import settings
from pathlib import Path
from . import getCommonRecipes
import time

# Create your views here.
def home_screen_view(request):
    if request.method == 'POST':
        imageForm = ImageForm(request.POST, request.FILES)
        imageName = request.FILES[u'image'].name

        if imageForm.is_valid():
            imageForm.save()
            imageInfo = getImageInfo(imageName) # Returns array of class names.
            array_param = ','.join(imageInfo)

            return redirect('display_image_with_classes', imageClasses=array_param)
    else:
        imageForm = ImageForm()

    
    return render(request, "personal/home.html", {'imageForm' : ImageForm})

def display_image(request, imageClasses):
    imageClasses = imageClasses.split(',')
    uploaded_image = Food.objects.last()
            
    return render(request, 'personal/imageView.html', {'uploaded_image': uploaded_image, 'ingredientForm' : IngredientForm, 'imageClasses' : imageClasses})

def display_recipes(request):
    rec_recipes = None
    if request.method == 'POST':
        if 'ingredients[]' in request.POST:
            ingredients = request.POST.getlist('ingredients[]')
            rec_recipes = getCommonRecipes.getRecRecipes(ingredients)
            print(f"recipes {rec_recipes}")
            return render(request, 'personal/recipesView.html', {'recipes': rec_recipes})

    if rec_recipes is None:
        data = {'recipes' : []}
    else:
        data = {'recipes' : rec_recipes}
    

    return render(request, 'personal/recipesView.html', data)

    