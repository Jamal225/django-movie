from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from django.views.generic.base import View

from .models import Movie, Genre, Actor


# Create your views here.

class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, View):
    """"Список фильмов"""

    def get(self, request):
        movies = Movie.objects.all()
        return render(request, "movies/movie_list.html",
                      {"movie_list": movies})



class MovieDetailView(GenreYear, View):
    """Полное описание фильма"""

    def get(self, request, slug):
        movie = Movie.objects.get(url=slug)
        actors = [actor.name for actor in movie.actors.all()]
        actors_repr = ", ".join(actors)
        return render(request, "movies/movie_detail.html",
                      {"movie": movie, "actors_repr": actors_repr})


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset


class ActorView(DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"