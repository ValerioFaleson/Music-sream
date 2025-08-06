from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('play/<str:filename>/', views.play_audio, name='play_audio'),# ← La vue d’accueil
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('base/', views.base_view, name='base'),
    path('playlists/', views.playlists_view, name='playlists'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/delete/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/edit/', views.edit_playlist, name='edit_playlist'),
    path('playlist/<int:playlist_id>/add/', views.add_to_playlist, name='add_to_playlist'),
]
