from django.shortcuts import render, redirect, reverse
from django.core.files.storage import default_storage
from django.utils.text import slugify
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

        if imageForm.is_valid():
            imageForm.save()
            imageName =  Food.objects.last().name
            imageInfo = getImageInfo(imageName) # Returns array of class names.
            array_param = ','.join(imageInfo)
            request.session['image_classes'] = array_param

            return redirect('display_image')
    else:
        imageForm = ImageForm()
    
    return render(request, "personal/home.html", {'imageForm' : ImageForm})

def display_image(request):
    imageClasses = request.session.get('image_classes', '').split(',')
    uploaded_image = Food.objects.last()

    if request.method == 'POST':
        if 'ingredients[]' in request.POST:
            ingredients = request.POST.getlist('ingredients[]')
            rec_recipes = getCommonRecipes.getRecRecipes(ingredients)
            print(f"recipes {rec_recipes}")
            request.session['recipes'] = rec_recipes
            
            # Delete image after use
            image_path = uploaded_image.image.path
            default_storage.delete(image_path)

            
    return render(request, 'personal/imageView.html', {'uploaded_image': uploaded_image, 'ingredientForm' : IngredientForm, 'imageClasses' : imageClasses})

def display_recipes(request):
    recipes = request.session.get('recipes', [])

    return render(request, 'personal/recipesView.html', {'recipes': recipes})


    