from django.shortcuts import render
from .forms import UploadForm
from .imageClassification import getImageInfo

# Create your views here.
def home_screen_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        imageName = request.FILES[u'image'].name
        if form.is_valid():
            form.save()
            getImageInfo(imageName)
    else:
        form = UploadForm()



    return render(request, "personal/home.html", {'form' : UploadForm})
