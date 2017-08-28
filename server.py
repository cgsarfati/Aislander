""" Grocery List App. """

# For using custom decorators
from functools import wraps

# Library for easy API calls
import requests

# To Access OS environmental variables
import os

# Import web templating language
from jinja2 import StrictUndefined

# Import Flask web framework
from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension

# Import model.py table definitions
from model import connect_to_db, db, User, Recipe, Ingredient, List, Cuisine
from model import Aisle, RecipeIngredient, ListIngredient, Bookmark, RecipeCuisine

# Import helper functions (query/add/delete from DB)
import helper_functions

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# So that undefined variables in Jinja2 will strike an error vs. failing silently
app.jinja_env.undefined = StrictUndefined


#################### GLOBAL FUNCTIONS ####################

@app.before_request
def pre_process_all_requests():
    """ Setup the request context. Current user info can now be accessed globally. """

    # Get user info from session
    user_id = session.get('user_id')

    # If exists, use it to grab user's info from DB. Save to g.current_user
    if user_id:
        g.current_user = User.query.get(user_id)
        # Use g.logged_in status for future conditionals in app routes
        g.logged_in = True
    else:
        g.logged_in = False
        g.current_user = None


# custom decorator
def login_required(f):
    """ Redirects user to login page if trying to access a page that
    requires a logged in user."""

    # Wraps gives ability to use @login_required under each app route
    # that needs a logged in user
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.current_user is None:
            # Get url that corresponds to login_form html
            return redirect(url_for('login_form', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# use API key
headers = {"X-Mashape-Key": os.environ['RECIPE_CONSUMER_KEY'],
           "Accept": "application/json"}


#################### HOMEPAGE ####################

@app.route("/")
def index():
    """ Display homepage. """

    return render_template("homepage.html")


#################### REGISTRATION ####################

@app.route("/register")
def display_registration_form():
    """ Display registration form. """

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def process_registration_form():
    """ Add user info to database. Redirects back to homepage. """

    # Get form data back from register_form.html
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Instantiate user
    # Refer to model.py for User table parameters
    # User_id will is autoincrementing, no need to specify it
    new_user = User(username=username, email=email, password=password)

    # Add user to database
    db.session.add(new_user)
    db.session.commit()

    flash("Thanks for registering {}!".format(username))  # same as new_user.username

    # Return to homepage. User now registered and can log in.
    return redirect("/")


#################### LOGIN/LOGOUT ####################

@app.route("/login")
def display_login_form():
    """ Display login form. """

    return render_template("login_form.html")


@app.route("/login", methods=['POST'])
def validate_login_info():
    """ Attempt to log the user in by crossmatching with database. """

    # Get form data back from login_form.html
    username = request.form["username"]
    password = request.form["password"]

    # Check if user in database
    # Use .first() --> gives back user object if exists. Nonetype if not.
    user = User.query.filter(User.username == username).first()

    # Error messages
    if not user:
        flash("{} does not exist!".format(username))
        return redirect("/login")
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # If successful, add user to session and go back to homepage.
    session["user_id"] = user.user_id
    flash("{} has successfully logged in.".format(user.username))
    return redirect("/dashboard")


@app.route("/logout")
def logout_user():
    """ Log out user. """

    # Remove user from session (remember session info is user's PK not username!)
    del session["user_id"]
    flash("You have logged out.")
    return redirect("/")


#################### USER PROFILE ####################

@app.route("/users/<username>")
def display_profile(username):
    """ Show user profile."""

    # Input of <username> is now the parameter for this function.
    # Crossmatch with DB to find that particular user's info. Returns object.
    user = User.query.filter(User.username == username).first()

    # Load bookmarks
    bookmarked_recipes = user.recipes  # a list of recipe objects

    # Load grocery lists
    user_lists = helper_functions.load_user_lists(g.current_user)

    return render_template("user_profile.html", username=user.username,
                           email=user.email, bookmarked_recipes=bookmarked_recipes,
                           user_lists=user_lists)


#################### DASHBOARD (RECIPE SEARCH/GROCERY LIST) ####################

@app.route("/dashboard")
@login_required
def display_searchbox_and_list():
    """ Displays dashboard with recipe search + display list feature. """

    # Access all of current user's list names, returns a list of List objects
    user_lists = helper_functions.load_user_lists(g.current_user)

    # Extract dictionary that contains all aisle info for all lists
    grocery_list_info = helper_functions.load_aisles(user_lists)

    return render_template("dashboard.html", grocery_list_info=grocery_list_info)


@app.route("/new-list.json", methods=['POST'])
@login_required
def process_new_list():
    """ Creates new grocery list that will be added to DB + displays in current
    page without having to refresh. """

    # Unpack formInputs
    new_list_name = request.form["new_list_name"]

    # Pack up list info
    list_info = [g.current_user.user_id, new_list_name]

    # Check if list already exists for particular user. If not, add.
    current_list = List.query.filter((List.list_name == new_list_name) & (List.user_id == g.current_user.user_id)).first()

    if not current_list:
        new_list = helper_functions.add_new_list(list_info)

        # Package up to have list id (for hidden data) + list name
        # Need to be sent back to success function as dictionary
        list_info = {'list_name': new_list.list_name, 'list_id': new_list.list_id}
        return jsonify(list_info)
    else:
        # Throw error message if list already exists
        error_message = "That list already exists. Try again!"
        return error_message


@app.route("/search.json")
@login_required
def process_recipe_search():
    """ Processes recipe search with Spoonacular API. """

    # Unpack formInputs
    recipe_search = request.args["recipe_search"]

    # Set up parameters for API call, then call API
    payload = {'query': recipe_search, 'number': 5}
    response = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search',
                            params=payload, headers=headers)

    # Store recipe info as json
    results_json = response.json()

    # Append "summary" key from another json to results_json
    for recipe in results_json['results']:
        recipe_id = str(recipe['id'])
        summary_response = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/' + recipe_id + '/summary',
                                        headers=headers)

        # Store as json and get summary key
        summary_json = summary_response.json()
        summary_text = summary_json['summary']

        # Create new summary key to original json
        recipe['summary'] = summary_text

    # Send json to search-result.js AJAX success function
    return jsonify(results_json)


@app.route("/bookmark.json", methods=["POST"])
@login_required
def process_recipe_bookmark_button():
    """ Adds recipe to DB, returns success message. """

    # Unpack info from .js
    recipe_id = request.form["recipe_id"]

    # See if recipe in DB. If not, add new recipe to DB.
    current_recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).first()

    if not current_recipe:
        current_recipe = helper_functions.add_recipe(recipe_id)

    # Extract recipe_id and user_id to put into Bookmarks table in DB
    bookmark_info = [g.current_user.user_id, current_recipe.recipe_id]

    # Check if user already bookmarked recipe. If not, add to DB.
    current_bookmark = Bookmark.query.filter((Bookmark.recipe_id == current_recipe.recipe_id) & (Bookmark.user_id == g.current_user.user_id)).first()

    if not current_bookmark:
        helper_functions.add_bookmark(bookmark_info)
        success_message = "This recipe has been bookmarked!"
        return success_message
    else:
        # Throw error message if bookmark already exists
        error_message = "You've already bookmarked this recipe."
        return error_message


@app.route("/add-to-list.json", methods=["POST"])
@login_required
def process_add_to_list_button():
    """ Adds recipe ingredients to ListIngredient table. """

    # Unpack info from .js
    recipe_id = request.form['recipeId']
    list_id = request.form['listId']

    # Check if recipe in DB. if not, add. In this process, the RecipeIngredient
    # table will be populated, allowing you to get relevant info.
    current_recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).first()

    if not current_recipe:
        current_recipe = helper_functions.add_recipe(recipe_id)

    # Add ingredients to current list, returns list of ListIngredient objects
    list_ingredients = helper_functions.add_to_list(recipe_id, list_id)

    # Create a dictionary that sends ingredient name, meas, and quant
    # back to ajax success function
    ingredient_info = {"list_ingredients": []}

    # FORMAT EXAMPLE:
    # per list item in ingredient_info above:
    #
    # new_ingredient = {'mass_qty': mass_qty,
    #                   'meas_unit': meas_unit,
    #                   'ingredient': {
    #                     'name': name,
    #                     'aisle_name': aisle_name
    #                     }
    #                   }

    for ingredient in list_ingredients:
        new_ingredient = {}
        new_ingredient["mass_qty"] = ingredient.mass_qty
        new_ingredient["meas_unit"] = ingredient.meas_unit

        new_ingredient["ingredient"] = {}
        new_ingredient["ingredient"]["name"] = ingredient.ingredient.ing_name
        new_ingredient["ingredient"]["aisle_name"] = ingredient.ingredient.aisle.aisle_name

        ingredient_info["list_ingredients"].append(new_ingredient)

    return jsonify(ingredient_info)


#################### DETAILED RECIPE INFO ####################

@app.route("/recipe-info/<recipe_id>")
@login_required
def display_recipe_info(recipe_id):
    """ Display detailed recipe info upon clicking on link. """

    # Call recipe info API feature (no payload required)
    info_response = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/' + recipe_id + '/information',
                                 headers=headers)

    # Store into json format
    recipe_info_json = info_response.json()

    # Unpack json
    title = recipe_info_json['title']
    cuisines = recipe_info_json['cuisines']  # list
    img = recipe_info_json['image']
    ingredients = recipe_info_json['extendedIngredients']  # list
    cooking_instructions = recipe_info_json['instructions']

    return render_template("recipe_info.html", title=title, cuisines=cuisines,
                           img=img, ingredients=ingredients,
                           cooking_instructions=cooking_instructions)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
