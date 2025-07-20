from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('play/<str:filename>/', views.play_audio, name='play_audio'),# ← La vue d’accueil
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout')

]
