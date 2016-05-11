# TODO
# 1) set up DB to store user/ events- DEBUG model.py server.py
# 
# 3) Fix routes- login, home (search, my events, twilio)
# 
#
# 4) Find events and restaurants, save to 'My Wanderings', set twilio reminders
# about what I'm attending. Invite others with twilio. 

# Wanderseek 


"""Models and database functions for project."""
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

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

    # def __repr__(self):
    #      """Provide helpful representation when printed."""

    #     return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Event(db.Model):
    """Table of events."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(30))
    name = db.Column(db.String(30))
    latitude = db.Column(db.Integer)
    longitutde = db.Column(db.Integer)
    city = db.Column(db.String(40))
    country = db.Column(db.String(40))
    phone = db.Column(db.Integer)

    # Define relationship to user
    # user = db.relationship("User",
    #                        backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to movie
    # movie = db.relationship("Movie",
    #                         backref=db.backref("ratings", order_by=rating_id))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
    #         self.rating_id, self.movie_id, self.user_id, self.score)

class Plans (db.Model):
    """Table of saved events in user agenda."""

    __tablename__ = "agenda"

    event_agenda__id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    remind_id = db.Column(db.String(40))
 
 # Define relationship to user
    user = db.relationship("User",
                        backref="users")

# Define relationship to event
    event = db.relationship("Event",
                         backref="events")
    
    

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

    from server import app
    connect_to_db(app)
    print "Connected to DB."

