from tinytag import TinyTag
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import spotipy

# Data
fileList = Path("D:/Music1/").rglob('*.mp3')
data = {'music': []}
song_list = []
scope = "playlist-modify-public"
username = "21ttgczqlm4tjnnxllt35zvsa"
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

# Authorization
token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope,
                     username=username)
spotify_object = spotipy.Spotify(auth_manager=token)

# Playlist creation
spotify_object.user_playlist_create(user=username, name="Local2Spotify", public=True, description="Made by Abhinav :)")

# Loop through files
for path in fileList:
    file = str(path)
    tag = TinyTag.get(file)

    song = f"{tag.title} {tag.artist} {tag.album}"

    result = spotify_object.search(q=song)
    song_list.append(result['tracks']['items'][0]['uri'])

    data['music'].append({
        'Title': tag.title,
        'Artist': tag.artist,
        'Album': tag.album
    })

    with open("C:/Users/abhin/PycharmProjects/Local2Spotify/Music.json", 'w') as fp:
        json.dump(data, fp, indent=4)

pre_playlist = spotify_object.user_playlists(user=username)
playlist = pre_playlist['items'][0]['id']
spotify_object.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=song_list)