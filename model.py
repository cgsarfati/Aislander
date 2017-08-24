"""Models and database functions for Grocery App project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################MODEL DEFINITIONS##############################

##### MAIN TABLES #####


class User(db.Model):
    """ User of grocery website. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} username={} email={} password={}>".format(
            self.user_id, self.username, self.email, self.password)


class Recipe(db.Model):
    """ Recipe in grocery website. """

    __tablename__ = 'recipes'

    # Recipe_id the actual Spoonacular recipe_id; not auto-incrementing
    recipe_id = db.Column(db.String(64), nullable=False, primary_key=True)
    recipe_name = db.Column(db.String(64), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)
    instructions = db.Column(db.String(10000), nullable=True)

    # Define relationships to cuisines (ASSOCIATION)
    cuisines = db.relationship("Cuisine",
                               secondary="recipe_cuisines",
                               backref=db.backref("recipes"))

    # Define relationship to users (ASSOCIATION)
    users = db.relationship("User",
                            secondary="bookmarks",
                            backref=db.backref("recipes"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Recipe recipe_id={} recipe_name={} img_url={}
                  instructions={}>""".format(self.recipe_id, self.recipe_name,
                                             self.img_url, self.instructions)


class Ingredient(db.Model):
    """ Ingredient of recipes in website. """

    __tablename__ = 'ingredients'

    # ing_id actual Spoonacular id, not auto-incrementing
    ing_id = db.Column(db.String(64), nullable=False, primary_key=True)
    ing_name = db.Column(db.String(64), nullable=False)
    aisle_id = db.Column(db.Integer, db.ForeignKey('aisles.aisle_id'))

    # Define relationship to aisle (1-TO-MANY)
    aisle = db.relationship("Aisle", backref=db.backref("ingredients"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ing_id={} ing_name={} aisle_id={}>".format(
            self.ing_id, self.ing_name, self.aisle_id)


class List(db.Model):
    """ Grocery list of user. """

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String(60), nullable=True)

    # Define relationship to user (1-TO-MANY)
    user = db.relationship("User", backref=db.backref("lists"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<List list_id={} user_id={} list_name={}>".format(
            self.list_id, self.user_id, self.list_name)


class Cuisine(db.Model):
    """ Category of recipes. """

    __tablename__ = 'cuisines'

    cuisine_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    cuisine_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Cuisine cuisine_id={} cuisine_name={}>".format(
            self.cuisine_id, self.cuisine_name)


class Aisle(db.Model):
    """ Category of ingredients. """

    __tablename__ = 'aisles'

    aisle_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    aisle_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Aisle aisle_id={} aisle_name={}>".format(
            self.aisle_id, self.aisle_name)

##### MIDDLE TABLES #####


class RecipeIngredient(db.Model):
    """ Ingredients of particular recipe / Recipes of particular ingredient. """

    __tablename__ = "recipe_ingredients"

    r_i_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))
    ing_id = db.Column(db.String(64), db.ForeignKey('ingredients.ing_id'))
    meas_unit = db.Column(db.String(30), nullable=True)
    mass_qty = db.Column(db.Integer, nullable=True)  # NOT to be incremented

    # Define relationship to recipe and ingredient
    recipe = db.relationship("Recipe", backref="recipe_ingredients")
    ingredient = db.relationship("Ingredient", backref="recipe_ingredients")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<RecipeIngredient r_i_id={} recipe_id={} ing_id={}
                  meas_unit={} mass_qty={}>""".format(self.r_i_id, self.recipe_id,
                                                      self.ing_id, self.meas_unit,
                                                      self.mass_qty)


class ListIngredient(db.Model):
    """ Ingredients of particular list / Lists of particular ingredient. """

    __tablename__ = "list_ingredients"

    l_i_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    list_id = db.Column(db.Integer,
                        db.ForeignKey('lists.list_id'))
    ing_id = db.Column(db.String(64), db.ForeignKey('ingredients.ing_id'))
    meas_unit = db.Column(db.String(30), nullable=True)
    mass_qty = db.Column(db.Integer, nullable=True)  # incrementable

    # Define relationship to list and ingredient
    lst = db.relationship("List", backref="list_ingredients")
    ingredient = db.relationship("Ingredient", backref='list_ingredients')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<ListIngredient l_i_id={} list_id={} ing_id={}
                  meas_unit={} mass_qty={}>""".format(self.l_i_id, self.list_id,
                                                      self.ing_id, self.meas_unit,
                                                      self.mass_qty)

##### ASSOCATION TABLES #####


class Bookmark(db.Model):
    """ Ingredients of particular recipe / Recipes of particular ingredient. """

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Bookmark bookmark_id={} user_id={} recipe_id={}>""".format(
            self.bookmark_id, self.user_id, self.recipe_id)


class RecipeCuisine(db.Model):
    """ Recipe of particulary category / Category of particular recipe. """

    __tablename__ = "recipe_cuisines"

    recipe_cuisine_id = db.Column(db.Integer,
                                  autoincrement=True,
                                  primary_key=True)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.cuisine_id'))
    recipe_id = db.Column(db.String(64), db.ForeignKey('recipes.recipe_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeCuisine recipe_cuisine_id={} cuisine_id={} recipe_id={}>".format(
            self.recipe_cuisine_id, self.cuisine_id, self.recipe_id)


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///groceries'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Ability to play with table definitions in interactive mode

    from server import app
    connect_to_db(app)
    print "Connected to DB."
