import base64
import json
import unittest

import models
from app import app

MODELS = [models.Todo, models.User]


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Initialize models, create test user, and setup test app."""

        models.initialize()

        app.testing = True
        self.app = app.test_client()

        self.test_user = models.User.create_user('test', 'test@test.com', 'test')
        if not self.test_user:
            self.test_user = models.User.get(models.User.id == 1)
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Basic %s' % base64.b64encode(b'test:test').decode('ascii')
        }

    def tearDown(self):
        """Delete tables in peewee test database."""

        models.DATABASE.drop_tables(MODELS)
        models.DATABASE.close()


class TestIndex(BaseTestCase):
    def test_index_page(self):
        """Test that index page is found."""

        response = self.app.get('/',
                                headers=self.headers
                                )

        self.assertEqual(response.status_code, 200)


class TestTodoApi(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.test_task = models.Todo.create(name='test_todo1', user=self.test_user)

    def test_todos_get(self):
        """Test todo_list get method."""

        response = self.app.get('/api/v1/todos',
                                headers=self.headers
                                )
        user_todos = models.Todo.select().where(models.Todo.user_id == self.test_user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, user_todos)

    def test_todos_post(self):
        """Test todo_list post method."""

        post_data = {
            'name': 'test_todo2'
        }
        response = self.app.post('/api/v1/todos',
                                 headers=self.headers,
                                 data=json.dumps(post_data)
                                 )

        self.assertEqual(response.status_code, 201)

        new_todo = models.Todo.get(models.Todo.name == 'test_todo2')
        new_todo_dict = {
            'id': new_todo.id,
            'name': new_todo.name
        }

        self.assertEqual(json.loads(response.data), new_todo_dict)

    def test_todo_get(self):
        """Test that a user _todo can be found."""

        response = self.app.get('/api/v1/todos/1',
                                headers=self.headers
                                )
        todo = models.Todo.get(models.Todo.id == 1)
        todo_dict = {
            'id': todo.id,
            'name': todo.name
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), todo_dict)

    def test_todo_get_bad_user(self):
        """Test that todos of other users cannot be found."""

        models.User.create_user('test2', 'test2@test.com', 'test2')
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Basic %s' % base64.b64encode(b'test2:test2').decode('ascii')
        }

        response = self.app.get('/api/v1/todos/1',
                                headers=headers
                                )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.data), {
            'message': 'Todo with that id is not connected to your user.'
        })

    def test_todo_put(self):
        """Test that a user _todo can be updated."""

        put_data = {
            'id': '1',
            'name': 'test_todo3'
        }
        response = self.app.put('/api/v1/todos/1',
                                headers=self.headers,
                                data=json.dumps(put_data)
                                )

        self.assertEqual(response.status_code, 200)

        updated_todo = models.Todo.get(models.Todo.name == 'test_todo3')
        updated_todo_dict = {
            'id': updated_todo.id,
            'name': updated_todo.name
        }

        self.assertEqual(json.loads(response.data), updated_todo_dict)

    def test_todo_put_bad_user(self):
        """Test that todos of other users cannot be updated."""

        models.User.create_user('test2', 'test2@test.com', 'test2')
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Basic %s' % base64.b64encode(b'test2:test2').decode('ascii')
        }

        response = self.app.put('/api/v1/todos/1',
                                headers=headers
                                )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.data), {
            'message': 'Todo with that id is not connected to your user.'
        })

    def test_todo_delete(self):
        """Test that a user _todo can be deleted."""

        response = self.app.delete('/api/v1/todos/1',
                                   headers=self.headers
                                   )
        try:
            todo = models.Todo.get(models.Todo.id == 1)
        except models.Todo.DoesNotExist:
            todo = None

        self.assertEqual(response.status_code, 204)
        self.assertEqual(todo, None)

    def test_todo_delete_bad_id(self):
        """Test that a _todo that does not exist throw proper error."""

        response = self.app.delete('/api/v1/todos/3',
                                   headers=self.headers
                                   )

        self.assertEqual(response.status_code, 404)

    def test_todo_delete_bad_user(self):
        """Test that todos of other users cannot be deleted."""

        models.User.create_user('test2', 'test2@test.com', 'test2')
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Basic %s' % base64.b64encode(b'test2:test2').decode('ascii')
        }

        response = self.app.delete('/api/v1/todos/1',
                                   headers=headers
                                   )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(json.loads(response.data), {
            'message': 'Todo with that id is not connected to your user.'
        })


class TestUserApi(BaseTestCase):
    def test_users_post(self):
        """Test that new users can be created."""

        post_data = {
            'username': 'test2',
            'email': 'test2@test.com',
            'password': 'test2',
            'verify_password': 'test2'
        }
        response = self.app.post('/api/v1/users',
                                 headers=self.headers,
                                 data=json.dumps(post_data)
                                 )

        self.assertEqual(response.status_code, 201)

        new_user = models.User.get(models.User.username == 'test2')

        self.assertEqual(json.loads(response.data), {'username': new_user.username})

    def test_users_post_bad_password(self):
        """Test that a new user cannot be created if passwords do not match."""

        post_data = {
            'username': 'test2',
            'email': 'test2@test.com',
            'password': 'test2',
            'verify_password': 'wrong_password'
        }
        response = self.app.post('/api/v1/users',
                                 headers=self.headers,
                                 data=json.dumps(post_data)
                                 )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {
            'error': 'Password and password verification do not match'
        })

    def test_users_delete(self):
        """Test that a user can be deleted correctly."""

        response = self.app.delete('/api/v1/users',
                                   headers=self.headers
                                   )
        try:
            user = models.User.get(models.User.id == 1)
        except models.User.DoesNotExist:
            user = None

        self.assertEqual(response.status_code, 204)
        self.assertEqual(user, None)


if __name__ == "__main__":
    unittest.main()
