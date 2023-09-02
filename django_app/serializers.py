from rest_framework import serializers
from .models import Todo

from .models import Book
class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = ['bid', 'title', 'author', 'category', 'pages', 'price', 'published_date',
    'description',]


class TodoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Todo
    fields = ['id','userid','title','done','regdate','moddate']

