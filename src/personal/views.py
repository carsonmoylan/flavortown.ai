from django.shortcuts import render
from .forms import ImageForm, IngredientForm
from .imageClassification import getImageInfo
import json
import sys
sys.path.append('/home/ubuntu/flavortown.ai/RecipeLoading')
import getCommonRecipes

# Create your views here.
def home_screen_view(request):
    if request.method == 'POST':
        if 'ingredients' in request.POST:
            ingredients = request.POST['ingredients']
            print(ingredients)

        imageForm = ImageForm(request.POST, request.FILES)
        imageName = request.FILES[u'image'].name
        ingredients_data = request.POST.getlist('ingredients[]')
        print(ingredients_data)
        rec_recipes = getCommonRecipes.getRecRecipes(ingredients_data)
        print(rec_recipes)

        if imageForm.is_valid():
            imageForm.save()
            getImageInfo(imageName)
    else:
        imageForm = ImageForm()


    return render(request, "personal/home.html", {'imageForm' : ImageForm, 'ingredientForm' : IngredientForm})
