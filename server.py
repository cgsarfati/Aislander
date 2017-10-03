""" Grocery List App. """

# For using custom decorators
from functools import wraps

# Import web templating language
from jinja2 import StrictUndefined

# Password hashing library
from passlib.apps import custom_app_context as pwd_context

# Import Flask web framework
from flask import Flask, render_template, request, flash, redirect, session, g
from flask import url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# Import model.py table definitions
from model import connect_to_db, db, User, Recipe, Ingredient, List, Cuisine
from model import Aisle, RecipeIngredient, ListIngredient, Bookmark, RecipeCuisine

# Import helper functions that handles SQLAlchemy queries
import helper_functions

import api_calls

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# So that undefined variables in Jinja2 will strike an error vs. failing silently
app.jinja_env.undefined = StrictUndefined


#################### SETUP ####################

@app.before_request
def pre_process_all_requests():
    """Setup the request context. Current user info can now be
    accessed globally."""

    user_id = session.get('user_id')  # Get user id from session

    # Grab user's info from DB using the id. Save to g.current_user
    if user_id:
        g.current_user = User.query.get(user_id)
        g.logged_in = True
    else:
        g.logged_in = False
        g.current_user = None


# Custom decorator
def login_required(f):
    """ Redirects user to login page if trying to access a page that
    requires a logged in user."""

    # Use @login_required wrap under each app route for pages that
    # require a logged in user.
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            # Get url that corresponds back to the login form
            return redirect(url_for('display_homepage', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


#################### HOMEPAGE - LOGIN/REGISTRATION ####################

@app.route("/")
def display_homepage():
    """ Display homepage with login and registration form. """

    return render_template("homepage.html")


@app.route("/login", methods=['POST'])
def validate_login_info():
    """Form validation regarding log in form. Redirects user to dashboard page
    upon successful login."""

    # Get data back from login form
    username = request.form["username"]
    password = request.form["password"]

    # Hash pw
    hash = pwd_context.hash(password)
    verified = pwd_context.verify(password, hash)

    # Check if user in database
    existing_user = helper_functions.check_if_user_exists(username)

    # Form validation error messages
    if not existing_user:
        flash("{} does not exist!".format(username))
        return redirect("/")
    if existing_user.password != password:
        if not verified:
            flash("Incorrect password. Try again.")
            return redirect("/")

    # If successful, add user to session and redirect to dashboard.
    session["user_id"] = existing_user.user_id
    flash("{} has successfully logged in.".format(existing_user.username))
    return redirect("/dashboard")


@app.route("/logout")
def logout_user():
    """Log out user."""

    # Remove user from session when user clicks "logout" link
    del session["user_id"]
    flash("You have logged out.")
    return redirect("/")


@app.route("/register", methods=['POST'])
def process_registration_form():
    """Add user info to database. Upon successful registration, logs user in
    and redirects to dashboard page."""

    # Get form data back from registration form
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Check if username already taken
    username_exists = helper_functions.check_if_user_exists(username)

    if username_exists:
        flash("{} already taken. Try again!".format(username))
        return redirect("/")

    # Add user to DB & session
    new_user = helper_functions.add_user(username, email, password)
    flash("Thanks for registering {}!".format(username))
    session["user_id"] = new_user.user_id

    # Redirect to dashboard with newly logged-in user.
    return redirect("/dashboard")


#################### USER PROFILE ####################

@app.route("/my-profile")
@login_required
def display_profile():
    """Display user profile of username, email, and bookmarked recipes."""

    return render_template("user_profile.html",
                           username=g.current_user.username,
                           email=g.current_user.email,
                           bookmarked_recipes=g.current_user.recipes)


@app.route("/bookmark-carousel.json")
@login_required
def process_bookmark_images():
    """Get all bookmark images from DB."""

    # Extract list of recipes from DB
    bookmarked_recipes = g.current_user.recipes

    # Create dictionary of recipe image links
    bookmark_images = {'images': []}

    for recipe in bookmarked_recipes:
        bookmark_images['images'].append(recipe.img_url)

    print bookmark_images

    return jsonify(bookmark_images)


#################### DASHBOARD (RECIPE SEARCH/GROCERY LIST) ####################

@app.route("/dashboard")
@login_required
def display_searchbox_and_list():
    """Displays initial dashboard with following features: recipe search form,
    create new list form, and current grocery lists buttons."""

    # Extract dictionary that contains aisle information for all lists
    grocery_list_info = helper_functions.load_aisles(g.current_user.lists)

    return render_template("dashboard.html",
                           grocery_list_info=grocery_list_info)


@app.route("/new-list.json", methods=['POST'])
@login_required
def process_new_list():
    """Adds new grocery list to DB + displays in dashboard. If list already
    exists, returns error message. Else, returns list info to AJAX success
    function."""

    # Unpack info from ajax
    new_list_name = request.form["new_list_name"]

    # Check if list already exists for particular user. If not, add.
    list_exists = helper_functions.check_if_list_exists(g.current_user.user_id,
                                                        new_list_name)

    if not list_exists:
        new_list = helper_functions.add_new_list(g.current_user.user_id,
                                                 new_list_name)

        # Package up for new-list.js ajax success fn
        list_info = {'list_name': new_list.list_name,
                     'list_id': new_list.list_id}
        return jsonify(list_info)

    # Return message to new-list.js ajax success fn
    error_message = "That list already exists. Try again!"
    return error_message


@app.route("/search.json")
@login_required
def process_recipe_search():
    """Processes recipe search, using Spoonacular API to access data."""

    # Unpack info from ajax
    recipe_search = request.args.get("recipe_search")
    number_of_results = request.args.get("number_of_results")

    results_json = api_calls.recipe_search(recipe_search, number_of_results)

    # Combine 2 jsons together to be sent as one unified unit to ajax success fn
    for recipe in results_json['results']:
        recipe_id = str(recipe['id'])

        summary_response = api_calls.summary_info(recipe_id)

        # Store info returned as json and isolate its "summary" info
        summary_json = summary_response
        summary_text = summary_json['summary']

        # Append info to other json's recipes
        recipe['summary'] = summary_text

    # Return json to search-result.js ajax success function
    return jsonify(results_json)


@app.route("/bookmark.json", methods=["POST"])
@login_required
def process_recipe_bookmark_button():
    """Adds bookmark to DB, returning either a success or error message
    back to ajax success function."""

    # Unpack info from ajax
    recipe_id = request.form["recipe_id"]

    # Check if recipe in DB. If not, add new recipe to DB.
    current_recipe = helper_functions.check_if_recipe_exists(recipe_id)

    if not current_recipe:
        current_recipe = helper_functions.add_recipe(recipe_id)

    # Check if user already bookmarked recipe. If not, add to DB.
    bookmark_exists = (helper_functions
                       .check_if_bookmark_exists(current_recipe.recipe_id,
                                                 g.current_user.user_id))

    if not bookmark_exists:
        helper_functions.add_bookmark(g.current_user.user_id,
                                      current_recipe.recipe_id)
        # Return success message to bookmark-recipe.js ajax success fn
        success_message = "This recipe has been bookmarked!"
        return success_message

    # Return error message to bookmark-recipe.js ajax success fn
    error_message = "You've already bookmarked this recipe."
    return error_message


@app.route("/add-to-list.json", methods=["POST"])
@login_required
def process_add_to_list_button():
    """ Adds recipe ingredients to ListIngredient table. """

    # Unpack info from .js
    recipe_id = request.form['recipeId']
    list_id = request.form['listId']

    # Add recipe to DB if it does not already exist.
    current_recipe = helper_functions.check_if_recipe_exists(recipe_id)

    if not current_recipe:
        current_recipe = helper_functions.add_recipe(recipe_id)

    # Add ingredients to current list, returns list of ListIngredient objects
    list_ingredients = helper_functions.add_to_list(recipe_id, list_id)

    # Construct a dictionary that sends ingredient name, meas, and quant
    # back to ajax success fn
    ingredient_info = {"list_ingredients": [],
                       "new_ing_count": len(list_ingredients)}

    # FORMAT EXAMPLE:
    # per list item in dict above:
    #
    # new_ingredient = {
    #                   'mass_qty': mass_qty,
    #                   'meas_unit': meas_unit,
    #                   'ingredient': {
    #                     'name': name,
    #                     'aisle_name': aisle_name,
    #                     'aisle_id': aisle_id
    #                     }
    #                   }

    for ingredient in list_ingredients:
        new_ingredient = {}
        new_ingredient["mass_qty"] = ingredient.mass_qty  # integer
        new_ingredient["meas_unit"] = ingredient.meas_unit

        new_ingredient["ingredient"] = {}
        new_ingredient["ingredient"]["name"] = ingredient.ingredient.ing_name
        new_ingredient["ingredient"]["aisle_name"] = (ingredient
                                                      .ingredient
                                                      .aisle
                                                      .aisle_name
                                                      )
        new_ingredient["ingredient"]["aisle_id"] = str(ingredient
                                                       .ingredient
                                                       .aisle
                                                       .aisle_id
                                                       )

        ingredient_info["list_ingredients"].append(new_ingredient)

    return jsonify(ingredient_info)


#################### DETAILED RECIPE INFO ####################

@app.route("/recipe-info/<recipe_id>")
@login_required
def display_recipe_info(recipe_id):
    """ Display detailed recipe info upon clicking on link. """

    # Call recipe info API feature (no payload required)
    recipe_info_json = api_calls.recipe_info(recipe_id)

    # Unpack json
    title = recipe_info_json['title']
    img = recipe_info_json['image']
    ingredients = recipe_info_json['extendedIngredients']  # list
    cooking_instructions = recipe_info_json['instructions']

    return render_template("recipe_info.html", title=title,
                           img=img, ingredients=ingredients,
                           cooking_instructions=cooking_instructions)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
