"""Models and database functions for Grocery App project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################MODEL DEFINITIONS##############################

# MAIN TABLES


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


class Ingredients(db.Model):
    """ Ingredients of recipes in website. """

    __tablename__ = 'ingredients'

    ing_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    ing_name = db.Column(db.String(64), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories-ing.cat_i_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "Ingredient ing_id={} ing_name={} cat_id={}".format(
            self.ing_id, self.ing_name, self.cat_id)


class Lists(db.Model):
    """ Grocery lists of user. """

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    list_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "List list_id={} user_id={} list_name={}".format(
            self.list_id, self.user_id, self.list_name)


# ONE-TO-MANY TABLES

class CategoryRecipe(db.Model):
    """ Categories of recipes. """

    __tablename__ = 'categories-rec'

    cat_r_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    cat_r_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "CategoryRecipe cat_r_id={} cat_r_name={}".format(
            self.cat_r_id, self.cat_r_name)


class CategoryIngredient(db.Model):
    """ Categories of ingredients. """

    __tablename__ = 'categories-ing'

    cat_i_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    cat_i_name = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "CategoryIngredient cat_i_id={} cat_i_name={}".format(
            self.cat_i_id, self.cat_i_name)


# MIDDLE TABLES

class RecipeIngredient(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    movie_id = db.Column(db.Integer,
                         db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
        return s % (self.rating_id, self.movie_id, self.user_id,
                    self.score)


# ASSOCATION TABLES


#####################################################################
# Helper functions