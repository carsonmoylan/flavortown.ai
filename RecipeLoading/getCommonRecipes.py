import os
import csv
import botocore
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')

# test list of ingredients



def getIngredientIds(ingredients):
  """
  param: ingredient_names a list of english words for ingredients
  return: a list of ingredient ids corresponding to the given ingredients
  """
  ingredient_table = dynamodb.Table('ingredients')
  fe = Attr('ingredient_name').is_in(ingredients)
  response = ingredient_table.scan(FilterExpression=fe)
  ingredient_ids = []
  for item in response['Items']:
    ingredient_ids.append(int(item['entity_id']))
  return ingredient_ids


def clean(final, temp):
  """
  params: final: a list of recipe ids to dwindle down
          temp: a list of recipe ids to check if they are in final
  return: return the intersection of final and temp
  """
  return [recipe for recipe in final if recipe in temp]


def getRecipeIds(ingredient_ids):
  """
  params: ingredient_ids: a list of recipe_ids to see what recipes are shared with all of them
  return: a list of recipe ids that have every ingredient given
  """
  table = dynamodb.Table("ingredients_by_recipes")
  # get the rows by searching ingredient ids
  fe = Attr('ingredient_id').is_in(ingredient_ids)  # Updated here
  response = table.scan(FilterExpression=fe)
  res = list()
  for item in response['Items']:
    test = item
    test['recipe_list'] = item['recipe_list'].split()
    res.append(test)
  res = sorted(res, key=lambda ingredient: int(ingredient['num_recipes']), reverse=True)
  final = res[0]['recipe_list']
  for i in range(1, len(res)):
    final = clean(final, res[i]['recipe_list'])
  return final


def getRecipeNames(recipe_ids):
  """
  params: recipe_ids: a list of recipe ids
  return: a list of english names for each recipe
  """
  print(recipe_ids)
  table = dynamodb.Table("recipe_details")
  # get the rows by searching ingredient ids
  fe = Attr('recipe_id').is_in(recipe_ids)
  response = table.scan(
    FilterExpression=fe
  )
  recipes = list()
  for item in response['Items']:
    recipes.append(item['title'].title())
  return recipes

def getRecRecipes(ingredients):
  ingredient_ids = getIngredientIds(ingredients)
  recipe_ids = getRecipeIds(ingredient_ids)
  recipe_ids = [int(recipe_id) for recipe_id in recipe_ids]
  return getRecipeNames(recipe_ids)

def main():
  ingredient_names = ["banana", "liquid smoke", "pork"]
  print(getRecRecipes(ingredient_names))

if __name__ == '__main__':
  main()