from django.contrib import admin
from .models import Book, Reader, BookRating,Grading
# Register your models here.
admin.site.register(Book)
admin.site.register(Reader)
admin.site.register(BookRating)
admin.site.register(Grading)
