from django.shortcuts import render
from YABLAPP.models import Book
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group

# Create your views here.
def bookOverview(request):
    Books = Book.objects.filter()
    return render(request, 'bookOverview.html',{'Books':Books})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
