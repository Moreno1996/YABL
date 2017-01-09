"""YABL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from YABLAPP import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/$', views.search_new, name='search_new_page'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout '),
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.bookOverview, name='bookOverview'),
    url(r'^books/single/(?P<pk>\d+)/$', views.singleBook, name='book_detail'),
    url(r'^books/grading/(?P<pk>\d+)/$', views.grade_single, name='grade_single'),
    url(r'^books/(?P<pk>\d+)/(?P<x>\d+)/$', views.add_book, name='add_book'),
    url(r'^reader/favourites/$', views.favourite_view, name='favourite_view'),
    url(r'^reader/rated/$', views.rated_view, name='rated_view'),
    url(r'^reader/read/$', views.read_view, name='read_view'),
    url(r'^reader/$', views.reader, name='reader'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
    url(r'^api/v1/books/$',             views.book_collection, name='book_collection'),
    url(r'^api/v1/books/(?P<pk>\d+)/$', views.book_element,     name='book_element'),
    url(r'^api/v1/reader/$',             views.reader_collection, name='reader_collection'),
    url(r'^api/v1/reader/(?P<pk>\d+)/$', views.reader_element,     name='reader_element'),

]
