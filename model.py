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
    password = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id={} username={} email={} password={}>".format(
            self.user_id, self.username, self.email, self.password)


class Recipe(db.Model):
    """ Recipe in grocery website. """

    __tablename__ = 'recipes'

    # Recipe_id the actual Spoonacular recipe_id; not auto-incrementing
    recipe_id = db.Column(db.String(64), nullable=False, primary_key=True)
    recipe_name = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(1000), nullable=True)
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

##########################TESTING DATA###############################


def example_data():
    """ Create some sample data to test in tests.py file. Manually created
        primary keys for auto-incrementing ones to ensure accuracy. """

    # Add sample users
    user1 = User(username='Bob', email='bob@gmail.com', password='Bobpw')
    user2 = User(username='Jane', email='jane@gmail.com', password='Janepw')
    user3 = User(username='Meg', email='meg@gmail.com', password='Megpw')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Add sample recipes
    recipe1 = Recipe(recipe_id='262682',
                     recipe_name="Thai Sweet Potato Veggie Burgers with Spicy Peanut Sauce",
                     img_url="https://spoonacular.com/recipeImages/262682-556x370.jpg",
                     instructions="Preheat the oven to 350F")
    recipe2 = Recipe(recipe_id='227961',
                     recipe_name="Cajun Spiced Black Bean and Sweet Potato Burgers",
                     img_url="Cajun-Spiced-Blao-Burgers-227961.jpg",
                     instructions='bake it')
    recipe3 = Recipe(recipe_id='602708',
                     recipe_name="Meatless Burgers with Romesco and Arugula",
                     img_url="Meatls-with-Romesco-and-Arugula-602708.jpg",
                     instructions='mix it')

    db.session.add_all([recipe1, recipe2, recipe3])
    db.session.commit()

    # Add sample aisles from ingredients
    aisle1 = Aisle(aisle_name="Canned and Jarred")
    aisle2 = Aisle(aisle_name="Ethnic Foods;Spices and Seasonings")
    aisle3 = Aisle(aisle_name="Produce")

    db.session.add_all([aisle1, aisle2, aisle3])
    db.session.commit()

    # Add sample ingredients
    ingredient1 = Ingredient(ing_id='16058', ing_name="canned chickpeas", aisle_id=1)
    ingredient2 = Ingredient(ing_id='1032028', ing_name="cajun spice", aisle_id=2)
    ingredient3 = Ingredient(ing_id='11959', ing_name="baby arugula", aisle_id=3)

    db.session.add_all([ingredient1, ingredient2, ingredient3])
    db.session.commit()

    # Add sample grocery lists
    list1 = List(user_id=1, list_name='Breakfast')
    list2 = List(user_id=2, list_name='Lunch')
    list3 = List(user_id=3, list_name='Dinner')

    db.session.add_all([list1, list2, list3])
    db.session.commit()

    # Add sample cuisines from recipes
    cuisine1 = Cuisine(cuisine_name='chinese')
    cuisine2 = Cuisine(cuisine_name='american')

    db.session.add_all([cuisine1, cuisine2])
    db.session.commit()

    # Add sample ingredients of existing recipe
    recipe_ingredient1 = RecipeIngredient(recipe_id='262682', ing_id='16058',
                                          meas_unit="ounce", mass_qty=15)
    recipe_ingredient2 = RecipeIngredient(recipe_id='227961', ing_id='1032028',
                                          meas_unit="tsp", mass_qty=2)
    recipe_ingredient3 = RecipeIngredient(recipe_id='602708', ing_id='11959',
                                          meas_unit="handful", mass_qty=1)

    db.session.add_all([recipe_ingredient1, recipe_ingredient2, recipe_ingredient3])
    db.session.commit()

    # Add sample ingredients of existing list
    list_ingredient1 = ListIngredient(list_id=1, ing_id='16058',
                                      meas_unit="ounce", mass_qty=15)
    list_ingredient2 = ListIngredient(list_id=2, ing_id='1032028',
                                      meas_unit="tsp", mass_qty=2)
    list_ingredient3 = ListIngredient(list_id=3, ing_id='11959',
                                      meas_unit="handful", mass_qty=1)

    db.session.add_all([list_ingredient1, list_ingredient2, list_ingredient3])
    db.session.commit()

    # Add sample bookmarks
    bookmark1 = Bookmark(user_id=1, recipe_id='262682')
    bookmark2 = Bookmark(user_id=2, recipe_id='227961')
    bookmark3 = Bookmark(user_id=3, recipe_id='602708')

    db.session.add_all([bookmark1, bookmark2, bookmark3])
    db.session.commit()

    # Add sample cuisines of recipes
    recipe_cuisine1 = RecipeCuisine(cuisine_id=1,
                                    recipe_id='262682')
    recipe_cuisine2 = RecipeCuisine(cuisine_id=2,
                                    recipe_id='227961')
    recipe_cuisine3 = RecipeCuisine(cuisine_id=2,
                                    recipe_id='602708')

    db.session.add_all([recipe_cuisine1, recipe_cuisine2, recipe_cuisine3])
    db.session.commit()


#####################################################################


def connect_to_db(app, db_uri='postgresql:///groceries'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Ability to play with table definitions in interactive mode

    from server import app
    connect_to_db(app)
    print "Connected to DB."
