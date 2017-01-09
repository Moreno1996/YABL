from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
import datetime
from django.contrib.auth.models import User




# Create your models here.
class Grading(models.Model):
    vsbh    =   models.FloatField(default=0)
    roman   =   models.IntegerField(default=0)
    pos     =   models.IntegerField(default=0)
    real    =   models.IntegerField(default=0)
    span    =   models.IntegerField(default=0)
    grade   =   models.IntegerField(default=0)
    count   =   models.IntegerField(default=0)
    def __str__(self):
        return str(self.vsbh)  + " - "+ str(self.roman)  + " - "+str(self.pos)  + " - "+str(self.real)  + " - "+str(self.span)
class Book(models.Model):
    bookID=models.IntegerField(default=0)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_link = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    year = models.CharField(default="", max_length=200)
    isbn = models.IntegerField(default = 0)
    rating = models.IntegerField(default=0)
    grading = models.OneToOneField(Grading, related_name='book_grading', null=True,on_delete=models.CASCADE)

    def new():
        return True
    def __str__(self):
        return self.title + " - " + self.author

class Reader(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE   )
    read_books      = models.ManyToManyField(Book,related_name="read+")
    tbr_books       =  models.ManyToManyField(Book,related_name="tbr+")
    graded_books     = models.ManyToManyField(Book,related_name="graded+")
    date_joined     = models.DateTimeField(default=timezone.now)
    grading = models.ForeignKey(Grading, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class BookRating(models.Model):
    date        = models.DateTimeField(default=timezone.now)
    rater       = models.ForeignKey(Reader, on_delete=models.CASCADE)
    rating      = models.IntegerField(default=0)
    comments    = models.TextField()
    book        = models.ForeignKey(Book, on_delete=models.CASCADE)
    def __str__(self):
        return self.book.title + " - " + self.rater.user.username + ": " + str(self.rating)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Reader.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
