import random
from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'main_app/index_food.html')

def login(request):
    return render(request, 'main_app/signin.html')

