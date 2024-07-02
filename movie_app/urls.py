from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.get_movies,name='home'),
    path('movie/<slug:slug_movie>',views.get_one_movie, name='slug_movie'),
    path('directors/',views.get_directors,name='directors'),
    path('director/<slug:slug_director>',views.get_one_director,name='slug_director'),
    path('actors/',views.Listofactors.as_view(),name='actors'),
    path('actor/<slug:slug_actor>',views.Oneofactors.as_view(),name='slug_actor')
]