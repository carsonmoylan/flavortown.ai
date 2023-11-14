# """
# A script to load data from text files to aws Dynamo DB
# TO RUN: UNCOMMENT ALL LINES. THIS UPLOADS ALL DATA TO DATABASE
# NOTE: RUNTIME ~1-2 HOURS FOR ALL DATA TO BE LOADED
# """
# import os
# import csv
# import boto3
# import time

# dynamodb = boto3.client('dynamodb', region_name='us-east-2')

# current_dir = os.path.dirname(os.path.abspath(__file__))
# recipe_details_file = os.path.join(current_dir, 'CulinaryDB\\01_Recipe_Details.csv')
# ingredients_file = os.path.join(current_dir, 'CulinaryDB\\02_Ingredients.csv')
# compound_ingredients_file = os.path.join(current_dir, 'CulinaryDB\\03_Compound_Ingredients.csv')
# recipe_integredients_aliases_file = os.path.join(current_dir, 'CulinaryDB\\04_Recipe-Ingredients_Aliases.csv')

# included_sources = ['FOOD_NETWORK']
# included_recipe_ids = []

# # UPLOADED
# # Populate recipe_details table
# with open(recipe_details_file, 'r', encoding='utf-8', newline='') as csv_file:
#   count = 0
#   table_name = 'recipe_details'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#             'recipe_id': {'N': row[0]},
#             'title': {'S': row[1].lower()},
#             'source': {'S': row[2].lower()},
#             'cuisine': {'S': row[3].replace('Misc.: ', '').lower()}
#         }
#     if (count == 1):
#       continue
#     if row[2] in included_sources:
#       included_recipe_ids.append(int(row[0]))
#       #print(data)
#       response = dynamodb.put_item(TableName=table_name, Item=data)


# # UPLOADED
# # Populate ingredients table
# with open(ingredients_file, 'r', encoding='utf-8', newline='') as csv_file:
#   count = 0
#   table_name = 'ingredients'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#       'entity_id': {'N': row[2]},
#       'ingredient_name': {'S': row[0].lower()},
#       'alias_ingredient_name': {'S': row[1].lower()},
#       'category': {'S': row[3].lower()}
#     }
#     if (count == 1):
#       continue
#     print(data)
#     response = dynamodb.put_item(TableName=table_name, Item=data)


# # UPLOADED
# # Populate compound_ingredients table
# with open(compound_ingredients_file, 'r', encoding='utf-8', newline='') as csv_file:
#   count = 0
#   table_name = 'compound_ingredients'
#   reader = csv.reader(csv_file)
#   for row in reader:
#     count += 1
#     data = {
#       'entity_id': {'N': row[2]},
#       'compound_ingredient_name': {'S': row[0].lower()},
#       'compound_ingredient_synonym': {'S': row[1].lower()},
#       'contituent_ingredients': {'S': row[3].lower()},
#       'category': {'S': row[4].lower()}
#     }
#     if (count == 1):
#       continue
#     print(data)
#     response = dynamodb.put_item(TableName=table_name, Item=data)


# print(len(included_recipe_ids))
# times = []
# # UPLOADED
# last_recipe_id = None
# with open(recipe_integredients_aliases_file, 'r', encoding='utf-8') as csv_file:
#   count = 0
#   table_name = 'recipes_by_ingredients'
#   reader = csv.reader(csv_file)
#   st = time.time()
#   for row in reader:
#     count += 1
#     data = {
#       'id': {'N': str(count-1)},
#       'recipe_id': {'N': row[0]},
#       'ingredient_name': {'S': row[1].lower()},
#       'aliased_ingredient_name': {'S': row[2].rstrip(' ').lower()},
#       'entity_id': {'N': row[3]}
#     }
#     if (count == 1):
#       continue
#     if int(row[0]) in included_recipe_ids:
#       #print(data)
#       response = dynamodb.put_item(TableName=table_name, Item=data)
#       current_recipe_id = int(row[0])
#       if last_recipe_id is not None and current_recipe_id != last_recipe_id:
#         print('Time for recipe ', last_recipe_id, ':', time.time() - st)
#         times.append(time.time()-st)
#         print('Avg recipe time: ', sum(times)/len(times))
#         st = time.time()
#       last_recipe_id = current_recipe_id

# # IMPORT DATA TO INGREDIENTS_BY_RECIPES
# # NOT UPLOADED
# times = []
# with open(recipe_integredients_aliases_file, 'r', encoding='utf-8') as csv_file:
#   count = 0
#   table_name = 'ingredients_by_recipes'
#   reader = csv.reader(csv_file)
#   st = time.time()
#   ingredients_dict = {}
#   for row in reader:
#     count += 1
#     if (count == 1):
#       continue
#     if int(row[0]) not in included_recipe_ids:
#       continue
#     ingredient_id = int(row[3])
#     if ingredient_id not in ingredients_dict:
#       ingredients_dict[ingredient_id] = [int(row[0])]
#     else:
#       ingredients_dict[ingredient_id].append(int(row[0]))
#   for ingredient_id in ingredients_dict:
#     data = {
#       'ingredient_id': {'N': str(ingredient_id)},
#       'num_recipes': {'N': str(len(ingredients_dict[ingredient_id]))},
#       'recipe_list': {'S': str(' '.join(map(str, ingredients_dict[ingredient_id]))).lower()}
#     }
#     print(data)
#     response = dynamodb.put_item(TableName=table_name, Item=data)
