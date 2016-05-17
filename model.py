"""Models and database functions for project."""
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
db = SQLAlchemy(app)

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)


##############################################################################
# Model definitions

class User(db.Model):
	"""User of webapp."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	firstname = db.Column(db.String(20))
	lastname = db.Column(db.String(20))
	email = db.Column(db.String(64))
	password = db.Column(db.String(64))
	phone = db.Column(db.Integer)
	zipcode = db.Column(db.Integer)

	def __repr__(self):
		"""Provide helpful representation when printed."""

		"<User user_name=%s firstname=%s lastname=%s email=%s >" % (
			self.user_name, self.fname, self.lname, self.email)


class Event(db.Model):
	"""Table of events information."""

	__tablename__ = "events"

	event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	details_id = db.Column(db.Integer, db.ForeignKey('details.details_id'))
	api_id  = db.Column(db.String(40))
	date = db.Column(db.DateTime)

	def __repr__(self):
		"""Provide helpful representation when printed."""

		
		return "<User event_id=%s category=%s >" % (
			self.event_id, self.category)

class Attraction(db.Model):
	"""Table of attraction information."""

	__tablename__ = "attractions"

	attraction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	details_id = db.Column(db.Integer, db.ForeignKey('details.details_id'))
	api_id = db.Column(db.String(40))
	rating = db.Column(db.String(40))

	def __repr__(self):
		"""Provide helpful representation when printed."""

		return "<User attraction_id=%s category=%s >" % (
			self.event_id, self.category)

class Detail(db.Model):
	"""Table of details."""

	__tablename__ = "details"

	details_id = db.Column(db.Integer, primary_key= True)
	category = db.Column(db.String(30))
	name = db.Column(db.String(30))
	latitude = db.Column(db.Integer)
	longitutde = db.Column(db.Integer)
	address = db.Column(db.String(30))
	city = db.Column(db.String(40))
	country = db.Column(db.String(40))
	phone = db.Column(db.Integer)
	image = db.Column(db.String(40))
	url = db.Column(db.String(100))

class UserEvent (db.Model):
	"""Table of saved events in user agenda."""

	__tablename__ = "userevent"

	user_event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
	
	# remind_id = db.Column(db.String(40))


# Define relationship to user
	user = db.relationship("User",
						backref="userevents")

# Define relationship to event
	event = db.relationship("Event",
						 backref="userevents")
	
class UserAttraction (db.Model):
	"""Table of saved attraction in user agenda."""

	__tablename__ = "userattraction"

	userattraction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.attraction_id'))
	
	 # Define relationship to user
	usera = db.relationship("User",
						backref="userattraction")

##############################################################################
# Helper functions

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use our PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
	db.app = app
	db.init_app(app)


if __name__ == "__main__":
	# As a convenience, if we run this module interactively, it will leave
	# you in a state of being able to work with the database directly.

	connect_to_db(app)
	print "Connected to DB."

#  ellen = User(firstname="ellen", lastname="blakeley", email="eb@gmail.com", password="123", phone=1234567, zipcode=123456)


