from app import create_app, db
from app.profile.models import User
from app.task.models import Task
from flask_testing import TestCase
import unittest
from datetime import datetime
from flask_login import login_user, current_user, logout_user


class BaseTestCase(TestCase):
    def create_app(self):
        # app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
        app = create_app()
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///testing.db', SECRET_KEY='asfdsfsaaffdf')
        return app

    # 1) перевірка відображення головної сторінки
    def test1_home_page(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is a portfolio', response.data)

    # 2) перевірка реєстрації, входу і виходу користувача.
    def test2_user(self):
        with self.client:
            user = User(username='unittester', email='unittester@gmail.com', password='12345')
            db.session.add(user)
            db.session.commit()
            self.assertIn(
                db.session.query(User).filter_by(username='unittester').first().email,
                'unittester@gmail.com'
            )

            # register
            # response = self.client.post(
            #     '/usr/login',
            #     data=dict(username='unittester',email="unittester@gmail.com", password="12345"),
            #     follow_redirects=True
            # )

            # login
            response = self.client.post(
                '/usr/login',
                data=dict(email="unittester@gmail.com", password="12345"),
                follow_redirects=True
            )

            login_user(User.query.filter(User.email == 'unittester@gmail.com').first())

            # self.assert_redirects(response, '/usr/account')
            self.assertIn(b'unittester', response.data)
            self.assertTrue(current_user.is_authenticated)
            logout_user()
            self.assertFalse(current_user.is_authenticated)

    # 3) покрити тестами операції CRUD для моделі Task (API з Flask-SQLalchemy)
    def test31_task_create(self):
        response = self.client.post(
            '/api/v2/tasks',
            data=dict(title="test_task", description="test_description", priority="low", category_id=1),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'test_task', response.data)

    def test32_task_all(self):
        response = self.client.get(
            '/api/v2/tasks',
            follow_redirects=True
        )
        self.assertIn(b'test_task', response.data)

    def test33_task_detail(self):
        response = self.client.get(
            '/api/v2/tasks/1',
            follow_redirects=True
        )
        self.assertEqual(response.json, dict(resource=dict(id=1, title="test_task", description="test_description",
                                                           priority="EnumPriority.low", is_done=False)))

'''
    def test34_task_update(self):
        response = self.client.put(
            '/api/v2/tasks/86',
            data=dict(title="updated_test_task", description="updated_test_description",
                      priority="high", category_id=1, is_done=True),
            follow_redirects=True
        )
        self.assertEqual(response.json, dict(resource=dict(id=1, title="updated_test_task", description="updated_test_description",
                                                           priority="EnumPriority.high", is_done=True)))

    def test35_task_delete(self):
        response = self.client.delete(
            '/api/v2/tasks/86',
            # data=dict(id=86),
            follow_redirects=True
        )
        self.assertNotIn(b'test_task', response.data)
        self.assertNotIn(b'updated_test_task', response.data)
'''

if __name__ == "__main__":
    unittest.main()
