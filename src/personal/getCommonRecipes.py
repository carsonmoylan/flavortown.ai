import os
import csv
import botocore
import boto3
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

dynamodb = boto3.resource('dynamodb')

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
  newList = [recipe for recipe in final if recipe in temp]
  if len(newList) == 0:
    return final
  else:
    return newList


def getRecipeIdsIntersection(ingredient_ids):
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


def getRecipeIdsUnion(ingredient_ids):
  """
  params: ingredient_ids: a list of ingredient ids
  return: the union of all recipe ids for the ingredient ids passed
  """
  table = dynamodb.Table("ingredients_by_recipes")
  # get the rows by searching ingredient ids
  fe = Attr('ingredient_id').is_in(ingredient_ids)
  response = table.scan(FilterExpression=fe)
  res = []
  for item in response['Items']:
    test = item
    test['recipe_list'] = item['recipe_list'].split()
    for recipe in test['recipe_list']:
      if int(recipe) not in res:
        res.append(int(recipe))
  return res

def getRecipeIngredients(recipe_ids):
  table = dynamodb.Table('recipes_by_ingredients')

  # Initialize the result dictionary
  recipes_by_ingredients = {}

  # Initialize the ExclusiveStartKey to None for the initial scan
  exclusive_start_key = None

  while True:
    # Perform scan operation with ExclusiveStartKey
    if exclusive_start_key is not None:
      response = table.scan(
          ExclusiveStartKey=exclusive_start_key
      )
    else:
      response = table.scan()

    items = response.get('Items', [])

    # Process the items in the current response
    for item in items:
      recipe_id = int(item['recipe_id'])
      if recipe_id in recipe_ids:
        # Process only the items with recipe_ids in the specified list
        if recipe_id not in recipes_by_ingredients:
          recipes_by_ingredients[recipe_id] = {'ingredient_ids': [], 'ingredient_instructions': []}
        recipes_by_ingredients[recipe_id]['ingredient_ids'] = [int(x) for x in item['ingredient_list'].split(' ')]
        recipes_by_ingredients[recipe_id]['ingredient_instructions'] = [instruction for instruction in item['ingredient_instructions'].split('---')]

    # If there is no LastEvaluatedKey, break out of the loop
    if 'LastEvaluatedKey' not in response:
      break

    # Set the ExclusiveStartKey for the next iteration
    exclusive_start_key = response['LastEvaluatedKey']

  return recipes_by_ingredients

def get_top_n_recipes(recipes_info, recipe_ingredient_ids, n):
  
  # Extract the ingredient IDs from recipes_info
  recipes_ingredient_lists = [recipes_info[recipe_id]['ingredient_ids'] for recipe_id in recipes_info]

  # Convert ingredient IDs to strings for TF-IDF vectorization
  recipes_ingredient_strings = [' '.join(map(str, ingredient_ids)) for ingredient_ids in recipes_ingredient_lists]

  # Create a TF-IDF vectorizer
  vectorizer = TfidfVectorizer()

  # Fit and transform the TF-IDF matrix
  tfidf_matrix = vectorizer.fit_transform(recipes_ingredient_strings)
  
  # Transform the input ingredient IDs
  input_ingredient_string = ' '.join(map(str, recipe_ingredient_ids))
  input_tfidf = vectorizer.transform([input_ingredient_string])

  # Compute cosine similarity
  similarity_scores = cosine_similarity(tfidf_matrix, input_tfidf)
  result_dict = {}
  recipe_ids = [recipe_id for recipe_id in recipes_info]
  for recipe_id, score in zip(recipe_ids, similarity_scores):
    result_dict[recipe_id] = score[0]
    
  # Sort recipes based on similarity scores
  sorted_dict_by_values = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))

  # return the top n mathced recipe ids
  return list(sorted_dict_by_values.keys())[:n]


def getRecipeNames(recipe_ids):
  """
  params: recipe_ids: a list of recipe ids
  return: a list of English names for each recipe
  """
  table = dynamodb.Table("recipe_details")
  recipes_by_name = {}

  last_evaluated_key = None

  while True:
    # Use Scan and filter by recipe_ids
    if last_evaluated_key:
      response = table.scan(
        FilterExpression=Attr('recipe_id').is_in(recipe_ids),
        ExclusiveStartKey=last_evaluated_key
      )
    else:
      response = table.scan(
        FilterExpression=Attr('recipe_id').is_in(recipe_ids)
      )

    for item in response['Items']:
      recipe_id = int(item['recipe_id'])
      recipes_by_name[recipe_id] = item['title'].title()

    last_evaluated_key = response.get('LastEvaluatedKey')

    if not last_evaluated_key:
      break  # No more pages to scan

  return recipes_by_name


def getRecRecipes(ingredients, n=5):
  st = time.time()
  ingredient_ids = getIngredientIds(ingredients)
  print('getIngredientIds runtime: ', time.time()-st)
  st = time.time()
  recipe_ids = getRecipeIdsUnion(ingredient_ids)
  print('getRecipeIdsUnion runtime: ', time.time()-st)
  st = time.time()
  recipes_info = getRecipeIngredients(recipe_ids)
  print('getRecipeIngredients runtime: ', time.time()-st)
  st = time.time()
  if (len(recipes_info) == 0):
    return {}
  top_n_recipe_ids = get_top_n_recipes(recipes_info, ingredient_ids, n)
  print('get_top_n_recipes runtime: ', time.time()-st)
  recipes_ids_with_ingredients = {}
  for recipe_id in top_n_recipe_ids:
    recipes_ids_with_ingredients[recipe_id] = recipes_info[recipe_id]['ingredient_instructions']
  st = time.time()
  top_n_recipe_names = getRecipeNames(top_n_recipe_ids)
  print('getRecipeNames runtime: ', time.time()-st)
  recipe_names_with_ingredients = {}
  for recipe_id in top_n_recipe_names:
    recipe_names_with_ingredients[top_n_recipe_names[recipe_id]] = recipes_ids_with_ingredients[recipe_id]
  return recipe_names_with_ingredients

def main():
  ingredient_names = ["tomato"]
  # ingredient_ids = getIngredientIds(ingredient_names)
  # print(ingredient_ids)
  # union = getRecipeIdsUnion(ingredient_ids)
  # print(union)
  # recipes_info = getRecipeIngredients(union)
  # print(recipes_info)
  # top_n_recipe_ids = get_top_n_recipes(recipes_info, ingredient_ids, 5)
  # print(top_n_recipe_ids)
  # print(getRecipeNames(top_n_recipe_ids))
  print(getRecRecipes(ingredient_names))

if __name__ == '__main__':
  main()