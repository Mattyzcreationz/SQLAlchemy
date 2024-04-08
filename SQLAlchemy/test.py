import unittest
from flask import current_app
from app import app, db, User

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Create the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize the database and create all tables
        with app.app_context():
            db.init_app(app)
            db.create_all()

        # Set up the test client after creating the application context
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test."""
        # Drop all database tables
        db.session.remove()
        db.drop_all()

        # Remove the application context
        self.app_context.pop()

    # Your test methods here

if __name__ == '__main__':
    unittest.main()
