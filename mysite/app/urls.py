from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('habits/', views.habits, name='app-habits'),
    path('journals/', views.journals, name='app-journals'),
]
