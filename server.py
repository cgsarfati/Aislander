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

    return render_template("user_profile.html", username=user.username, email=user.email)


#################### DASHBOARD (RECIPE SEARCH/GROCERY LIST) ####################

@app.route("/dashboard")
@login_required
def display_searchbox_and_list():
    """ Displays dashboard with recipe search + empty grocery list. """

    return render_template("dashboard.html")


@app.route("/grocery-list.json")
@login_required
def process_new_list():
    """ Creates new grocery list that will be added to DB. Returns empty list. """

    # Unpack formInputs
    recipe_search = request.form["new_list_name"]

    # Add new empty list to DB

    # Return something
    return recipe_search


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

    # # Bookmark recipe
    # helper_functions.add_bookmark(g.current_user)

    # Return something back to ajax
    return recipe_id


# @app.route("/add_to_list.json", methods=["POST"])
# @login_required
# def process_add_to_list_button():
#     """ Adds recipe ingredients to list and stores it in DB,
#     returns updated list in browser. """

#     # Unpack info from .js

#     # API query the ingredients, extract needed info to be transferred to DB.

#     # Return data to display on list
#     pass


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
