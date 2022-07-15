from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# 3) Now django comes to the views file to find the homepage view and render
# whatever is defined inside the view
def homepage(request):
    return HttpResponse("This is our homepage page, and it works")
