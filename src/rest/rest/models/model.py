from bson import ObjectId
from datetime import datetime
import json, logging, os
from pymongo import MongoClient

mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']
collection = db['todos']

class MongoTodoItem:
    def __init__(self, title: str,  created_at: datetime = None, updated_at: datetime = None):
        self.title = title
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()


    @staticmethod
    def from_django_model(django_todo):
        return MongoTodoItem(
        title=django_todo.title,
        created_at=django_todo.created_at,
        updated_at=django_todo.updated_at
    )

    @staticmethod
    def from_mongo_data(mongo_data):
        return MongoTodoItem(
            title=mongo_data['title'],
            created_at=mongo_data['created_at'],
            updated_at=mongo_data['updated_at']
        )

    @staticmethod
    def to_django_model(mongo_todo):
        from rest.schema.todo import TodoItem as DjangoTodoItem
        return DjangoTodoItem(
            title=mongo_todo.title,
            created_at=mongo_todo.created_at,
            updated_at=mongo_todo.updated_at
        )

    @staticmethod
    def get_all():
        mongo_todos = collection.find()
        return [MongoTodoItem.from_mongo_data(todo) for todo in mongo_todos]

    @staticmethod
    def get_by_id(todo_id):
        todo_data = collection.find_one({"_id": ObjectId(todo_id)})
        return MongoTodoItem(**todo_data) if todo_data else None

    @staticmethod
    def insert(todo):
        if isinstance(todo, MongoTodoItem):
            collection.insert_one(todo.__dict__)
        else:
            from rest.schema.todo import TodoItem as DjangoTodoItem
            if isinstance(todo, DjangoTodoItem):
                todo = MongoTodoItem.from_django_model(todo)
            collection.insert_one(todo.__dict__)

    @staticmethod
    def update(todo_id, updated_todo):
        if isinstance(updated_todo, MongoTodoItem):
            collection.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_todo.__dict__})
        else:
            from rest.schema.todo import TodoItem as DjangoTodoItem
            if isinstance(updated_todo, DjangoTodoItem):
                updated_todo = MongoTodoItem.from_django_model(updated_todo)
            collection.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_todo.__dict__})

    @staticmethod
    def delete(todo_id):
        collection.delete_one({"_id": ObjectId(todo_id)})
