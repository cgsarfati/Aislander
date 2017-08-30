""" SQL Alchemy queries used for Flask routes. """

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


def check_if_user_exists(username):
    """Checks if user exists in DB. If user exists, returns instantiated user
    object. Returns none if user not found. """

    return User.query.filter(User.username == username).first()


def add_user_to_db(username, email, password):
    """Adds user to Users table in DB. Returns instantiated user object."""

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def add_recipe(recipe_id):
    """ Adds recipe to Recipes table as well as appending its ingredients and
    cuisines to the Ingredient, Cuisine, and RecipeIngredient tables. """

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

    # Loop through ing. list
    for ingredient_info in ingredients_info:

        # Isolate id from info pkg, then check if in DB
        ingredient_id = str(ingredient_info['id'])
        current_ingredient = Ingredient.query.filter(Ingredient.ing_id == ingredient_id).first()

        # If ing not in DB, instantiate + check if ing's aisle in DB
        if not current_ingredient:

            # create ingredient object that may or may not have aisle id info
            new_ingredient = Ingredient(ing_id=ingredient_id,
                                        ing_name=ingredient_info['name'])

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

            else:
                new_ingredient.aisle_id = current_aisle.aisle_id

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
    cuisines = new_recipe_json['cuisines']

    for cuisine in cuisines:

        # Check if cuisine in DB
        current_cuisine = Cuisine.query.filter(Cuisine.cuisine_name == cuisine).first()

        # If not, instantiate + add to DB
        if not current_cuisine:
            new_cuisine = Cuisine(cuisine_name=cuisine)

            ########## ADD CUISINE TO DB ##########
            db.session.add(new_cuisine)
            db.session.commit()

            cuisine_id = new_cuisine.cuisine_id

        else:
            cuisine_id = current_cuisine.cuisine_id

        new_recipe_cuisine = RecipeCuisine(cuisine_id=cuisine_id, recipe_id=recipe_id)
        db.session.add(new_recipe_cuisine)
        db.session.commit()

    return new_recipe


def add_bookmark(bookmark_info):
    """ Adds recipe to Bookmarks table. """

    # bookmark_info is a list --> [current_user_id, current_recipe_id]
    new_bookmark = Bookmark(user_id=bookmark_info[0], recipe_id=bookmark_info[1])

    db.session.add(new_bookmark)
    db.session.commit()

    return new_bookmark


def add_new_list(list_info):
    """ Adds new list to List table. """

    # list_info is a list --> [current_user_id, new_list_name]
    new_list = List(user_id=list_info[0], list_name=list_info[1])

    db.session.add(new_list)
    db.session.commit()

    return new_list


def add_to_list(recipe_id, list_id):
    """ Adds recipe ingredients to ListIngredient table. """

    # Get list of recipe_ingredient objects that have ing_ids, meas, and units
    recipe_ingredients = RecipeIngredient.query.filter(RecipeIngredient.recipe_id == recipe_id).all()

    # This will be appended with new ListIngredient objects
    updated_list_ingredients = []

    for recipe_ingredient in recipe_ingredients:
        new_ListIngredient = ListIngredient(list_id=list_id,
                                            ing_id=recipe_ingredient.ing_id,
                                            meas_unit=recipe_ingredient.meas_unit,
                                            mass_qty=recipe_ingredient.mass_qty)
        db.session.add(new_ListIngredient)
        db.session.commit()
        updated_list_ingredients.append(new_ListIngredient)

    # Return the list of ListIngredient objects
    return updated_list_ingredients


def load_user_lists(current_user):
    """ Initially loads current user's lists onto dashboard page. """

    return current_user.lists


def load_aisles(user_lists):
    """ Creates dictionary containing ingredient info for each aisle in each
    grocery list. """

    # Create empty dictionary (will store all info at end)
    grocery_dictionary = {}

    # Loop through each grocery list
    for user_list in user_lists:
        aisles = {}  # Will be populated with aisles and ingredients later
        list_key = (str(user_list.list_id), user_list.list_name)  # Will add to dict at end once aisles dict fills up

        for list_ingredient in user_list.list_ingredients:
            aisle_key = (str(list_ingredient.ingredient.aisle.aisle_id), list_ingredient.ingredient.aisle.aisle_name)
            # If aisle exists, add to list. if not, create new aisle with new list
            if aisle_key[1] in aisles:
                aisles[aisle_key].append({'ing_qty': list_ingredient.mass_qty,
                                          'ing_unit': list_ingredient.meas_unit,
                                          'ing_name': list_ingredient.ingredient.ing_name})
            else:
                aisles[aisle_key] = [{'ing_qty': list_ingredient.mass_qty,
                                      'ing_unit': list_ingredient.meas_unit,
                                      'ing_name': list_ingredient.ingredient.ing_name}]

        # Add list_key as key to grocery dict with aisles dict
        grocery_dictionary[list_key] = aisles

    return grocery_dictionary
