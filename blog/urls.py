from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.list, name='list'),
    path('author', views.author),
    path(
        '<int:year>/<int:month>/<int:day>/<str:slug>/',
        views.detail,
        name='detail'
    ),
    path('testing/', views.testing, name='testing'),

    path('tag/<str:tag_slug>/',
         views.list, name='posts_by_tag'),

]