## PYTHON3
import os, sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import recommendation as rec

## Configure authentication 
SPOTIFY_CLIENT_ID="56c1ae8e401640d6b90b8066c3821f95"
SPOTIFY_CLIENT_SECRET=""
SPOTIPY_REDIRECT_URI="https://abhivk23.github.io"
REQUESTED_SCOPES="user-library-read"

if len(sys.argv)>1:
    username = sys.argv[1]
else:
    username = "npby7v4xwgsty64kobmk9xb3w"

try:
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

except:
    os.remove(f".cache-{username}")
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)
sp_client = spotipy.client.Spotify(auth=token)

## Take textual sentiment input and generate song recommendation
#text_sentiment = input("TEXT INPUT: ")
#print(text_sentiment)
Rec = rec.Recommendation(sp)
uri = Rec.user_lib[0]['track']['uri']
track_id = uri.split(":")[2]
print(sp_client.track(track_id)['name'], "\n", sp_client.audio_features([track_id]))


""" for song in Rec.user_lib:
    uri = song['track']['uri']
    track_id = uri.split(":")[2]
    print(sp_client.audio_analysis(track_id)) """