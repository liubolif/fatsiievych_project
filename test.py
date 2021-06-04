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
        print('-test1_home_page finished')

    # 2) перевірка реєстрації, входу і виходу користувача.
    def test2_user(self):
        with self.client:
            user = User(username='unittester1', email='unittester1@gmail.com', password='12345', admin=True)
            db.session.add(user)
            db.session.commit()
            self.assertIn(
                User.query.filter_by(username='unittester1').first().email,
                'unittester1@gmail.com'
            )

            user1 = User.query.filter(User.email == 'unittester1@gmail.com').first()
            self.assertEqual(user, user1)

            login_user(user1)
            self.assertTrue(current_user.is_authenticated)
            logout_user()
            self.assertFalse(current_user.is_authenticated)

            db.session.delete(user)
            db.session.commit()
            print('-test2_user finished')

    # 3) покрити тестами операції CRUD для моделі Task (API з Flask-SQLalchemy)
    def test31_task_create(self):
        response = self.client.post(
            '/api/v2/tasks',
            data=dict(title="test_task", description="test_description", priority="low", category_id=1),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 201)
        data_json = response.json
        del data_json['created']
        self.assertEqual(data_json, dict(id=6, title="test_task", description="test_description",
                                         priority="EnumPriority.low", category=None, is_done=False))

        # unsuccessful request
        response2 = self.client.post(
            '/api/v2/tasks',
            data=dict(title=110, description="jdfjlkdsfjsdf", priority="super", category_id=1),
            follow_redirects=True
        )
        self.assertEqual(response2.status_code, 400)
        print('-test31_task_create finished')

    def test32_task_all(self):
        response = self.client.get(
            '/api/v2/tasks',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_task', response.data)
        print('-test32_task_all finished')

    def test33_task_detail(self):
        response = self.client.get(
            '/api/v2/tasks/6',
            follow_redirects=True
        )

        data_json = response.json
        del data_json['created']
        self.assertEqual(data_json, dict(id=6, title="test_task", description="test_description",
                                         priority="EnumPriority.low", category=None, is_done=False))

        response2 = self.client.get(
            '/api/v2/tasks/666',
            follow_redirects=True
        )
        self.assertEqual(response2.status_code, 404)
        print('-test33_task_detail finished')

    def test34_task_update(self):
        response = self.client.put(
            '/api/v2/tasks/6',
            data=dict(title="updated_test_task", description="updated_test_description",
                      priority="high", category_id=1, is_done=True),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 201)
        data_json = response.json
        del data_json['created']
        self.assertEqual(data_json, dict(id=6, title="updated_test_task", description="updated_test_description",
                                         priority="EnumPriority.high", category=None, is_done=True))
        print('-test34_task_update finished')

    def test35_task_delete(self):
        response = self.client.delete(
            '/api/v2/tasks/6',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 204)
        self.assertNotIn(b'updated_test_task', response.data)
        print('-test35_task_delete finished')


if __name__ == "__main__":
    unittest.main()
