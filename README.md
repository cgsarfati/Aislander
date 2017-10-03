![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/homepage.png)

Aislander is intended to automate a task we all spend too much time on: manually creating a grocery list. This project takes into account that we meal plan differently than we shop.  By considering various permutations of how a user might interface with their data, this app creates a planning interface and a shopping plan where the priority is efficiency in the store. 

[View full video demo.](https://www.youtube.com/watch?v=rHoRXGNCmI8)

## Table of Contents
* [Technologies](#technologies)
* [Features](#features)
* [Installation](#installation)
* [Future Features](#future-features)
* [Author](#author)

## Technologies

* Backend: Python, Flask, PostgreSQL, SQLAlchemy
* Frontend: JavaScript, jQuery, AJAX, JSON, Jinja2, HTML5, CSS, Bootstrap
* API: Spoonacular API

## Features
![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/Login.gif)
Users can log in or register in the homepage, where the data is stored after password hashing to the PostgreSQL database. Registered users have a personalized dashboard only they have access to once logged in.

![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/AddToggleList.gif)
Once a user is logged in, it will lead to the dashboard page, where users can create grocery lists via AJAX POST requests, and access previously saved ones. There is also a progress bar on top, guiding new users via a step-by-step tutorial.

![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/Search.gif)
Users can also search for recipes, triggering Spoonacular API calls to access recipe data upon clicking the search button. A loading button is installed to provide user feedback.

![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/AddRecipe.gif)
If users want to append a recipe's ingredients into a grocery list, they can click the shopping cart button. The grocery list is organized by aisle categories, saving users from scavenger hunting in grocery stores.

![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/AddAnotherRecipe.gif)
When adding additional recipes, ingredients either append to existing aisles, or creating a new aisle in the process. 

![Homepage](https://raw.githubusercontent.com/cgsarfati/hb-grocery-app/master/static/img/Bookmark.gif)
Lastly, users can bookmark recipes via AJAX POST requests, which can be accessed in their profile page. The profile page includes user info as well as a Bootstrap carousel of the bookmarked recipes' images. Jinja2 was particularly used here to standardize the layout schema of all profile pages.

## Installation

To run Aislander:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/cgsarfati/hb-grocery-app.git
```

To have this app running on your local computer:
Create and activate a virtual environment inside your ChefBox directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Sign up to use the [Spoonacular API](https://spoonacular.com/food-api).

Save your API key in a file called secrets.sh using this format:

```
export YOURKEY="YOURKEYHERE"
```

In the same file called secrets.sh, designate any secret key to use the Flask app:

```
export FLASK_SECRET_KEY="YOURKEYHERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Create database 'groceries'.
```
createdb groceries
```
Create your database tables
```
python model.py
```


Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to start exploring Aislander. Happy grocery listing!

## Future-Features
* Repeating ingredients will increment in measurement values rather than duplicating.
* Users can access the recipes included in each grocery list.
* A grocery store locator feature using the GoogleMaps API where users can locate the nearest grocery stores based on their current location that has all the ingredients in the store inventory.
* Expanding on the recipe search filter (e.g. dietary restrictions, calories, etc.)
* Utilizing data visualizations (either via Chart.js or D3) in the user profile page or in the dashboard page. For instance, each grocery list having a dynamic pie chart where users can see which aisles contain the most ingredients in their list.

## Author

Hi! I'm [Charlotte Sarfati](https://www.linkedin.com/in/cgsarfati/), a nurse-turned-software engineer who graduated from a full-stack coding bootcamp, Hackbright Academy, on September 2017.

Previously, I pursued an undergraduate Nursing degree at USF, ultimately obtaining my RN license in September, 2016. During the program, I acquired 3 years of hands-on nursing experience in hospitals such as UCSF and Stanford, doing 12-hour shifts in specialties such as labor and delivery, ICU, and pediatrics. 

While I still believe nursing is one of the noblest professions, my transition to computer programming stems from my itch to become a "modern inventor". The ability to unlock human potential through automation and the never-ending learning embedded in this industry perfectly align with my aspirations.

I'm currently seeking a full-time software developer role in the San Francisco Bay Area or New York City. Feel free to reach out at sarfati.charlotte@gmail.com or connect with me on [LinkedIn](https://www.linkedin.com/in/cgsarfati/)!

