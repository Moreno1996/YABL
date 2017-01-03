from django.conf import settings
settings.configure()
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import pprint
from models import Book
from xml.dom.minidom import parse
from datetime import date

def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


#Goodreads API
"""
devKey = "ZPR5rF0ZTrQBDyOg5I4tZw"
devSecret = "Zl7PXOWtwOj7XYS0N47HtwVY0pOFBqwpT2l4hFY7g"
api = 'https://www.goodreads.com/author/list/'
authorID ="1077326"
 # Replace with your own key
print(api+authorID+"?format=xml&key="+devKey)
string = api+authorID+"?format=xml&key="+devKey;
print(string)
u = urllib.request.urlopen(string)
data = u.read().decode('utf8')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)
"""

#bol.com API



def search():

    devKey = "4ED7064993AB46EE9B4BDE70BA4DBF00"
    devSecret = "BE09BFB17B5371CE8AECB46FBFEE5C19E60722A3D0A8DB8FE50F93830A8F3FD234E1A1455A58B8F48978686C665DE189546EEB4BF74EAA0280D0C46E21D881B906083333904244861992E7C6E88ED8BC541B61F4A4BA7463AEB1826CDAAE5006BC9C4DC3DECB6B67BBD109CD8C69E2FDA443F8E7A5FC1603603B918AFF85023A"
    limit = 1

    ID = 10756
    Format = "json"
    api = "https://api.bol.com/catalog/v4/search/?"
    request = {
        'q' : 'harry',
        'limit' : '3',
        'offset' : '0',
        'apikey': devKey ,
        'format':"json",
        'dataoutput':'products,categories'
        } # Replace with your own key
    urlquery = urllib.parse.urlencode(request) # nicer way to build urls
    print (api+urlquery)
    api2="https://api.bol.com/catalog/v4/search/?q=harry&offset=0&limit=2&dataoutput=products,categories&apikey="+devKey+"&format=json"
    print(api2)

def list():
    devKey = "4ED7064993AB46EE9B4BDE70BA4DBF00"
    devSecret = "BE09BFB17B5371CE8AECB46FBFEE5C19E60722A3D0A8DB8FE50F93830A8F3FD234E1A1455A58B8F48978686C665DE189546EEB4BF74EAA0280D0C46E21D881B906083333904244861992E7C6E88ED8BC541B61F4A4BA7463AEB1826CDAAE5006BC9C4DC3DECB6B67BBD109CD8C69E2FDA443F8E7A5FC1603603B918AFF85023A"
    limit = 3
    categories = {
        'Fantasy':'25369',
    #    'Romantiek': '25371',
    #    'Sciencefiction': '25372',
    #    'Spanning': '25374'
    }
    lang = "8293"
    Format = "json"
    api = "https://api.bol.com/catalog/v4/lists/"
    for cat in categories:
        print(categories[cat])
        request = {
            'ids' : categories[cat]+','+lang,
            'limit' : str(limit),
            'apikey': devKey ,
           'format':Format,
            'dataoutput':'products',
            'sort':'datedesc'
            } # Replace with your own key
        urlquery = urllib.parse.urlencode(request) # nicer way to build urls
        #print (api+'?'+urlquery)
        u = urllib.request.urlopen(api+'?'+urlquery)
        data = u.read().decode('utf8') # decode: turns bytes into strings
        print(pp_json(data))

        try: js = json.loads(str(data))
        except: js = None
        for x in range(0, limit):
    #author ,title ,decription,image_link,title,date_added,year,isbn
            title = js["products"][x]["title"]
            author = js["products"][x]["specsTag"]



def newBook(au ,ti ,de,im,date,ye,isb ):
    Book.objects.create(author =au,title =ti ,decription=de,image_link=im,date_added=date.today() ,year=ye,isbn=isb    )

list()
