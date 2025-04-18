from django import template
from app_kinopoisk.models import Category, Movie
#темплейттег для экономии времени и возвращения категорий в хедере не копируя метод в каждое представление
register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    movies = Movie.objects.order_by("id")[:count]#5 запсией
    return {"last_movies": movies}