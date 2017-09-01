""" SQL Alchemy queries used for Flask routes. """

# Import model.py table definitions
from model import connect_to_db, db, User, Recipe, Ingredient, List, Cuisine
from model import Aisle, RecipeIngredient, ListIngredient, Bookmark, RecipeCuisine

# Import file with all the Spoonacular API calls
import api_calls


def check_if_user_exists(username):
    """Checks if user exists in DB. If so, returns instantiated User
    object. Returns none if user not found."""

    return User.query.filter(User.username == username).first()


def check_if_list_exists(user_id, list_name):
    """Check if list exists in DB. If so, returns instantiated List
    object. Returns none if list not found."""

    return List.query.filter((List.list_name == list_name) &
                             (List.user_id == user_id)).first()


def check_if_recipe_exists(recipe_id):
    """Check if recipe exists in DB. If so, returns instantiated Recipe object.
    Returns none if recipe not found."""

    return Recipe.query.filter(Recipe.recipe_id == recipe_id).first()


def check_if_bookmark_exists(recipe_id, user_id):
    """Check if bookmark exists in DB. If so, returns instantiated Bookmark
    object. Returns none if bookmark not found."""

    return Bookmark.query.filter((Bookmark.recipe_id == recipe_id) &
                                 (Bookmark.user_id == user_id)).first()


def check_if_ingredient_exists(ingredient_id):
    """Check if ingredient exists in DB. If so, returns instantiated Ingredient
    object. Returns none if ingredient not found."""

    return Ingredient.query.filter(Ingredient.ing_id == ingredient_id).first()


def check_if_aisle_exists(aisle_name):
    """Check if aisle exists in DB. If so, returns instantiated Aisle
    object. Returns none if aisle not found."""

    return Aisle.query.filter(Aisle.aisle_name == aisle_name).first()


def check_if_cuisine_exists(cuisine_name):
    """Check if cuisine exists in DB. If so, returns instantiated Cuisine
    object. Returns none if cuisne not found."""

    return Cuisine.query.filter(Cuisine.cuisine_name == cuisine_name).first()


def add_aisle(aisle_name):
    """Adds recipe's ingredient's aisle to Aisle table in DB."""

    new_aisle = Aisle(aisle_name=aisle_name)
    db.session.add(new_aisle)
    print new_aisle.aisle_name, "added to Aisle table!"
    db.session.commit()

    return new_aisle


def add_recipe_ingredient(recipe_id, ing_id, meas_unit, mass_qty):
    """Adds recipe's ingredient to RecipeIngredient table in DB."""

    new_recipe_ingredient = RecipeIngredient(recipe_id=recipe_id,
                                             ing_id=ing_id,
                                             meas_unit=meas_unit,
                                             mass_qty=mass_qty)

    db.session.add(new_recipe_ingredient)
    db.session.commit()

    return new_recipe_ingredient


def add_ingredients(recipe_id, ingredients_info):
    """Adds recipe's ingredients to Ingredient table in DB. This in turn
    also requires adding ingredient's aisles to Aisle table and populating
    RecipeIngredient table."""

    # Loop through ing. list, adding new ingredients and aisles to DB if necessary
    for ingredient_info in ingredients_info:
        ingredient_id = str(ingredient_info['id'])
        ingredient_exists = check_if_ingredient_exists(ingredient_id)

        if not ingredient_exists:
            print "THIS INGREDIENT DOES NOT EXIST IN INGREDIENT TABLE:", ingredient_info['name'], " **********"
            # create Ingredient object that may or may not have aisle id info
            new_ingredient = Ingredient(ing_id=ingredient_id,
                                        ing_name=ingredient_info['name'])

            aisle_name = ingredient_info['aisle']
            print ingredient_info['name'], "'s aisle is", aisle_name
            aisle_exists = check_if_aisle_exists(aisle_name)

            if not aisle_exists:
                print aisle_name, " does not exist in DB."
                new_aisle = add_aisle(aisle_name)
                new_ingredient.aisle_id = new_aisle.aisle_id
            else:
                print aisle_name, " already exists in DB."
                new_ingredient.aisle_id = aisle_exists.aisle_id

            # At this point, new_ingredient should have an aisle_id
            # Add completed new_ingredient to DB
            db.session.add(new_ingredient)
            print new_ingredient.ing_name, "NOW ADDED TO INGREDIENTS TABLE! **********"
            db.session.commit()

            # Add new ing to RecipeIngredient table
            add_recipe_ingredient(recipe_id,
                                  ingredient_id,
                                  ingredient_info['unit'],
                                  ingredient_info['amount'])
            print new_ingredient.ing_name, "added to R-I table! (this is a new ing) ***********"
        else:
            # Add already-existing ing to RecipeIngredient table, since this is
            # always going to be a new recipe (indicated in server.py conditional).
            # This ing could already exist in DB due to past recipes using the
            # same ingredient.
            add_recipe_ingredient(recipe_id,
                                  ingredient_id,
                                  ingredient_info['unit'],
                                  ingredient_info['amount'])
            print ingredient_info['name'], "added to R-I table! (ing already existed) ************"


def add_recipe_cuisine(cuisine_id, recipe_id):
    """Populates RecipeCuisine association table in DB after adding
    Cuisine to DB."""

    new_recipe_cuisine = RecipeCuisine(cuisine_id=cuisine_id, recipe_id=recipe_id)
    db.session.add(new_recipe_cuisine)
    db.session.commit()


def add_cuisines(recipe_id, cuisines):
    """Adds cuisines to Cuisine table in DB."""

    for cuisine in cuisines:
        cuisine_exists = check_if_cuisine_exists(cuisine)

        if not cuisine_exists:
            new_cuisine = Cuisine(cuisine_name=cuisine)
            db.session.add(new_cuisine)
            db.session.commit()
            cuisine_id = new_cuisine.cuisine_id
        else:
            cuisine_id = cuisine_exists.cuisine_id
        add_recipe_cuisine(cuisine_id, recipe_id)


def add_recipe(recipe_id):
    """ Adds recipe to Recipes table, which also populates the following
    tables: Ingredient, Aisle, Cuisine, RecipeIngredient. Returns new Recipe
    object back to server."""

    # Get info from API and store as json
    info_response = api_calls.recipe_info(recipe_id)

    new_recipe_json = info_response.json()

    # Add new recipe to DB
    new_recipe = Recipe(recipe_id=recipe_id,
                        recipe_name=new_recipe_json['title'],
                        img_url=new_recipe_json['image'],
                        instructions=new_recipe_json['instructions'])

    db.session.add(new_recipe)
    print "recipe added to DB. new recipe object:", new_recipe
    db.session.commit()

    # Isolate ingredients and cuisine info from dict to be added to DB.
    ingredients_info = new_recipe_json['extendedIngredients']
    add_ingredients(recipe_id, ingredients_info)
    print "successfully added new ingredients to DB, and"

    cuisines = new_recipe_json['cuisines']
    add_cuisines(recipe_id, cuisines)

    return new_recipe


def add_user(username, email, password):
    """Adds user to Users table in DB. Returns instantiated user object."""

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def add_bookmark(user_id, recipe_id):
    """Adds recipe to Bookmarks table. Returns instantiated Bookmark object."""

    new_bookmark = Bookmark(user_id=user_id, recipe_id=recipe_id)

    db.session.add(new_bookmark)
    db.session.commit()

    return new_bookmark


def add_new_list(user_id, list_name):
    """Adds new list to List table."""

    new_list = List(user_id=user_id, list_name=list_name)

    db.session.add(new_list)
    db.session.commit()

    return new_list


def add_to_list(recipe_id, list_id):
    """ Add chosen recipe's ingredients to ListIngredient table in DB. Return
    a list of ListIngredient objects. """

    # Get list of recipe_ingredient objects that have ing_ids, meas, and units
    recipe_ingredients = (RecipeIngredient.query
                          .filter(RecipeIngredient.recipe_id == recipe_id)
                          .all()
                          )
    print "this is a list of R-I objects that need to be added to L-I table:", recipe_ingredients

    # Create empty list, which will be appended with new ListIngredient objects
    updated_list_ingredients = []

    for recipe_ingredient in recipe_ingredients:
        new_ListIngredient = ListIngredient(list_id=list_id,
                                            ing_id=recipe_ingredient.ing_id,
                                            meas_unit=recipe_ingredient.meas_unit,
                                            mass_qty=recipe_ingredient.mass_qty)
        db.session.add(new_ListIngredient)
        print "recipe-ingredient added to ListIngredient table!"
        db.session.commit()
        updated_list_ingredients.append(new_ListIngredient)

    # Return the list of ListIngredient objects
    print "At this point. List-Ingredient table should be fully populated with that recipe's ingredients."
    return updated_list_ingredients


def load_aisles(user_lists):
    """ Creates dictionary containing ingredient info for each aisle in each
    grocery list.

    Format:
    {
     (list_id, list_name): {
        (aisle_id, aisle_name): [
                                 {'ing_qty: qty,
                                  'ing_unit': unit,
                                  'ing_name': name},
                                 {'ing_qty: qty,
                                  'ing_unit': unit,
                                  'ing_name': name}
                                ]
        }
    }
    """

    # Create empty dictionary (will append all info at end)
    grocery_dictionary = {}

    # Loop through grocery lists
    for user_list in user_lists:
        aisles = {}
        list_key = (str(user_list.list_id), user_list.list_name)

        # Loop through each list's ingredients
        for list_ingredient in user_list.list_ingredients:
            aisle_key = (str(list_ingredient.ingredient.aisle.aisle_id),
                         list_ingredient.ingredient.aisle.aisle_name)

            # If aisle exists, add to list. If not, create a new aisle first.
            if aisle_key in aisles:
                print aisle_key[1], " already exists! just appending to already existing list"
                aisles[aisle_key].append({'ing_qty': list_ingredient.mass_qty,
                                          'ing_unit': list_ingredient.meas_unit,
                                          'ing_name': list_ingredient.ingredient.ing_name})
            else:
                print aisle_key[1], " is new! lets create a new list"
                aisles[aisle_key] = [{'ing_qty': list_ingredient.mass_qty,
                                      'ing_unit': list_ingredient.meas_unit,
                                      'ing_name': list_ingredient.ingredient.ing_name}]

        # Populate empty aisles dict with info created above, attaching aisles
        # dict as the value to the grocery dict's key
        grocery_dictionary[list_key] = aisles

        print grocery_dictionary

    return grocery_dictionary
