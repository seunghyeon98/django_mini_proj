from django.urls import path,include
from .views import helloAPI, TodoAPI,TodosAPI
from .views import helloAPI, bookAPI, booksAPI, BooksAPIMixins,BookAPIMixins


from .views import Train,Predict
# from django.conf.urls import url

# 애플리케이션 안에서의 url들을 추가해주자!
urlpatterns =[
  path('hello/',helloAPI),
  path('fbv/todos/',TodosAPI),
  path('fbv/todo/<int:bid>/',TodoAPI),
  path("fbv/books/", booksAPI),
  path("fbv/book/<int:bid>/", bookAPI),

  path('mixin/books/',BooksAPIMixins.as_view()),
  path('mixin/book/<int:bid>/',BookAPIMixins.as_view()),

  path('train/',Train.as_view(),name='train'),
  path('predict/',Predict.as_view(),name='predict'),


]

