from django.db import models
from django.utils import timezone
import datetime



# Create your models here.
class Book(models.Model):
    #author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    decription = models.TextField()
    image_link = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    year = models.DateTimeField(default=timezone.now, blank = True, null = True)
    isbn = models.IntegerField(default = 0)
    def new():
        return True
    def __str__(self):
        return self.title + " - " + self.author
"""class Author(models.Model):
    name = models.TextField()
    genre = models.TextField()"""
