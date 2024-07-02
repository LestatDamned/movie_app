from django.shortcuts import render, get_object_or_404
from .models import Movie,Director,Actor
from django.urls import reverse
from django.db.models import F, Sum, Max, Min, Avg, Count,Value
from django.views.generic import ListView, DetailView
from django.views import View


# Create your views here.
def get_movies(request):
  #movies = Movie.objects.order_by(F('year').asc(),'-rating')
  movies = Movie.objects.annotate(
    true_bool=Value(True),
    new_budget=F('budget')+1000)
  agg = movies.aggregate(Sum('budget'),Avg('year'),Max('budget'),Min('budget'),Count('id'))
  context={
    'movies':movies,
    'agg':agg
  }
  return render(request,'movie_app/all_movie.html', context=context)

def get_one_movie(request, slug_movie):
  movie = get_object_or_404(Movie, slug=slug_movie)
  context={
    'movie':movie,

  }
  return render(request, 'movie_app/one_movie.html', context=context)

def get_directors(request):
  directors=Director.objects.all()
  context={
    'directors':directors
  }
  return render(request,'movie_app/all_directors.html',context=context)

def get_one_director(request, slug_director):
  director = get_object_or_404(Director, slug=slug_director)
  context={
    'director':director
  }
  return render(request, 'movie_app/one_director.html', context=context)


# def get_one_actor(request, slug_actor):
#   actor = get_object_or_404(Actor, slug=slug_actor)
#   context={
#     'actor':actor
#   }
#   return render(request, 'movie_app/one_actor.html', context=context)

class Oneofactors(DetailView):
  template_name = 'movie_app/one_actor.html'
  model = Actor
  context_object_name = 'actor'
  slug_field = 'slug'
  slug_url_kwarg = 'slug_actor'

class Listofactors(ListView):
  template_name = 'movie_app/all_actors.html'
  model = Actor
  context_object_name = 'actors'

  def get_queryset(self):
    queryset = super().get_queryset()
    return queryset