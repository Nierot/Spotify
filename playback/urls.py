from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites', views.favorites, name='index'),
    path('testgraph', views.graph, name="test"),
    path('playback', views.playback, name='playback'),
    path('add', views.add_songs, name='add_songs'),
    path('auth_test', views.auth_test, name='auth_test'),
    re_path(r'^add_test/$', views.add_test, name='add_test'),
    re_path(r'^auth/$',views.auth, name='auth'),
    re_path(r'^callback/$', views.callback, name='callback'),
]