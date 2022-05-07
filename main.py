from tinytag import TinyTag
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import spotipy
import re

# Input
print("Enter your username:")
username = input()
print("Enter path eg. \"D:/Music/\":")
path_input = input()
print("Enter playlist name: ")
playlist_name = input()
print("Enter description: ")
description = input()

# Data
fileList = Path(path_input).rglob('*.mp3')
data = {'music': []}
data_unable = {'music': []}
song_list = []
scope = "playlist-modify-public"
# Add these to environment variables on PC
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
count = 0
loop_count = 0
total_count = 0

# Authorization
token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope,
                     username=username)
spotify_object = spotipy.Spotify(auth_manager=token)

# Playlist creation
spotify_object.user_playlist_create(user=username, name=playlist_name, public=True, description=f"{description}. "
                                                                                                f"Check out my GitHub"
                                                                                                f" page: "
                                                                                                f"https://github.com"
                                                                                                f"/agb2k")

path, dirs, files = next(os.walk(path_input))
num_files = len(files)

# Loop through files
print("Please wait till program is complete:")
for x in fileList:
    count += 1
    total_count += 1
    file = str(x)
    tag = TinyTag.get(file)

    # Account for songs/albums with brackets in their title
    modified_title = re.sub(r"\([^()]*\)", "", f"{tag.title}")
    modified_album = re.sub(r"\([^()]*\)", "", f"{tag.album}")

    song = f"{modified_title} {tag.artist} {modified_album}"
    result = spotify_object.search(q=song)

    try:
        song_list.append(result['tracks']['items'][0]['uri'])
    except:
        try:
            file_details = os.path.basename(x).split(' - ')
            song_new = f"{modified_title} {file_details[0]}"
            result_new = spotify_object.search(q=song_new)
            song_list.append(result_new['tracks']['items'][0]['uri'])
        except:
            try:
                song_new = f"{modified_title}"
                result_new = spotify_object.search(q=song_new)
                song_list.append(result_new['tracks']['items'][0]['uri'])
                print(f"{song_new} may not be accurate search query")
            except:
                print(f"Unable to search query: {song_new}")
                data_unable['music'].append({
                    'Title': tag.title,
                    'Artist': tag.artist,
                    'Album': tag.album
                })

                with open("Error.json", 'w') as fp_new:
                    json.dump(data_unable, fp_new, indent=4)
                continue

    data['music'].append({
        'Title': tag.title,
        'Artist': tag.artist,
        'Album': tag.album
    })

    with open("Music.json", 'w') as fp:
        json.dump(data, fp, indent=4)

    if count >= 100:
        pre_playlist = spotify_object.user_playlists(user=username)
        playlist = pre_playlist['items'][0]['id']
        spotify_object.playlist_add_items(playlist_id=playlist, items=song_list)
        song_list.clear()
        count = 0
        loop_count += 1
        continue
    elif total_count >= num_files:
        pre_playlist = spotify_object.user_playlists(user=username)
        playlist = pre_playlist['items'][0]['id']
        spotify_object.playlist_add_items(playlist_id=playlist, items=song_list)
        print("Your playlist is now ready!")
        break
