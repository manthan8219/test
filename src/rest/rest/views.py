from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest.models import model

class TodoListView(APIView):

    def get(self, request):
        todos = model.MongoTodoItem.get_all()
        converted_todos = [model.MongoTodoItem.to_django_model(todo) for todo in todos]
        serialized_todos = [todo.to_dict() for todo in converted_todos]
        return Response(serialized_todos, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        todo = model.MongoTodoItem(title=title)
        model.MongoTodoItem.insert(todo)
        
        return Response({'message': 'Todo item created successfully'}, status=status.HTTP_201_CREATED)
