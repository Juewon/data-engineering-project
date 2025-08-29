# urls.py
# 이 두줄은 외우자
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # main/
    path('', views.index, name='index'),
    path('login/', views.login, name='login')
]
######