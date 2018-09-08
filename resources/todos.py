from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for, abort

import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String
}


def get_todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
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
    def get(self):
        """Returns a list of all todos."""

        todos = [marshal(todo, todo_fields) for todo in models.Todo.select()]

        return todos

    @marshal_with(todo_fields)
    def post(self):
        """Creates a new todos and returns."""

        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)

        return todo, 201, {'Location': url_for('resources.todos.todo', todo_id=todo.id)}


class Todos(TodoBase):
    @marshal_with(todo_fields)
    def get(self, todo_id):
        """Returns a single todos."""

        todo = get_todo_or_404(models.Todo.get(models.Todo.id == todo_id))

        return todo

    @marshal_with(todo_fields)
    def put(self, todo_id):
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == todo_id)
        query.execute()

        return models.Todo.get(models.Todo.id == todo_id), 200, {
            'Location': url_for('resources.todos.todo', todo_id=todo_id)}

    def delete(self, todo_id):
        query = models.Todo.delete().where(models.Todo.id == todo_id)
        query.execute()

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
