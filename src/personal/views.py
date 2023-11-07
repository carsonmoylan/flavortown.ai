from django.shortcuts import render
from .forms import UploadForm
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

        #form = UploadForm(request.POST, request.FILES)
        #imageName = request.FILES[u'image'].name
        ingredients_data = request.POST.getlist('ingredients[]')
        print(ingredients_data)
        rec_recipes = getCommonRecipes.getRecRecipes(ingredients_data)
        print(rec_recipes)

        #if form.is_valid():
            #form.save()
            #getImageInfo(imageName)
    else:
        form = UploadForm()


    return render(request, "personal/home.html", {'form' : UploadForm})
