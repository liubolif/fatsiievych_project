from urllib.request import urlopen

from app import app, db, Student
from flask_testing import TestCase
import unittest


class BaseTestCase(TestCase):
    def create_app(self):
        # let's use SQLite3 as it is much faster to test with than a larger postgres DB
        # app.config.from_object('config.TestConfiguration')
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        return app

    def setUp(self):
        db.create_all()
        person1 = Student("Elie", "Schoppik")
        person2 = Student("Tim", "Garcia")
        person3 = Student("Matt", "Lane")
        db.session.add_all([person1, person2, person3])
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

    def test_index(self):
        response = self.client.get('/students', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Elie Schoppik', response.data)
        self.assertIn(b'Tim Garcia', response.data)
        self.assertIn(b'Matt Lane', response.data)


'''


    def test_show(self):
        response = self.client.get('/students/1')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            '/students',
            data=dict(first_name="New", last_name="Student"),
            follow_redirects=True
        )
        self.assertIn(b'New Student', response.data)

    def test_edit(self):
        response = self.client.get(
            '/students/1/edit'
        )
        self.assertIn(b'Elie', response.data)
        self.assertIn(b'Schoppik', response.data)

    def test_update(self):
        response = self.client.patch(
            '/students/1',
            data=dict(first_name="updated", last_name="information"),
            follow_redirects=True
        )
        self.assertIn(b'updated information', response.data)
        self.assertNotIn(b'Elie Schoppik', response.data)

    def test_delete(self):
        response = self.client.delete(
            '/students/1',
            follow_redirects=True
        )
        self.assertNotIn(b'Elie Schoppik', response.data)
'''

if __name__ == '__main__':
    unittest.main()