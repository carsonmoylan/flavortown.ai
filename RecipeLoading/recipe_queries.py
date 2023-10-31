import os
import csv
import boto3
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.client('dynamodb', region_name='us-east-2')

table_compound_ingredients = 'compound_ingredients'
table_ingredients = 'ingredients'
table_recipes_by_ingredients = 'recipes_by_ingredients'
table_recipe_details = 'recipe_details'

response = dynamodb.scan(
    TableName=table_ingredients,
    FilterExpression=Attr('ingredient_name').eq('pepper')
)

items = response['Items']
for item in items:
    print("Item:", item)