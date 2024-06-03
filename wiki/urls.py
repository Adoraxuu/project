from django.urls import path
from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.wiki_index),
    path('testing/', views.testing, name='testing'),
]