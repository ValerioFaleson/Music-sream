from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('play/<str:filename>/', views.play_audio, name='play_audio'),# ← La vue d’accueil
]
