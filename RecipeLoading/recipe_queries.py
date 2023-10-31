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
ingredient_name_to_query = 'Buckwheat'  # Replace with the ingredient name you want to query

table = dynamodb.Table(table_ingredients)

fe = Attr('ingredient_name').eq("Buckwheat");

response = table.scan(
        FilterExpression=fe        
    )
for item in response['Items']:
  print(item)