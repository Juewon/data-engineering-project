from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # main/
    path('signup_signin/', views.signup_signin, name='signup_signin'),
    path('signout/', views.signout, name='signout'),
]