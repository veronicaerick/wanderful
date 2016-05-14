
##############################################################################

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from yelpapi import YelpAPI 
from pprint import pprint
import os 
import yelp_results
import json

############################################# IMPORTED MODEL TABLES TO ROUTES
from model import User, Event, Attraction, Detail, UserEvent, UserAttraction
from model import connect_to_db, db

##############################################################################

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

##############################################################################
##############################################################################
							# HOME PAGE/SEARCH FIELD


@app.route('/')
def index():
	"""Render homepage plus search field for location."""

	return render_template("homepage.html")

##############################################################################
##############################################################################
							# SEARCH PROCESS AND RESULTS


@app.route("/process_search", methods=["POST"])
def search_process():
	"""Search events."""
	
	location = request.form.get('location')
	term = request.form.get('term')
	

	api_results = yelp_results.get_business_results(location, term)
	
	return render_template("search_results.html", api_results=api_results)


##############################################################################
##############################################################################
							# SEARCH PROCESS AND RESULTS


@app.route("/add_to_attractions", methods=['POST'])
def add_to_attractions():
	"""Ajax route to add events and add the event to the user agenda."""
	
	# query yelp data
	user_id = request.args.get("user_id")
	api_id = request.args.get("api_id")
	details_id = request.args.get("details_id")
	category = request.args.get("category")
	name = request.args.get("name")
	latitude = request.args.get("latitude")
	longitutde = request.args.get("longitutde")
	address = request.args.get("address")
	city = request.args.get("city")
	country = request.args.get("country")
	phone = request.args.get("phone")
	image = request.args.get("image")

	# check to see if api id is in DB
	find_attraction = Attraction.query.filter_by(api_id).first()
	# if not, add to DB
	if not find_attraction:
		added_attraction = Attraction(attraction_id=attraction_id, details_id = details_id, api_id =api_id)

	db.session.add(added_attraction)
	db.session.commit()


@app.route("/my_agenda")
def my_agenda():
	"""Render user's saved events and attractions."""

@app.route("/attractions_to_events")
def attractions_to_events():
	"""Whens user submits dates in input field for attractions, they are now saved as events(by adding date)."""



##############################################################################
##############################################################################
								# LOGIN ROUTES 

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
##############################################################################
							# REGISTER ROUTES 


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
	firstname = request.form["firstname"]
	lastname = request.form["lastname"]
	phone = request.form["phone"]
	zipcode = request.form["zipcode"]

	new_user = User(email=email, password=password, firstname=firstname,
	lastname=lastname, phone=phone, zipcode=zipcode)

	db.session.add(new_user)
	db.session.commit()

	flash("User %s added." % email)
	return redirect("/")

##############################################################################
##############################################################################
							# LOGOUT ROUTES 


@app.route('/logout')
def logout():
	"""Log out."""

	del session["user_id"]
	flash("Logged Out.")
	return redirect("/")

##############################################################################
##############################################################################
							# HELPER FUNCTIONS


if __name__ == "__main__":
	# We have to set debug=True here, since it has to be True at the point
	# that we invoke the DebugToolbarExtension
	app.debug = True

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run()
