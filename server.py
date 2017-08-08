""" Grocery List App. """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Recipe, Ingredient
from model import List, CategoryRecipe, CategoryIngredient, RecipeIngredient
from model import ListIngredient, Bookmark, RecipeCategory

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# So that undefined variables in Jinja2 will strike an error vs. failing silently
app.jinja_env.undefined = StrictUndefined


@approute("/")
pass

#homepage


@app.route("/register")
pass

#GET - SHOW FORM
#POST - PROCESS FORM


@app.route("/login")
pass

#GET - SHOW FORM
#POST - CHECK LOGIN
# if ok, add user to session


@app.route("/logout")
pass

#GET
#redirect back to homepage
#delete user from session


@app.route("/user")
pass

#GET - SHOW PROFILE
# URL should be /users/<username>
# implied that /users should be a page in itself?


@app.route("/<username>/home")

#LOGGED IN userpage with grocery list / recipe search bar
#"Dashboard" of user
#Or should I not do this and render '/' instead?

pass

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
