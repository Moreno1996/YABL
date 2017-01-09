from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Book, Reader, Grading
import json


class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ('vsbh', 'roman', 'pos', 'real', 'span','grade','count')
        #fields = ('grade','count')

class ReaderGradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ('vsbh', 'roman', 'pos', 'real', 'span')
        #fields = ('grade','count')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class BookSerializer(serializers.ModelSerializer):
    grading = ReaderGradingSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ('id','title', 'author', 'description', 'rating', 'image_link','isbn','year', 'grading')

class BookListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title +" by "+ value.author


class ReaderSerializer(serializers.ModelSerializer):
    grading = GradingSerializer(read_only=True)
    read_books = BookListingField(many=True,read_only=True)
    tbr_books = BookListingField(many=True,read_only=True)
    graded_books = BookListingField(many=True,read_only=True)

    class Meta:
        model = Reader
        fields = ('user', 'read_books', 'tbr_books', 'graded_books', 'date_joined','grading')
