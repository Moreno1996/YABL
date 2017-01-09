from django.test import TestCase
import rest_framework
from rest_framework import serializers
from .models import Book
from .serializers import BookSerializer


# Create your tests here.
def test():
    book = Book.objects.first()
    serializers= BookSerializer(book)

    info =json.dumps(serializers.data)
    print(info)
