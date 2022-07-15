from django.shortcuts import render
from django.http import HttpResponse

from .models import Article, ArticleSeries
# Create your views here.

# 3) Now django comes to the views file to find the homepage view and render
# whatever is defined inside the view
def homepage(request):
    # Since the home.html references objects, I need to make sure that the context is equal to objects
    matching_series = ArticleSeries.objects.all()
    return render(request, 'main/home.html', context={'objects': matching_series})


def series(request, series: str):
    series_articles = Article.objects.filter(series__series_slug=series).all()
    return render(request, 'main/home.html', context={'objects': series_articles})
