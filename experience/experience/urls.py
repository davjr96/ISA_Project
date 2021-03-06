"""experience URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from experience_app import views

urlpatterns = [
    url(r'^api/v1/home$', views.home, name='homepage'),
    url(r'^api/v1/books/(?P<book_id>\d+)$', views.book_detail, name='book_detail'),
    url(r'^api/v1/login', views.login, name='login'),
    url(r'^api/v1/check_authenticator', views.check_authenticator, name='check_authenticator'),
    url(r'^api/v1/logout', views.logout, name='logout'),
    url(r'^api/v1/books/create', views.create_listing, name='create_listing'),
    url(r'^api/v1/create_user', views.create_user, name='create_user'),
    url(r'^api/v1/search', views.search, name='search'),
    url(r'^api/v1/recommend/(?P<book_id>\d+)$', views.get_recommendations, name='get_recommendations'),
]
