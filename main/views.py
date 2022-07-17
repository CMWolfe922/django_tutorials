from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .models import Article, ArticleSeries
# Create your views here.

# 3) Now django comes to the views file to find the homepage view and render
# whatever is defined inside the view
def homepage(request):
    # Since the home.html references objects, I need to make sure that the context is equal to objects
    matching_series = ArticleSeries.objects.all()
    return render(request, 'main/home.html', context={'objects': matching_series})


def series(request, series: str):
    matching_series = Article.objects.filter(series__slug=series).all()

    return render(
        request=request,
        template_name='main/home.html',
        context={'objects': matching_series}
        )

# First I need to go to the models.py file where I created the slug method
# with a @property decorator and join series_slug with article_slug

def article(request, series: str, article: str):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    return render(
        request=request,
        template_name='main/article.html',
        context={'object': matching_article}
        )

