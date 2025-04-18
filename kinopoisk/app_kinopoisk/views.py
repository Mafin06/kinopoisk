from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from django.views import View
from django.utils.text import slugify
from django.db.models import Q
from .models import Category, Movie, MovieShots, Actor, RatingStar, Rating, Reviews, Genre
from .forms import ReviewForm, RatingForm

# Create your views here.

class GenreYear:
    """года и жанры - фильтрация фильмов по ним"""
    def get_genres(self):
        return Genre.objects.all()
    
    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").distinct()
  

class MovieView(GenreYear, ListView):
    '''список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"

    '''def get(self, request): ---------обычное View
        movies = Movie.objects.all()
        return render(request, "movies/movies.html", {"movie_list": movies})'''
    # def get_context_data(self, *args, **kwargs):#отображение категорий фильмов в headers
    #      context = super().get_context_data(*args,**kwargs)
    #      context["categories"] = Category.objects.all()
    #      return context
    
class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"
    template_name = "movies/movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        
        # Получаем текущий рейтинг
        ip = self.get_client_ip()
        try:
            rating = Rating.objects.get(
                movie=self.object,
                ip=ip
            )
            context['user_rating'] = rating.star.value
        except Rating.DoesNotExist:
            context['user_rating'] = None
            
        return context
    
    def get_client_ip(self):
        request = self.request
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    '''def get(self, request, slug): ---------обычное View
        movie = Movie.objects.get(url=slug)
        return render(request, "movies/moviesingle.html", {"movie": movie})'''

class AddReview(View):
    '''добавление отзыва к фильму'''
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie =  Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
    
class ActorView(GenreYear, View):
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"

    def get(self, request, slug):
        # Получаем актера по slug
        actor = Actor.objects.get(name=slug)
        context = {
            'actor': actor,
        }
        return render(request, self.template_name, context)
    
class FilterMovieView(GenreYear,ListView):
    template_name = 'movies/movie_list.html'
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in = self.request.GET.getlist("year")) | 
            Q(genres__in = self.request.GET.getlist("genre")))
        return queryset
    
class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            try:
                ip = self.get_client_ip(request)
                rating, created = Rating.objects.update_or_create(
                    ip=ip,
                    movie_id=int(request.POST.get("movie")),
                    defaults={'star_id': int(request.POST.get("star"))}
                )
                return JsonResponse({
                    'status': 'success',
                    'rating': rating.star.value
                }, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({'error': 'Invalid data'}, status=400)