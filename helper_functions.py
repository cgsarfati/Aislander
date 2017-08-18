# Import model.py table definitions
from model import connect_to_db, db, User, Recipe, Ingredient, List, Cuisine
from model import Aisle, RecipeIngredient, ListIngredient, Bookmark, RecipeCuisine

# Library for easy API calls
import requests

# To Access OS environmental variables
import os

# use API key
headers = {"X-Mashape-Key": os.environ['RECIPE_CONSUMER_KEY'],
           "Accept": "application/json"}


def add_recipe(recipe_id):
    """ Adds recipe to Recipes table as well as appending its ingredients and
    cuisines to the Ingredients and Cuisines tables. """

    # Get info from API and store as json
    info_response = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/'
                                 + recipe_id + '/information', headers=headers)
    new_recipe_json = info_response.json()

    # Instantiate recipe object
    new_recipe = Recipe(recipe_id=recipe_id, recipe_name=new_recipe_json['title'],
                        img_url=new_recipe_json['image'],
                        instructions=new_recipe_json['instructions'])

    ########## ADD RECIPE TO DB ##########
    db.session.add(new_recipe)
    db.session.commit()

    # Isolate ing. key to be looped over
    ingredients_info = new_recipe_json['extendedIngredients']

    for ingredient_info in ingredients_info:

        # Isolate id from info pkg, then check if in DB
        ingredient_id = ingredient_info['id']
        current_ingredient = Ingredient.query.filter(Ingredient.ing_id == ingredient_id).first()

        # If ing not in DB, instantiate + check if ing's aisle in DB
        if not current_ingredient:

            # create ingredient object that may or may not have aisle id info
            new_ingredient = Ingredient(ing_id=ingredient_id,
                                        ing_name=ingredient_info['name'],
                                        aisle_id=None)

            # get ing info package, isolate its aisle. Check if in DB.
            aisle_name = ingredient_info['aisle']
            current_aisle = Aisle.query.filter(Aisle.aisle_name == aisle_name).first()

            # if aisle not in DB, instantiate, add to DB, then add to ing object
            if not current_aisle:
                new_aisle = Aisle(aisle_name=aisle_name)

                ########## ADD AISLE TO DB ##########
                db.session.add(new_aisle)
                db.session.commit()

                # Add aisle_id that was previously None during instantiation
                new_ingredient.aisle_id = new_aisle.aisle_id

            # Now, back at the ingredient loop, new_ing should have aisle_id
            ########## ADD INGREDIENT TO DB ##########
            db.session.add(new_ingredient)
            db.session.commit()

        # Instantiate for middle table and add to DB
        new_recipe_ingredient = RecipeIngredient(recipe_id=recipe_id,
                                                 ing_id=ingredient_id,
                                                 meas_unit=ingredient_info['unit'],
                                                 mass_qty=ingredient_info['amount'])

        ########## ADD RECIPE-INGREDIENT TO DB ##########
        db.session.add(new_recipe_ingredient)
        db.session.commit()

    # At this point, the recipe, ingredients, and aisle tables should be filled.
    # Now, it's time to fill the cuisine table. Similar appraoch to ingredients
    # since cuisines is a list in the json.

    # Isolate cuisine list
    cuisine_list = new_recipe_json['cuisines']



def add_bookmark():
    # new_rec.bookmark.users.append(current_user_obj)

    pass


def add_to_list():

    pass
