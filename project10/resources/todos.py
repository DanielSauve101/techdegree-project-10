from flask import Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                           inputs, marshal_with, url_for)

import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'completed': fields.Boolean
}


def todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id==todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name for todo provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            default=False,
            help='Requires true or false',
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields)
                for todo in models.Todo.select()]
        return {'todos': todos}

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo, 201, {
            'Location': url_for('resources.todos.todo', id=todo.id)
            })


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name for todo provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            default=False,
            help='Requires true or false',
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id==id)
        query.execute()
        return (models.Todo.get(models.Todo.id==id), 200, 
               {'Location': url_for('resources.todos.todo', id=id)})

    def delete(self, id):
        query = models.Todo.delete().where(models.Todo.id==id)
        query.execute()
        return ('', 204, {'Location': url_for('resources.todos.todos')})


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)
