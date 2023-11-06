from django.shortcuts import render

# Create your views here.
def home_screen_view(request):
    context = {}

    list_items = ["First item", "second item", "third item", "fourth item"]
    context["list_items"] = list_items

    return render(request, "personal/home.html", context)