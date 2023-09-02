from django.db import models

# Create your models here.
class Todo(models.Model):
  id = models.AutoField(primary_key=True)
  userid=models.CharField(max_length=100)
  title=models.CharField(max_length=100)
  done= models.BooleanField()
  regdate = models.DateTimeField(auto_now_add=True)
  moddate = models.DateTimeField()

class Book(models.Model):
  bid = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=50)
  author = models.CharField(max_length=50)
  category = models.CharField(max_length=50)
  pages = models.IntegerField()
  price = models.IntegerField()
  published_date = models.DateField()
  description = models.TextField()