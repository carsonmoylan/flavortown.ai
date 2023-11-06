import os
import csv
import botocore
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')

table_compound_ingredients = 'compound_ingredients'
table_ingredients = 'ingredients'
table_recipes_by_ingredients = 'recipes_by_ingredients'
table_recipe_details = 'recipe_details'

table_ingredients = 'ingredients'

table = dynamodb.Table(table_ingredients)

# Assign this to list of ingredients to get the ids
# Use the ids to find recipes
ingredient_names = ["Banana", "Liquid Smoke", "Pork"]

# Create a filter expression to check if the ingredient_name is in the list
fe = Attr('ingredient_name').is_in(ingredient_names)
#fe = Attr('ingredient_name').eq("Buckwheat");

response = table.scan(
        FilterExpression=fe        
    )

ingredient_ids = []
for item in response['Items']:
  #print(item)
  ingredient_ids.append(int(item['entity_id']))

#print(ingredient_ids)

table = dynamodb.Table("ingredients_by_recipes")
# get the rows by searching ingredient ids
fe = Attr('ingredient_id').is_in(ingredient_ids)
response = table.scan(
  FilterExpression=fe
)
res = list()
for item in response['Items']:
  #print(item)
  test = item
  test['recipe_list'] = item['recipe_list'].split()
  res.append(test)
print(res)
# sort num_recipes
for item in res:
  print(item['num_recipes'])
res = sorted(res, key=lambda ingredient: int(ingredient['num_recipes']), reverse=True)
for item in res:
  print(item['num_recipes'])
# go through ingredients and see if there are common recipes
# final = list(("carson", "bart", "colin"))

def clean(final, temp):
  return [recipe for recipe in final if recipe in temp]

final = res[0]['recipe_list']
print("here", len(final))
for i in range(1, len(res)):
  final = clean(final, res[i]['recipe_list'])
print(final, len(final))
# temp = list(("colin", "tyler", "will"))
