# deep_app의 urls.py
from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('', views.outline, name='outline'),
]
