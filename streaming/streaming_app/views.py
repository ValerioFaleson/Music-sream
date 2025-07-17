from django.shortcuts import render
from django.http import StreamingHttpResponse
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
    return render(request, 'home.html', {'playlist': playlist})


from django.http import StreamingHttpResponse

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