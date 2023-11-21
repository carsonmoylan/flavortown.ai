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
  """
  params: recipe_ids: a list of recipe ids
  return: a dictionary with each recipe id as a key and the value is a the list of ingredient ids for that recipe
                  and a list of portions per ingredient
  """
  table = dynamodb.Table("recipes_by_ingredients")
  recipes_by_ingredients = {}
  for recipe_id in recipe_ids:
    response = table.query(
      KeyConditionExpression=Key('recipe_id').eq(recipe_id)
    )
    recipes_by_ingredients[recipe_id] = {'ingredient_ids': [], 'ingredient_instructions': []}
    ids = response['Items'][0]['ingredient_list'].split()
    recipes_by_ingredients[recipe_id]['ingredient_ids'] = [int(x) for x in ids]
    instructions = response['Items'][0]['ingredient_instructions'].split('---')
    recipes_by_ingredients[recipe_id]['ingredient_instructions'] = instructions
    
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

# change s.t. 
def getRecipeNames(recipe_ids):
  """
  params: recipe_ids: a list of recipe ids
  return: a list of english names for each recipe
  """
  table = dynamodb.Table("recipe_details")
  recipes_by_name = {}
  for recipe_id in recipe_ids:
    response = table.query(
      KeyConditionExpression=Key('recipe_id').eq(recipe_id)
    )
    recipes_by_name[recipe_id] = (response['Items'][0]['title'].title())
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
  return list(recipe_names_with_ingredients.keys())

def main():
  ingredient_names = ["banana", "liquid smoke", "pork"]
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