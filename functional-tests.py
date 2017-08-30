""" Functional testing app's UI. """

from selenium import webdriver
import unittest

from time import sleep


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.PhantomJS()

        self.browser.get('http://localhost:5000/')

        username = self.browser.find_element_by_id('username')
        username.send_keys("charlotte")

        password = self.browser.find_element_by_id('password')
        password.send_keys("charlotte")

        search = self.browser.find_element_by_id('submit-login')
        search.click()

    def tearDown(self):
        self.browser.quit()

    def test_recipe_search_button(self):

        search = self.browser.find_element_by_id('recipe-search')
        search.send_keys("burger")

        btn = self.browser.find_element_by_id('submit-search')
        btn.click()

        sleep(10)

        result = self.browser.find_element_by_id('recipes')
        self.assertNotIn("Healthy Salmon Quinoa Burgers", result.text)


if __name__ == "__main__":
    import unittest

    unittest.main()
