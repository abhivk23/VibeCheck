## PYTHON3
import os, sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

## Configure authentication 
SPOTIFY_CLIENT_ID="56c1ae8e401640d6b90b8066c3821f95"
SPOTIFY_CLIENT_SECRET="665045e7a1a44db7ae68b220bf1f12a3"
SPOTIPY_REDIRECT_URI="https://abhivk23.github.io"
REQUESTED_SCOPES="user-library-read, user-follow-read"

if len(sys.argv)>1:
    username = sys.argv[1]
else:
    username = "npby7v4xwgsty64kobmk9xb3w"

try:
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

except:
    os.remove(f".cache-{username}")
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

## Take textual sentiment input and generate song recommendation
#text_sentiment = input("TEXT INPUT: ")
#print(text_sentiment)

sp_user = spotipy.Spotify(auth=token)
sp_client = spotipy.client.Spotify(auth=token)

from recommendation import Recommender
current_state = [0,0]
Rec = Recommender(sp_user, sp_client, current_state)
uri = Rec.generate_track_rec()
track_id = uri.split(":")[2] # TRACK ID
#print(sp_client.track(track_id))
artists = [artist['name'] for artist in sp_client.track(track_id)['artists']]
print("The current vibe is: " + sp_client.track(track_id)['name'] + " by " + artists[0]) # expand to get all artists

""" 
## Client API calls
print(sp_client.track(track_id)['name']) # TRACK NAME
print(sp_client.audio_features([track_id])) # FEATURES 
"""
""" ## User API calls
followed = sp_user.current_user_followed_artists(limit=20, after=None)['artists']['items'] ## FOLLOWED_ARTISTS (list)
for artist in followed:
    res = sp_client.artist_top_tracks(artist['uri'])

    for track in res['tracks'][:10]:
        print(track['uri']) """
""" 
for song in Rec.user_lib:
    uri = song['track']['uri']
    track_id = uri.split(":")[2]
    print(sp_client.audio_analysis(track_id)) 
"""