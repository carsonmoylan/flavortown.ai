# A script to load data from text files to aws Dynamo DB

import os
import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-2')

table_name = 'ingredients'

# # Prepare data in the required format
# data = {
#     'id': {'N': '1'},
#     'name': {'S': 'example'},
#     # Add other attributes as needed
# }

recipe_details_file = 'C:\\Users\\tyler\\\Desktop\\Uky\\F23\\CS498\\Project\\flavortown.ai\\RecipeLoading\\01_Recipe_Details.csv'
ingredients_file = 'C:\\Users\\tyler\\\Desktop\\Uky\\F23\\CS498\\Project\\flavortown.ai\\RecipeLoading\\02_Ingredients.csv'
compound_ingredients_file = 'C:\\Users\\tyler\\\Desktop\\Uky\\F23\\CS498\\Project\\flavortown.ai\\RecipeLoading\\03_Compound_Ingredients.csv'
recipe_integredients_aliases_file = 'C:\\Users\\tyler\\\Desktop\\Uky\\F23\\CS498\\Project\\flavortown.ai\\RecipeLoading\\04_Recipe-Ingredients_Aliases.csv'

current_dir = os.path.dirname(os.path.abspath(__file__))
recipe_details_file = os.path.join(current_dir, 'CulinaryDB\\01_Recipe_Details.csv')
ingredients_file = os.path.join(current_dir, 'CulinaryDB\\02_Ingredients.csv')
compound_ingredients_file = os.path.join(current_dir, 'CulinaryDB\\03_Compound_Ingredients.csv')
recipe_integredients_aliases_file = os.path.join(current_dir, 'CulinaryDB\\04_Recipe-Ingredients_Aliases.csv')
# print(recipe_details_file)

# with open(recipe_details_file, 'r', encoding='utf-8') as file:
#   for line in file:
#     print(line)
count = 0
with open(ingredients_file, 'r', encoding='utf-8') as file:
  for line in file:
    count += 1
    #print(',' in line)
    print(line.strip('\n'))
    items = line.strip('\n').split(',')
    print(items)
    data = {
      'entity_id': {'N': items[2]},
      'ingredient_name': {'S': items[0]},
      'alias_ingredient_name': {'S': items[1]},
      'category': {'S': items[3]}
    }
    if (count == 1):
      continue
    response = dynamodb.put_item(TableName=table_name, Item=data)
    if count == 100:
      break

# with open(compound_ingredients_file, 'r', encoding='utf-8') as file:
#   for line in file:
#     print(line)

# with open(recipe_integredients_aliases_file, 'r', encoding='utf-8') as file:
#   for line in file:
#     print(line)

