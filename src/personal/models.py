from django.db import models

# Create your models here.

class Food(models.Model):
    image = models.ImageField(upload_to='images')

class Ingredients(models.Model):
    ingredients = models.CharField(max_length=200) 