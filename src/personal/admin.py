from django.contrib import admin
from .models import Food
# Register your models here.


class imageAdmin(admin.ModelAdmin):
    list_display = ["image"]

admin.site.register(Food, imageAdmin)
