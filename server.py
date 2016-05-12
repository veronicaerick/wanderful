
##############################################################################
				##### CONTROLLER, ROUTES, VIEW  ####
##############################################################################
#!/usr/bin/python -tt
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from yelpapi import YelpAPI 
from pprint import pprint
import os 
import yelp
import json

# IMPORTED MODEL TABLES TO ROUTES
from model import User, Event, Attraction, Plan
from model import connect_to_db, db

##############################################################################

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

##############################################################################
							# Yelp API tokens
##############################################################################


consumer_key=os.environ.get('YELP_CONSUMER_KEY')
consumer_secret=os.environ.get('YELP_CONSUMER_SECRET')
token=os.environ.get('YELP_ACCESS_TOKEN_KEY')
token_secret=os.environ.get('YELP_ACCESS_TOKEN_SECRET')

yelp_api = YelpAPI(consumer_key, consumer_secret, token, token_secret)


##############################################################################
							# HOME PAGE/SEARCH FIELD
##############################################################################

@app.route('/')
def index():
	"""Render homepage plus search field for location."""

	return render_template("homepage.html")


@app.route("/search_results", methods=["POST"])
def search_process():
	"""Search events."""
	
	location = request.form['location']
	return render_template("results_page.html" attractions=attractions)

def get_attractions(location):

	search_results = yelp_api.search_query(location=location, term=attractions, limit=limit)
	#parse out data and return attractions dict. 

@app.route("/add_to_events")
def add_to_events():
	"""Ajax route to add events and add the event to the user agenda."""
	
	api_id = request.args.get("api_id")

@app.route("/my_agenda")
def my_agenda():
	"""Render user's saved events and attractions."""

@app.route("/attractions_to_events")
def attractions_to_events():
	"""Whens user submits dates in input field for attractions, they are now saved as events(by adding date)."""



##############################################################################
						## REGISTER ROUTES ##
##############################################################################

@app.route('/register', methods=['GET'])
def register_form():
	"""Show form for user signup."""

	return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
	"""Process registration."""

	# Get form variables
	email = request.form["email"]
	password = request.form["password"]
	age = int(request.form["age"])
	zipcode = request.form["zipcode"]

	new_user = User(email=email, password=password, age=age, zipcode=zipcode)

	db.session.add(new_user)
	db.session.commit()

	flash("User %s added." % email)
	return redirect("/")

##############################################################################
						## LOGIN ROUTES ##
##############################################################################

@app.route('/login', methods=['GET'])
def login_form():
	"""Show login form."""

	return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
	"""Process login."""

	# Get form variables
	email = request.form["email"]
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	if not user:
		flash("No such user")
		return redirect("/login")

	if user.password != password:
		flash("Incorrect password")
		return redirect("/login")

	session["user_id"] = user.user_id

	flash("Logged in")
	return redirect("/")

##############################################################################
						## LOGOUT ROUTES ##
##############################################################################

@app.route('/logout')
def logout():
	"""Log out."""

	del session["user_id"]
	flash("Logged Out.")
	return redirect("/")


##############################################################################
						# HELPER FUNCTIONS
##############################################################################

if __name__ == "__main__":
	# We have to set debug=True here, since it has to be True at the point
	# that we invoke the DebugToolbarExtension
	app.debug = True

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run()
