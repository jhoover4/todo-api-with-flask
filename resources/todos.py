import json

from flask import Blueprint, make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for, abort

import models
from auth import basic_auth, g

todo_fields = {
    'id': fields.Integer,
    'name': fields.String
}


def get_todo_or_abort(todo_id):
    """"Checks that a _todo exists and is connected to user."""

    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        if todo.user_id != g.user.id:
            abort(405, message='Todo with that id is not connected to your user.')

        return todo


class TodoBase(Resource):
    """Base class for both types of todos resource."""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided.',
            location=['form', 'json']
        )

        super().__init__()


class TodoList(TodoBase):
    @basic_auth.login_required
    def get(self):
        """Returns a list of all todos associated with user."""

        todos = [marshal(todo, todo_fields) for todo in models.Todo.select().where(models.Todo.user_id == g.user.id)]

        return todos

    @marshal_with(todo_fields)
    @basic_auth.login_required
    def post(self):
        """Creates a new _todo, todos do not need unique names so they will always be created."""

        args = self.reqparse.parse_args()
        todo = models.Todo.create(user=g.user, **args)

        return todo, 201, {'Location': url_for('resources.todos.todo', todo_id=todo.id)}


class Todos(TodoBase):
    @marshal_with(todo_fields)
    @basic_auth.login_required
    def get(self, todo_id):
        """Returns a single _todo."""

        todo = get_todo_or_abort(todo_id)

        return todo

    @marshal_with(todo_fields)
    @basic_auth.login_required
    def put(self, todo_id):
        """Updates a single _todo."""

        get_todo_or_abort(todo_id)

        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == todo_id)
        query.execute()

        return models.Todo.get(models.Todo.id == todo_id), 200, {
            'Location': url_for('resources.todos.todo', todo_id=todo_id)}

    @basic_auth.login_required
    def delete(self, todo_id):
        """Deletes a _todo if it is associated with the current user."""

        todo = get_todo_or_abort(todo_id)
        todo.delete_instance()

        return '', 204


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)

api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todos,
    '/api/v1/todos/<int:todo_id>',
    endpoint='todo'
)
