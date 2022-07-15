from django.urls import path
from . import views


urlpatterns = [
     # 2) Django then looks here and sees to look for views.homepage view
    path('', views.register, name='register'),

]
