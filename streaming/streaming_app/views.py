from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .forms import RegisterForm
from django.contrib.auth.models import User

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from .models import Playlist, PlaylistTrack
from django.shortcuts import get_object_or_404
# Create your views here.
# def home(request):
#     return render(request, 'home.html')

import socket

def home(request):
    HOST = '127.0.0.1'
    PORT = 50007
    playlist = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(4096).decode()
            playlist = data.split('\n')
    except Exception as e:
        playlist = []
    # Ajout de user_playlists pour la sidebar
    user_playlists = Playlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'home.html', {
        'playlist': playlist,
        'user_playlists': user_playlists,
    })


from django.http import StreamingHttpResponse
@login_required(login_url='login')  # redirection vers 'login' si non connecté
def play_audio(request, filename):
    HOST = '127.0.0.1'
    PORT = 50007

    def audio_stream():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.recv(4096)  # On ignore la playlist
            s.sendall(filename.encode())
            while True:
                data = s.recv(1024)
                if not data:
                    break
                yield data

    response = StreamingHttpResponse(audio_stream(), content_type='audio/mpeg')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = user.profile.token  # le token généré automatiquement
            print("Token du nouvel utilisateur :", token)
            messages.success(request, f"Compte créé avec succès ! Ton token : {token}")
            return redirect('login')  # redirige vers la page de connexion
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def base_view(request):
    return render(request, 'base.html')

@login_required
def playlists_view(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'playlists.html', {'playlists': playlists})

@login_required
def create_playlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Playlist.objects.create(name=name, user=request.user)
    return redirect('home')

@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    playlist.delete()
    return redirect('home')

@login_required
def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            playlist.name = name
            playlist.save()
    return redirect('playlist_detail', playlist_id=playlist.id)

@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    tracks = PlaylistTrack.objects.filter(playlist=playlist)
    user_playlists = Playlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'playlist_detail.html', {
        'playlist': playlist,
        'tracks': tracks,
        'user_playlists': user_playlists,
    })
    
@login_required
def add_to_playlist(request, playlist_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        track_name = request.POST.get('track_name')
        if track_name:
            PlaylistTrack.objects.get_or_create(playlist=playlist, track_name=track_name)
    return redirect('home')