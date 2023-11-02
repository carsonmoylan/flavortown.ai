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
ingredient_names = ["Buckwheat", "Rice", "Quinoa"]

# Create a filter expression to check if the ingredient_name is in the list
fe = Attr('ingredient_name').is_in(ingredient_names)
#fe = Attr('ingredient_name').eq("Buckwheat");

response = table.scan(
        FilterExpression=fe        
    )

ingredient_ids = []
for item in response['Items']:
  print(item)
  ingredient_ids.append(int(item['entity_id']))

print(ingredient_ids)

