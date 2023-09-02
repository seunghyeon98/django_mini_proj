from django.shortcuts import render

# from rest_framework.response import Response
# from rest_framework.decorators import api_view


# from rest_framework import status
# from rest_framework.generics import get_object_or_404
# from .models import Todo
# from .serializers import TodoSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Todo
from .models import Book
from .serializers import TodoSerializer
from .serializers import BookSerializer

# class형 view만들기
from rest_framework import generics,mixins

@api_view(['GET'])
def helloAPI(request):
  return Response('hello world')


# Create your views here.

# 요청(post, get)을 처리하는 함수를 작성!

@api_view(['GET','POST'])
def TodosAPI(request):
  # 요청이 get이라면, db의 데이터를 가져오는 것이라면
  if request.method == 'GET':
    # db의 모든 데이터를
    datas = Todo.objects.all()
    #직렬화 하고
    serializer = TodoSerializer(datas,many=True)
    # return함
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  # 요청이 post라면, db에 데이터를 저장하는 것이라면
  elif request.method =='POST':
    # request받은 데이터를 직렬화 시키고
    serializer = TodoSerializer(data=request.data)
    # 만약 데이터가 정상적으로 처리되었다면
    if serializer.is_valid():
      serializer.save() #저장하고
      # 반환한다
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    # 그게 아니라면 400 에러!
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  

@api_view(['GET'])
def TodoAPI(request,bid):
  data = get_object_or_404(Todo,bid=bid)
  serializer = TodoSerializer(data)
  return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def booksAPI(request):
  if request.method == 'GET':
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    serializer = BookSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def bookAPI(request, bid):
  book = get_object_or_404(Book, bid=bid)
  serializer = BookSerializer(book)
  return Response(serializer.data, status=status.HTTP_200_OK)


# 클래스형 view
class BooksAPIMixins(mixins.ListModelMixin,
  mixins.CreateModelMixin,generics.GenericAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
  
class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
  mixins.DestroyModelMixin, generics.GenericAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  lookup_field = 'bid'
  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)
  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)
  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)
  

import os
import pickle
import numpy as np
import pandas as pd
from sklearn import datasets
from django.conf import settings
  
from rest_framework import status,views

from rest_framework.response import Response
from sklearn.ensemble import RandomForestClassifier

class Train(views.APIView):
  def post(self,request):
    iris = datasets.load_iris()
    mapping = dict(zip(np.unique(iris.target),iris.target_names))

    X = pd.DataFrame(iris.data,columns=iris.features_names)
    y = pd.DataFrame(iris.target).replace(mapping)
    model_name = request.data.pop('model_name')

    try:
      clf = RandomForestClassifier(**request.data) # 요청값 넣기
      clf.fit(X,y)

    except Exception as err:
      return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
    
    path = os.path.join(settings.MPDEL_ROOT,model_name)
    with open(path,'wb') as file:
      pickle.dump(clf.file)
    return Response(status=status.HTTP_200_OK)
  
class Predict(views.APIView):
  def post(self,request):
    predictions =[]
    for entry in request.data:
      model_name = entry.pop('model_name')
      path = os.path.join(settings.MODEL_ROOT,model_name)
      with open(path,'rb') as file:
        model = pickle.load(file)
      try:
        result = model.predict(pd.DataFrame([entry]))
        predictions.append(result[0])
      except Exception as err:
        return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
      return Response(predictions,status=status.HTTP_200_OK)