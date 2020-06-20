from django.contrib import admin
from django.urls import path
from rss.apps.rss_news import views

urlpatterns = [
    path('', views.index),
]