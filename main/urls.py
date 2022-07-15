"""django_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


urlpatterns = [
     # 2) Django then looks here and sees to look for views.homepage view
    path('', views.homepage, name='homepage'),
    # now create a new url patter with a path to the series
    path('<series>', views.series, name='series'),
    # Add the path for rendering the articles: This means I have to create a articles view
    path('<series>/<article>', views.article, name='article'),
]
