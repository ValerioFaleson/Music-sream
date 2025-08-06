import socket
import threading
import os
import struct  # Ajouté pour envoyer la taille du fichier

AUDIO_FOLDER = r"C:\Users\Valerio\Downloads\Music"
HOST = '0.0.0.0'
PORT = 50007

def get_playlist():
    return [f for f in os.listdir(AUDIO_FOLDER) if f.endswith('.mp3')]

def stream_audio(conn, filename):
    try:
        filepath = os.path.join(AUDIO_FOLDER, filename)
        filesize = os.path.getsize(filepath)
        # Envoyer la taille du fichier sur 8 octets (unsigned long long)
        conn.sendall(struct.pack('!Q', filesize))
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                conn.sendall(data)
    except Exception as e:
        print("Erreur stream :", e)

def handle_client(conn, addr):
    print(f"Client connecté : {addr}")
    playlist = get_playlist()
    conn.sendall('\n'.join(playlist).encode())

    try:
        filename = conn.recv(1024).decode().strip()
        # Sécurité : empêcher les chemins relatifs
        filename = os.path.basename(filename)
        if filename in playlist:
            stream_audio(conn, filename)
        else:
            # Envoyer 0 comme taille pour signaler l'erreur
            conn.sendall(struct.pack('!Q', 0))
            conn.sendall(b'Fichier non trouve')
    except Exception as e:
        print(f"Erreur client {addr} :", e)
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Serveur audio prêt. En attente de clients...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()