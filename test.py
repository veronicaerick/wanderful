import json
from unittest import TestCase
from model import User, Event, Attraction, UserEvent, UserAttraction, connect_to_db, db
from server import app
import server


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        server.app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("<p>Wander your way.</p>", result.data)

    def test_search_page(self):
        """Test search page."""

        result = self.client.get("/process_search")
        self.assertIn("<p>hi</p>", result.data)

    def test_agenda_page(self):
        """Test search page."""

        result = self.client.get("/my_agenda")
        self.assertIn("<p>hi</p>", result.data)

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    # def test_search_page(self):
    #     """Test results page."""

    #     result = self.client.get("/process_search")
    #     self.assertIn("<h1 class ='header'> Results for {{location}}: </h1>", result.data)


    # def test_agenda_details(self):
    #     """Test agenda page."""

    #     result = self.client.get("/my_agenda")
    #     self.assertIn("saved", result.data)





class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


if __name__ == "__main__":
    import unittest

    unittest.main()
