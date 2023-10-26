# A script to load data from text files to aws Dynamo DB
import os
import csv
import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-2')

current_dir = os.path.dirname(os.path.abspath(__file__))
recipe_details_file = os.path.join(current_dir, 'CulinaryDB\\01_Recipe_Details.csv')
ingredients_file = os.path.join(current_dir, 'CulinaryDB\\02_Ingredients.csv')
compound_ingredients_file = os.path.join(current_dir, 'CulinaryDB\\03_Compound_Ingredients.csv')
recipe_integredients_aliases_file = os.path.join(current_dir, 'CulinaryDB\\04_Recipe-Ingredients_Aliases.csv')

included_sources = ['FOOD_NETWORK']
included_recipe_ids = []

# UPLOADED
# Populate recipe_details table
# with open(recipe_details_file, 'r', encoding='utf-8', newline='') as csv_file:
#   count = 0
#   table_name = 'recipe_details'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#             'recipe_id': {'N': row[0]},
#             'title': {'S': row[1]},
#             'source': {'S': row[2]},
#             'cuisine': {'S': row[3].replace('Misc.: ', '')}
#         }
#     if (count == 1):
#       continue
#     if row[2] in included_sources:
#       included_recipe_ids.append(int(row[0]))
#       print(data)
#       response = dynamodb.put_item(TableName=table_name, Item=data)


# UPLOADED
# Populate ingredients table
# with open(ingredients_file, 'r', encoding='utf-8', newline='') as csv_file:
#   count = 0
#   table_name = 'ingredients'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#       'entity_id': {'N': row[2]},
#       'ingredient_name': {'S': row[0]},
#       'alias_ingredient_name': {'S': row[1]},
#       'category': {'S': row[3]}
#     }
#     if (count == 1):
#       continue
#     print(data)
#     response = dynamodb.put_item(TableName=table_name, Item=data)


# UPLOADED
# Populate compound_ingredients table
# with open(compound_ingredients_file, 'r', encoding='utf-8', newline='') as csv_file:
#   count = 0
#   table_name = 'compound_ingredients'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#       'entity_id': {'N': row[2]},
#       'compound_ingredient_name': {'S': row[0]},
#       'compound_ingredient_synonym': {'S': row[1]},
#       'contituent_ingredients': {'S': row[3]},
#       'category': {'S': row[4]}
#     }
#     if (count == 1):
#       continue
#     print(data)
#     response = dynamodb.put_item(TableName=table_name, Item=data)

# # NOT UPLOADED
# with open(recipe_integredients_aliases_file, 'r', encoding='utf-8') as csv_file:
#   count = 0
#   table_name = 'recipes_by_ingredients'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#       'id': {'N': str(count-1)},
#       'recipe_id': {'N': row[0]},
#       'ingredient_name': {'S': row[1]},
#       'aliased_ingredient_name': {'S': row[2].rstrip(' ')},
#       'entity_id': {'N': row[3]}
#     }
#     if (count == 1):
#       continue
#     if (int(row[0]) in included_recipe_ids):
#       print(data)
#       response = dynamodb.put_item(TableName=table_name, Item=data)
