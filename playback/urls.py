from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites', views.favorites, name='index'),
    path('testgraph', views.graph, name="test"),
    re_path(r'^auth/$',views.auth, name='auth'),
    re_path(r'^callback/$', views.callback, name='callback'),
]