## PYTHON3
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID=""
SPOTIFY_CLIENT_SECRET=""
username = "npby7v4xwgsty64kobmk9xb3w"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri="https://abhivk23.github.io", username=username))
print(sp.me()["id"])
playlists = sp.user_playlists(username)
if not playlists['items']:
    print("No playlists found")
for playlist in playlists['items']:
    print(playlist['name'])