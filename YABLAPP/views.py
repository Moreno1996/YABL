from django.shortcuts import render,get_object_or_404
from YABLAPP.models import Book, Reader, BookRating, Grading
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, BookSerializer,ReaderSerializer
from django.contrib.auth.models import User, Group
import urllib.request
from itertools import chain
import urllib.parse
import json
from django.db.models import Q
import xml.etree.ElementTree as ET
import pprint
from django.utils import timezone
from xml.dom.minidom import parse
from datetime import date
from .forms import searchBookForm, UserForm, GradingForm
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from itertools import groupby

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

""""

Web views defined.

"""
def search_new(request):
    print('request: '+ str(request))
    print('path'+request.path_info)
    print('pathinfo: '+request.path_info)
    if request.method == "GET":
            print('get')
            try:query = request.GET['q']
            except: query=False
            if not query == False:

                result = search(query)
                print(result)
                print('done')
                return render(request, 'bookOverview.html',{"Books":result, 'Title': 'Found Books:'})

    else:
        print('not get')
    form = searchBookForm()
    print('new')
    return render(request, 'search_new_page.html', {'form': form})

def add_book(request,pk,x):
    user = request.user
    book = get_object_or_404(Book,pk=pk)

    lis = ""
    if user.is_authenticated():
        message = "Welcome " + user.username
    else:
        lis = "None! You are not logged in!"
        return render(request, 'singleBook.html', { 'book':book, 'alert':lis})
    x = int(x)
    print(x)
    reader = Reader.objects.filter(user=user)
    print (reader)
    reader = reader.first()
    if x == 0:
        reader.tbr_books.add(book)
        lis="Added Book to Favourites"
    elif x==1:
        reader.read_books.add(book)
        lis="Added Book to Read books"
    elif x==2:
        reader.graded_books.add(book)
        lis="Added book to Graded Books"
    else:
        return render(request, 'singleBook.html', {'book': book,'alert':'Error'})

    return render(request, 'singleBook.html', {'book': book,'success':lis})


def grade_single(request,pk):
        user = request.user
        if user.is_authenticated():
            reader = Reader.objects.filter(user=user).first()
            book = get_object_or_404(Book,pk=pk)
            if request.method == "POST":
                grade = book.grading
                vsbh = int(request.POST['vsbh'])/10
                rating = int(request.POST['rating'])/10
                roman = int(request.POST['roman'])/10
                pos = int(request.POST['pos'])/10
                real = int(request.POST['real'])/10
                span = int(request.POST['span'])/10
                if not grade:
                    grade = Grading.objects.create(vsbh=vsbh, roman=roman,pos=pos,real=real,span=span,grade=rating, count=1)
                    book.grading = grade
                    book.save()

                else:
                    count = grade.count
                    grade.vsbh = (vsbh + count * grade.vsbh)/(count+1)
                    grade.grade = (rating + count * grade.grade)/(count+1)
                    grade.roman = (roman + count * grade.roman)/(count+1)
                    grade.real = (real + count * grade.real)/(count+1)
                    grade.pos = (pos + count * grade.pos)/(count+1)
                    grade.span = (span + count * grade.span)/(count+1)
                    grade.count = count + 1
                    grade.save()
                    book.grading = grade
                    book.save()
                print(grade)
                print(book.grading)
                reader.graded_books.add(book)
                reader_grading = reader.grading
                if not reader_grading:
                    reader_grading = Grading.objects.create()
                    reader.grading = reader_grading
                    reader.save()
                count = reader_grading.count
                if rating>8:
                    if count > 0:
                        reader_grading.vsbh = (vsbh +count*reader_grading.vsbh   )/(count+1)
                        reader_grading.grade = (rating +count*reader_grading.grade)/(count+1)
                        reader_grading.roman = (roman +count*reader_grading.roman)/(count+1)
                        reader_grading.pos = (pos +count*reader_grading.pos)/(count+1)
                        reader_grading.real = (real +count*reader_grading.real)/(count+1)
                        reader_grading.span = (span +count*reader_grading.span)/(count+1)
                        reader_grading.count = reader_grading.count + 1
                    else:
                        reader_grading.vsbh = vsbh
                        reader_grading.grade = rating
                        reader_grading.roman = roman
                        reader_grading.pos = pos
                        reader_grading.real = real
                        reader_grading.span = span
                        reader_grading.count = reader_grading.count + 1
                elif rating>6:
                        if count > 0:
                            reader_grading.vsbh = (vsbh*0.5 +count*reader_grading.vsbh   )/(count+0.5)
                            reader_grading.grade = (rating*0.5  +count*reader_grading.grade)/(count+0.5)
                            reader_grading.roman = (roman*0.5  +count*reader_grading.roman)/(count+0.5)
                            reader_grading.pos = (pos*0.5  +count*reader_grading.pos)/(count+0.5)
                            reader_grading.real = (real*0.5  +count*reader_grading.real)/(count+0.5)
                            reader_grading.span = (span*0.5  +count*reader_grading.span)/(count+0.5)
                            reader_grading.count = reader_grading.count + 1
                        else:
                            reader_grading.vsbh = vsbh
                            reader_grading.grade = rating
                            reader_grading.roman = roman
                            reader_grading.pos = pos
                            reader_grading.real = real
                            reader_grading.span = span
                            reader_grading.count = reader_grading.count + 1
                reader_grading.save()
                reader.grading = reader_grading
                reader.save()
                print(reader_grading)
                print(reader.grading)
                return render(request, 'singleBook.html', { 'book':book, 'success':'Graded'})
            else:
                return render(request, 'grade.html', {'id':pk, 'book':book})
        else:
                return render(request, 'singleBook.html', {'book':book, 'alert':"Not logged in"})






def singleBook(request,pk):
    book = get_object_or_404(Book,pk=pk)
    recom = findRecommendations(book.bookID)
    return render(request, 'singleBook.html',{'book':book,'recom':recom})

def bookOverview(request):
    Books = Book.objects.filter()
    Books = Books.order_by('-rating')
    return render(request, 'bookOverview.html',{'Books':Books, 'Title': 'All Books:'})

def read_view(request):
    user = request.user
    reader = Reader.objects.filter(user=user).first()
    Books = reader.read_books
    Books = Books.order_by('-rating')
    return render(request, 'bookOverview.html',{'Books':Books, 'Title': 'Read Books:'})

def favourite_view(request):
    user = request.user
    reader = Reader.objects.filter(user=user).first()
    Books = reader.tbr_books
    Books = Books.order_by('-rating')
    return render(request, 'bookOverview.html',{'Books':Books, 'Title': 'To-Be-Read Books:'})
def rated_view(request):
    user = request.user
    reader = Reader.objects.filter(user=user).first()
    Books = reader.graded_books
    Books = Books.order_by('-rating')
    return render(request, 'bookOverview.html',{'Books':Books, 'Title': 'Graded Books:'})

def reader(request):
    user = request.user
    reader = Reader.objects.filter(user=user).first()
    merged = chain(reader.graded_books, reader.tbr_books, reader.read_books)
    print(reader)


    Books = reader.graded_books.all() | reader.tbr_books.all() |reader.read_books.all()
    Books = Books.order_by('-rating')
    return render(request, 'bookOverview.html',{'Books':Books, 'Title': 'All Books:'})


def index(request):
    message = ""
    user = request.user
    if user.is_authenticated():
        message = user.username
    else:
        message = ""
    books = Book.objects.all()
    books = books.order_by("-date_added")[:8]
    best = Book.objects.all().exclude(grading__isnull=True).order_by("-rating")[:8]


    return render(request, 'index.html',{'message':  message,'Books':books, 'best':best, 'user':user})



"""

Some other stuff


"""

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



"""


 This is the api Part of getting the information


 """
def findRecommendations(ID):
    print("Start recommendations Search")
    results = []
    devKey = "4ED7064993AB46EE9B4BDE70BA4DBF00"
    devSecret = "BE09BFB17B5371CE8AECB46FBFEE5C19E60722A3D0A8DB8FE50F93830A8F3FD234E1A1455A58B8F48978686C665DE189546EEB4BF74EAA0280D0C46E21D881B906083333904244861992E7C6E88ED8BC541B61F4A4BA7463AEB1826CDAAE5006BC9C4DC3DECB6B67BBD109CD8C69E2FDA443F8E7A5FC1603603B918AFF85023A"
    limit = 4
    Format = "json"
    api = "https://api.bol.com/catalog/v4/recommendations/"
    request = {

        'apikey': devKey ,
        'format':"json",
        'limit':limit,
        } # Replace with your own key
    urlquery = urllib.parse.urlencode(request) # nicer way to build urls
    #print (api+'?'+urlquery)
    url = api +str(ID)+"/?"+ urlquery
    u = urllib.request.urlopen(url)
    data = u.read().decode('utf-8') # decode: turns bytes into strings
    #print(pp_json(data))
    try: js = json.loads(str(data))
    except: js = None
    for x in range(0, limit):
        #author ,title ,description,image_link,title,date_added,year,isbn
        try:    ID = str(js["products"][x]["id"])
        except: ID = -100
        if ID!=-100:
            book = Book.objects.filter(bookID=ID)
            if not book:
                new_book = findSpecific(ID)
                if new_book != False:
                    results.append(new_book)
            else:
                results.append(book.first())

    print("Finished recommendations Search")
    return results

def search(term):
    results = []
    devKey = "4ED7064993AB46EE9B4BDE70BA4DBF00"
    devSecret = "BE09BFB17B5371CE8AECB46FBFEE5C19E60722A3D0A8DB8FE50F93830A8F3FD234E1A1455A58B8F48978686C665DE189546EEB4BF74EAA0280D0C46E21D881B906083333904244861992E7C6E88ED8BC541B61F4A4BA7463AEB1826CDAAE5006BC9C4DC3DECB6B67BBD109CD8C69E2FDA443F8E7A5FC1603603B918AFF85023A"
    limit = 12
    ids = "8299,11209"
    Format = "json"
    api = "https://api.bol.com/catalog/v4/search/?"
    request = {
        'q' : term,
        'limit': limit,
        'ids': ids,
        'offset' : '0',
        'apikey': devKey ,
        'format':"json",
        'dataoutput':'products'
        } # Replace with your own key
    urlquery = urllib.parse.urlencode(request) # nicer way to build urls
    #print (api+'?'+urlquery)
    url = api + urlquery
    u = urllib.request.urlopen(url)
    data = u.read().decode('utf-8') # decode: turns bytes into strings
    #print(pp_json(data))

    try: js = json.loads(str(data))
    except: js = None
    try: count = js["totalResultSize"]
    except:count = 0
    print(url)
    if count == 0:
        return "NO RESULTS"
    if count<limit:
        limit = count
    for x in range(0, limit):
        #author ,title ,description,image_link,title,date_added,year,isbn
        try:    ID = str(js["products"][x]["id"])
        except: ID = -100
        if ID!=-100:
            book = Book.objects.all().filter(bookID=ID)
            if not book:
                print("new")
                results.append(findSpecific(ID))
            else:
                print("exists")
                results.append(book.first())
        else:
            print("error")

    print(results)
    return results
def findSpecific(ID):
        devKey = "4ED7064993AB46EE9B4BDE70BA4DBF00"
        devSecret = "BE09BFB17B5371CE8AECB46FBFEE5C19E60722A3D0A8DB8FE50F93830A8F3FD234E1A1455A58B8F48978686C665DE189546EEB4BF74EAA0280D0C46E21D881B906083333904244861992E7C6E88ED8BC541B61F4A4BA7463AEB1826CDAAE5006BC9C4DC3DECB6B67BBD109CD8C69E2FDA443F8E7A5FC1603603B918AFF85023A"
        Format = "json"
        api = "https://api.bol.com/catalog/v4/products/"
        request = {
            'apikey':devKey,
            'format':'json',
            } # Replace with your own key
        urlquery = urllib.parse.urlencode(request) # nicer way to build urls
        url = api + str(ID) +'?'+urlquery
        u = urllib.request.urlopen(url)
        data = u.read().decode('utf-8') # decode: turns bytes into strings
        try: js = json.loads(str(data))
        except: js = None
        x=0
        try:title = js["products"][x]["title"]
        except: title = ""
        try:author = js["products"][x]["specsTag"]
        except: author = ""
        try:rating = int(js["products"][x]["rating"])/5
        except: rating = 0
        try:description = striphtml(js["products"][x]["shortDescription"])
        except: description = ""
        try:isbn = js["products"][0]["attributeGroups"][0]["attributes"]
        except: isbn = "Not There"
        try:imLength = len(js["products"][x]["images"])
        except: imLength = 0
        try:im = js["products"][x]["images"][imLength-1]["url"]
        except: im = ""
        length = len(isbn)
        isbn = ""
        year = ""
        for x in range(0,length):
            try:key = js["products"][0]["attributeGroups"][0]["attributes"][x]["key"]
            except: key = "Not There"
            if key == "ISBN13":
                isbn = js["products"][0]["attributeGroups"][0]["attributes"][x]["value"]
            if key == "VERSCHIJNINGSDATUM":
                year = js["products"][0]["attributeGroups"][0]["attributes"][x]["value"]

        new_book = newBook(author,title,description,im,year,isbn,rating,ID)
        if new_book== False:
            return False
        return new_book



def list():
    devKey = "4ED7064993AB46EE9B4BDE70BA4DBF00"
    devSecret = "BE09BFB17B5371CE8AECB46FBFEE5C19E60722A3D0A8DB8FE50F93830A8F3FD234E1A1455A58B8F48978686C665DE189546EEB4BF74EAA0280D0C46E21D881B906083333904244861992E7C6E88ED8BC541B61F4A4BA7463AEB1826CDAAE5006BC9C4DC3DECB6B67BBD109CD8C69E2FDA443F8E7A5FC1603603B918AFF85023A"
    limit = 1
    categories = {
        'Fantasy':'25369',
        'Fantasy & Science fiction':'2510',
        'Romantiek': '25371',
        'Sciencefiction': '25372',
        'Spanning': '25374',
        'Thrillers': '2551'
    }
    lang = "8293"
    Format = "json"
    api = "https://api.bol.com/catalog/v4/lists/"
    y = 0
    for cat in categories:
        request = {
            'ids' : categories[cat]+','+lang,
            'limit' : str(limit),
            'apikey': devKey ,
           'format':Format,
            'dataoutput':'products',
            'sort':'rankasc'
            } # Replace with your own key
        urlquery = urllib.parse.urlencode(request) # nicer way to build urls
        u = urllib.request.urlopen(api+'?'+urlquery)
        data = u.read().decode('utf-8') # decode: turns bytes into strings

        try: js = json.loads(str(data))
        except: js = None
        for x in range(0, limit):

            try:ID = js["products"][x]["id"]
            except: ID = 0
            book = Book.objects.filter(bookID=ID)
            if not book:
                findSpecific(ID)

    return js["products"][x]["images"]


"""


This is the part of other methods.


"""

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def newBook(au ,ti ,de,im,ye,isb,rating,ID ):
    if isb == "":
        return False
    book = Book.objects.filter(isbn=isb)
    if not book:
        result = Book.objects.create(author =au,title =ti ,description=de,image_link=im,year = ye, isbn=isb,rating=rating, bookID=ID    )
        print('Added')
        return result
    else:
        print('Double')
        return book.first()

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None



"""


This is the user Login, Register and Logout part


"""

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print (user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'register.html', {'user_form': user_form, 'registered': registered})

@login_required
def user_logout(request):
    logout(request)
    return render(request,'login.html', {'result': "Loged OUT!"})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return render(request,'login.html', {'result': "Loged in!", 'user': user})
            else:
                return render(request,'login.html', {'result': "Account Disabled"})
        else:
                return render(request,'login.html', {'result': "Invalid Login", })
    else:
        return render(request,'login.html', {})






























"""

API ONZIN

"""


@api_view(['GET'])
def book_collection(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def book_element(request, pk):
    try:
        book = get_object_or_404(Book,pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['GET'])
def reader_collection(request):
    if request.method == 'GET':
        readers = Reader.objects.all()
        serializer = ReaderSerializer(readers, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def reader_element(request, pk):
    try:
        reader = get_object_or_404(Reader,pk=pk)
    except Reader.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReaderSerializer(reader)
        return Response(serializer.data)
