from django.contrib import admin 
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace= 'blog')),
    path('blog/list/', views.blog_list, name='list'), 
    path('wiki/', include('wiki.urls', namespace= 'wiki')),
    path("__reload__/", include("django_browser_reload.urls")),
]