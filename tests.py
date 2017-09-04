""" Test file for Flask routes and database. """

# import library used for user tests
from unittest import TestCase

# import example_data function only
from model import connect_to_db, db, example_data, User, Bookmark

from server import app
from flask import session

# import file with Spoonacular API calls to mock
import api_calls

import fake_api_json


###################### LOG IN / LOG OUT / REGISTRATION ####################

class FlaskTestsLogInLogOutRegistration(TestCase):
    """Test log in and log out."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login_form_display(self):
        """ Test that login page properly showing login form. """

        result = self.client.get('/')
        self.assertIn("Log In", result.data)

    def test_registration_form_display(self):
        """ That that registration page properly showing registration form. """

        result = self.client.get('/')
        self.assertIn("Register", result.data)

    def test_correct_login(self):
        """Test log in form with correct info."""

        with self.client as c:
            result = c.post('/login',
                            data={'username': 'Bob', 'password': 'Bobpw'},
                            follow_redirects=True
                            )

            self.assertEqual(session['user_id'], 1)
            self.assertIn("Bob has successfully logged in.", result.data)

    def test_incorrect_username(self):
        """Test log in form with purposefully wrong username."""

        with self.client as c:
            result = c.post('/login',
                            data={'username': 'char', 'password': 'Bobpw'},
                            follow_redirects=True
                            )

            self.assertIn("char does not exist!", result.data)
            self.assertNotIn("char has successfully logged in.", result.data)

    def test_incorrect_password(self):
        """Test log in form with purposefully wrong password."""

        with self.client as c:
            result = c.post('/login',
                            data={'username': 'Bob', 'password': 'pw'},
                            follow_redirects=True
                            )

            self.assertIn("Incorrect password. Try again.", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('You have logged out.', result.data)

    def test_registration_correct_info(self):
        """Test that user successfully registers upon form submission."""

        with self.client as c:
            result = c.post('/register',
                            data={'username': 'Char',
                                  'email': 'Char@gmail.com',
                                  'password': 'Char1'},
                            follow_redirects=True
                            )

            # Check that success message appears
            self.assertIn("Thanks for registering Char!", result.data)

            # Check that info gets stored in DB
            current_user = User.query.filter(User.username == 'Char').first()
            self.assertIsNotNone(current_user)

    def test_registration_incorrect_info(self):
        """Test that user gets error message upon already-taken username."""

        with self.client as c:
            result = c.post('/register',
                            data={'username': 'Bob',
                                  'email': 'bob@gmail.com',
                                  'password': 'Bobpw'},
                            follow_redirects=True
                            )

            # Check that success message appears
            self.assertIn("Bob already taken. Try again!", result.data)
            self.assertNotIn("Thanks for registering Bob!", result.data)

            # Check that info does not get stored in DB
            current_user = User.query.filter(User.username == 'Bob').count()
            self.assertNotEqual(2L, current_user)

    def test_cannot_access_page(self):
        """Test that @loginrequired wrapper works, where user cannot access
        page that requires being logged in."""

        result = self.client.get('/dashboard')

        self.assertIn("Redirecting", result.data)


########################## USER PROFILE PAGE ###############################

class FlaskTestsUserProfile(TestCase):
    """Test user profile page."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_correct_page(self):
        """Test that correct page is showing up."""

        result = self.client.get('/my-profile')
        self.assertIn("User Profile", result.data)
        self.assertNotIn("Recipe Info", result.data)
        self.assertNotIn("Login Form", result.data)
        self.assertNotIn("Registration Form", result.data)

    def test_correct_username(self):
        """Test correct username is showing on the profile page."""

        result = self.client.get('/my-profile')
        self.assertIn("Bob", result.data)
        self.assertNotIn("Jane", result.data)

    def test_correct_email(self):
        """Test that correct email is showing on the profile page."""

        result = self.client.get('/my-profile')
        self.assertIn("bob@gmail.com", result.data)
        self.assertNotIn("jane@gmail.com", result.data)

    def test_correct_bookmarks(self):
        """Test that correct bookmarked recipes is showing on the profile page."""

        result = self.client.get('/my-profile')
        self.assertIn("Thai Sweet Potato", result.data)
        self.assertNotIn("Meatless Burgers with Romesco and Arugula", result.data)

######################### INITIAL DASHBOARD PAGE ##############################


class FlaskTestsDashboard(TestCase):
    """Test dashboard page."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_correct_info(self):
        """ Test that what is supposed to show up in initial page is indeed showing. """

        result = self.client.get('/dashboard')
        self.assertIn("Dashboard", result.data)
        self.assertIn("Search Recipe:", result.data)
        self.assertIn("Create New List:", result.data)
        self.assertIn("Current Grocery List", result.data)

    def test_no_search_results(self):
        """ Test that search results are not showing upon initial load. """

        result = self.client.get('/dashboard')
        self.assertNotIn("Bookmark", result.data)
        self.assertNotIn("Add To List", result.data)

########################## ADD NEW LIST FEATURE ###############################


class FlaskTestsAddNewList(TestCase):
    """Test add new list feature from server side."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_new_list(self):
        """ Test successful dictionary if list does not exist. """

        with self.client as c:
            result = c.post('/new-list.json',
                            data={'new_list_name': "Snack"},
                            follow_redirects=True
                            )

            # Check for components in dictionary (list name, list, id)
            self.assertIn("Snack", result.data)  # Check that list name is Snack
            self.assertIn("4", result.data)  # Check that list id is 4

    def test_list_already_exists(self):
        """ Test that error message appears if user triesto add
        already-existing list. """

        with self.client as c:
            result = c.post('/new-list.json',
                            data={'new_list_name': "Breakfast"},
                            follow_redirects=True
                            )

            self.assertIn("That list already exists. Try again!", result.data)

########################### BOOKMARK FEATURE #################################


class FlaskTestsBookmark(TestCase):
    """Test bookmark feature from server side."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_already_existing_bookmark(self):
        """ Test if error message appears with already-bookmarked recipe. """

        with self.client as c:
            result = c.post('/bookmark.json',
                            data={'recipe_id': '262682'},
                            follow_redirects=True
                            )

            self.assertIn("You've already bookmarked this recipe.", result.data)

    def test_new_bookmark(self):
        """ Test if success message appears with bookmarking a new recipe. """

        # Check that bookmark did not exist before
        check = Bookmark.query.filter((Bookmark.recipe_id == '227961') & (Bookmark.user_id == 1)).first()
        self.assertIsNone(check)

        with self.client as c:
            result = c.post('/bookmark.json',
                            data={'recipe_id': '227961'},
                            follow_redirects=True
                            )

            # Check that success message appears
            self.assertIn("This recipe has been bookmarked!", result.data)

            # Check that new bookmark now successfully added
            current_bookmark = Bookmark.query.filter((Bookmark.recipe_id == '227961') & (Bookmark.user_id == 1)).first()
            self.assertIsNotNone(current_bookmark)

    def test_existing_bookmark(self):
        """ Test if error message appears with an already-bookmarked recipe. """

        with self.client as c:
            result = c.post('/bookmark.json',
                            data={'recipe_id': '262682'},
                            follow_redirects=True
                            )

            # Check that error message appears
            self.assertIn("You've already bookmarked this recipe.", result.data)

            # Check that bookmark does not get duplicated in DB
            current_bookmark = Bookmark.query.filter((Bookmark.recipe_id == '262682') & (Bookmark.user_id == 1)).count()
            self.assertEqual(1L, current_bookmark)

########################## ADD TO LIST FEATURE ###############################


class FlaskTestsAddIngredientsToList(TestCase):
    """Test add-ingredients-to-list feature from server side."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_add_to_list_process(self):
        """ Check that ajax success function is getting correct ingredient
        information back to be displayed in grocery list. """

        with self.client as c:
            result = c.post('/add-to-list.json',
                            data={'recipeId': '262682',
                                  'listId': 1},
                            follow_redirects=True
                            )

            self.assertIn('15', result.data)  # Mass qty
            self.assertIn('ounce', result.data)  # Meas Unit
            self.assertIn('canned chickpeas', result.data)  # Ing name
            self.assertIn('Canned and Jarred', result.data)  # Aisle name
            self.assertIn('1', result.data)  # Aisle id

########################## RECIPE INFO PAGE ###############################


class FlaskTestsRecipeInfo(TestCase):
    """Test recipe info page."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_correct_layout(self):
        """ Test that page displays name, cuisine, ingredients, and cooking
        instructions. """

        result = self.client.get('/recipe-info/262682')
        self.assertIn("Ingredients", result.data)
        self.assertIn("Cooking Instructions", result.data)


########################### MOCK API #################################

class MockFlaskTests(TestCase):
    """Test routes that include a Spoonacular API call."""

    def setUp(self):
        """Before every test"""

        app.config['TESTING'] = True
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Make mock
        def _mock_recipe_search(search_name, recipe_id):
            """ Mocks info returned from Spoonacular API. """

            example_search = fake_api_json.recipe_search('pasta', 1)

            return example_search

        def _mock_summary_info(recipe_id):
            """ Mocks info returned from Spoonacular API. """

            example_summary = fake_api_json.summary_info('548180')

            return example_summary

        def _mock_recipe_info(recipe_id):
            """ Mocks info returned from Spoonacular API. """

            example_info = fake_api_json.recipe_info('548180')

            return example_info

        # Attaches mocks calls to app's real calls
        api_calls.recipe_search = _mock_recipe_search
        api_calls.summary_info = _mock_summary_info
        api_calls.recipe_info = _mock_recipe_info

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_search_results(self):
        """Test accuracy of combining two jsons together from 2 API calls.
        Particularly check if summary key was added to original json."""

        results = self.client.get('/search.json', query_string={"recipe_search": "pasta",
                                                                "number_of_results": 1})

        self.assertIn("Italian Sausage Tortellini Soup", results.data)
        self.assertIn('"summary": "Italian Sausage Tortellini Soup', results.data)

    def test_recipe_info_page(self):
        """Test accuracy of API call into displaying correct info at
        detailed recipe page."""

        results = self.client.get("/recipe-info/'548180")

        self.assertIn("Italian Sausage Tortellini Soup", results.data)
        self.assertIn("Remove the bay leaf and serve", results.data)

if __name__ == "__main__":
    import unittest

    unittest.main()
