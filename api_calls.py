# To Access OS environmental variables
import os

# Library for API calls
import requests

headers = {"X-Mashape-Key": os.environ['RECIPE_CONSUMER_KEY'],
           "Accept": "application/json"}


def recipe_search(recipe_search, number_of_results):
    """Extracts recipe search results from Spoonacular API."""

    # Set up parameters for API call, then call Spoonacular API
    payload = {'query': recipe_search, 'number': number_of_results}
    spoonacular_endpoint = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
    response = requests.get(spoonacular_endpoint,
                            params=payload,
                            headers=headers)

    return response.json()


def summary_info(recipe_id):
    """Extracts recipe summary from Spoonacular API."""

    # call Spoonacular API, inserting recipe_id into endpoint
    summary_response = (requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/'
                                     + recipe_id + '/summary',
                                     headers=headers))

    return summary_response.json()


def recipe_info(recipe_id):
    """Extracts detailed recipe info from Spoonacular API."""

    # Get info from API, inserting recipe_id into endpoint
    info_response = requests.get(
        'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/'
        + recipe_id + '/information', headers=headers)

    return info_response.json()
