
## have two route, first route is a wait page. on page have JS do an ajax call as soon as page loads to get second route results 
### 
##############################################################################

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from yelpapi import YelpAPI 
from pprint import pprint
import os 
import yelp_results
import eventbrite_results
import json
from twilio.rest import TwilioRestClient 

############################################# IMPORTED MODEL TABLES TO ROUTES
from model import User, Event, Attraction, UserEvent, UserAttraction
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


@app.route("/process_search", methods=["GET"])
def search_process():
	"""Process the search and show results"""
	
	location = request.args.get('location')
	term = request.args.get('term')
	datestring = request.args.get('date')

	print "date", type(datestring)
	print "location", location

	yelp_result = yelp_results.get_business_results(location, term)
	eventbrite_result = eventbrite_results.get_event_results(location, datestring)
	
	return render_template("search_results.html", location=location,yelp_result=yelp_result, eventbrite_result=eventbrite_result)


##############################################################################
##############################################################################
							# SEARCH PROCESS AND RESULTS


@app.route("/add_to_attractions", methods=['POST'])
def add_to_attractions():
	"""Ajax route to add attractions and add the attraction to the user agenda."""

	# grab yelp API results
	name = request.form.get("name")
	location = request.form.get("address")
	latitude = request.form.get("latitude")
	longitude = request.form.get("longitude")
	phone = request.form.get("phone")
	image = request.form.get("image")
	url = request.form.get("url")
	rating = request.form.get("rating")
	review_count = request.form.get("review_count")

	# check to see if api id is in DB
	find_attraction = Attraction.query.filter_by(name=name).first()
	# if not, add to DB
	if find_attraction:
		add_attraction = find_attraction
	else:
		add_attraction = Attraction(name=name, location=location, latitude=latitude,
									phone=phone, image=image, url=url,
									rating=rating, review_count=review_count)
		db.session.add(add_attraction)
		db.session.commit()

	# print add_attraction
	user = User.query.get(session['user_id'])	
	attraction = Attraction.query.get(add_attraction.attraction_id)
	
	print user.user_id
	print add_attraction.attraction_id
	
	userattraction = UserAttraction(user_id=user.user_id, attraction_id=attraction.attraction_id)
	db.session.add(userattraction)
	db.session.commit()
	return "yay"

@app.route("/add_to_events", methods=['POST'])
def add_to_events():
	"""Ajax route to add events and add the event to the user agenda."""

	# query EB data
	name = request.form.get("name")
	start = request.form.get("start")
	status = request.form.get("status")
	url = request.form.get("url")
	locale = request.form.get("locale")
	
	print start
	# d = datetime.strptime(start, "%Y-%m-%d")
	# print d

	# strptime to make it date and strftime to format to user view

	# check to see if api id is in DB
	find_event = Event.query.filter_by(name=name).first()
	# if not, add to DB
	if find_event:
		add_event = find_event
		flash("Already added to your agenda")
	if not find_event:
		add_event = Event(name=name, start=start, status=status,
									url=url, locale=locale)
		db.session.add(add_event)
		db.session.commit()

	user = User.query.get(session['user_id'])
	event = Event.query.get(add_event.event_id)

	userevent = UserEvent(user_id=user.user_id, event_id=event.event_id)
	db.session.add(userevent)
	db.session.commit()
	return "yay"

@app.route("/delete_attr", methods=["POST"])
def delete_attr():
    """Allows user to remove attr from DB"""

    user = User.query.get(session['user_id'])
    attraction_id = request.form.get('attraction_id')
    
    find_attraction = UserAttraction.query.filter_by(user_id=user.user_id, attraction_id=attraction_id).first()
    if find_attraction:
    	db.session.delete(find_attraction)
    	db.session.commit()
	if not find_attraction:
		return "didnt find attraction in DB"
   	

    return attraction_id

@app.route("/delete_event", methods=["POST"])
def delete_event():
    """Allows user to remove event from DB"""

    user = User.query.get(session['user_id'])
    event_id = request.form.get('event_id')
    
    find_event = UserEvent.query.filter_by(user_id=user.user_id, event_id=event_id).first()
   	
    db.session.delete(find_event)
    db.session.commit()

    return event_id


@app.route("/my_agenda")
def my_agenda():
	"""Render user's saved events and attractions."""
	
	user = User.query.get(session['user_id'])

	userattractions = UserAttraction.query.filter_by(user_id=user.user_id).all()
	userevents = UserEvent.query.filter_by(user_id=user.user_id).all()
	

	return render_template("my_agenda.html", user=user, userattractions=userattractions, userevents=userevents)

@app.route("/calendar")
def calendar():

	user = User.query.get(session['user_id'])
	userevents = UserEvent.query.filter_by(user_id=user.user_id).all()
	
	event_list = []

	for userevent in userevents:
		event_dict = {}
		title = userevent.event.name
		start = userevent.event.start
		event_dict["title"] = title
		event_dict["start"] = start
		event_list.append(event_dict)

	event_results = {"events": event_list}
	return jsonify(event_results) 


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

	user = User.query.filter_by(email=email).first()
	session["user_id"] = user.user_id

	flash("User %s added." % email)
	return redirect("/")

@app.route('/twilio', methods=['POST'])
def twilio():
 
 	message = request.form.get('message')
 	
	ACCOUNT_SID = "AC3a959eac16c2ec0874ea33ac53d6e021" 
	AUTH_TOKEN = "264e6637c88819c5b5d6c4a4579c4e37" 
 
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
	client.messages.create(
		to="+17076960691", 
		from_="+17073311083", 
		body=message) 
	
	return redirect("/my_agenda")

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
	# DebugToolbarExtension(app)

	app.run()
