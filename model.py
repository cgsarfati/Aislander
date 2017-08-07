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

    recipe_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    recipe_name = db.Column(db.String(64), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories-rec.cat_r_id'))
    instructions = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Recipe recipe_id={} recipe_name={} img_url={}
                          cat_id={} instructions={}>""".format(
            self.recipe_id, self.recipe_name, self.img_url, self.cat_id,
            self.instructions)

    # Define relationship to category recipe
    category_recipe = db.relationship("CategoryRecipe", backref=db.backref("recipes"))


class Ingredient(db.Model):
    """ Ingredient of recipes in website. """

    __tablename__ = 'ingredients'

    ing_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    ing_name = db.Column(db.String(64), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories-ing.cat_i_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Ingredient ing_id={} ing_name={} cat_id={}>".format(
            self.ing_id, self.ing_name, self.cat_id)

    # Define relationship to category ingredient
    category_ingredient = db.relationship("CategoryIngredient",
                                          backref=db.backref("ingredients"))


class List(db.Model):
    """ Grocery list of user. """

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<List list_id={} user_id={} list_name={}>".format(
            self.list_id, self.user_id, self.list_name)

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("lists"))

##### ONE-TO-MANY TABLES #####


class CategoryRecipe(db.Model):
    """ Category of recipes. """

    __tablename__ = 'categories-rec'

    cat_r_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    cat_r_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CategoryRecipe cat_r_id={} cat_r_name={}>".format(
            self.cat_r_id, self.cat_r_name)


class CategoryIngredient(db.Model):
    """ Category of ingredients. """

    __tablename__ = 'categories-ing'

    cat_i_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    cat_i_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<CategoryIngredient cat_i_id={} cat_i_name={}>".format(
            self.cat_i_id, self.cat_i_name)

##### MIDDLE TABLES #####


class RecipeIngredient(db.Model):
    """ Ingredients of particular recipe / Recipes of particular ingredient. """

    __tablename__ = "recipe-ingredients"

    r_i_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    ing_id = db.Column(db.Integer, db.ForeignKey('ingredients.ing_id'))
    meas_unit = db.Column(db.String(30), nullable=True)
    mass_qty = db.Column(db.Integer, nullable=True)  # NOT to be incremented

    # Define relationship to recipe
    recipe = db.relationship("Recipe", backref=db.backref("recipe-ingredients"))

    # Define relationship to ingredient
    ingredient = db.relationship("Ingredient",
                                 backref=db.backref("recipe-ingredients"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<RecipeIngredient r_i_id={} recipe_id={} ing_id={}
                  meas_unit={} mass_qty={}>""".format(self.r_i_id, self.recipe_id,
                                                      self.ing_id, self.meas_unit,
                                                      self.mass.qty)


class ListIngredient(db.Model):
    """ Ingredients of particular list / Lists of particular ingredient. """

    __tablename__ = "list-ingredients"

    l_i_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    list_id = db.Column(db.Integer,
                        db.ForeignKey('lists.list_id'))
    ing_id = db.Column(db.Integer, db.ForeignKey('ingredients.ing_id'))
    meas_unit = db.Column(db.String(30), nullable=True)
    mass_qty = db.Column(db.Integer, nullable=True)  # incrementable

    # Define relationship to list
    # List is keyword so used lst instead; REMEMBER THIS
    lst = db.relationship("List", backref=db.backref("list-ingredients"))

    # Define relationship to ingredient
    ingredient = db.relationship("Ingredient",
                                 backref=db.backref("list-ingredients"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<ListIngredient l_i_id={} list_id={} ing_id={}
                  meas_unit={} mass_qty={}>""".format(self.l_i_id, self.list_id,
                                                      self.ing_id, self.meas_unit,
                                                      self.mass.qty)

##### ASSOCATION TABLES #####


class Bookmark(db.Model):
    """ Ingredients of particular recipe / Recipes of particular ingredient. """

    __tablename__ = "bookmarks"

    bookmark_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("bookmarks"))

    # Define relationship to recipe
    recipe = db.relationship("Recipe", backref=db.backref("bookmarks"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Bookmark bookmark_id={} user_id={} recipe_id={}>""".format(
            self.bookmark_id, self.user_id, self.recipe_id)


# RESEARCH API TO SEE IF THIS TABLE DEFINITION IS NEEDED

class RecipeCategory(db.Model):
    """ Recipe of particulary category / Category of particular recipe. """

    __tablename__ = "recipe-categories"

    rec_c_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    cat_r_id = db.Column(db.Integer, db.ForeignKey('categories-rec.cat_r_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))

    # Define relationship to category recipe
    # REMEMBER table name categories-rec not category_rec
    category_rec = db.relationship("CategoryRecipe", backref=db.backref("recipe-categories"))

    # Define relationship to recipe
    recipe = db.relationship("Recipe", backref=db.backref("recipe-categories"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<RecipeCategory rec_c_id={} cat_r_id={} recipe_id={}>".format(
            self.rec_c_id, self.cat_r_id, self.recipe_id)


#####################################################################
# Helper functions
