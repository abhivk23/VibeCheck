#########################################################################
# Provide authentication keys in main call:
# $ python3 client.py SPOTIFY_USERNAME SPOTIFY_CLIENT_SECRET NEXMO_SECRET
#########################################################################
import os, sys, requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#from speech_to_text import transcribe_model_selection

## Configure authentication
SPOTIFY_CLIENT_ID="56c1ae8e401640d6b90b8066c3821f95"
SPOTIFY_CLIENT_SECRET="665045e7a1a44db7ae68b220bf1f12a3" # !!! hide key
SPOTIPY_REDIRECT_URI="https://abhivk23.github.io"
REQUESTED_SCOPES="user-library-read, user-follow-read"

if len(sys.argv)>1:
    username = sys.argv[1]
else:
    username = "npby7v4xwgsty64kobmk9xb3w"

# Generate Spotify auth_token
try:
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

except:
    os.remove(f".cache-{username}")
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

# Initialize Spotify user and client modules
sp_user = spotipy.Spotify(auth=token)
sp_client = spotipy.client.Spotify(auth=token)

""" # Fetch phone transcription
url = 'https://api.nexmo.com/v1/files/c598ae96-2f87-44ef-a412-f28544737585?api_key=657a6239&api_secret=ENKun12C4T8dsMfn' # !!! hide key
r = requests.get(url, allow_redirects=True)
open('404c2974-3c3e-45db-b3f8-2398956ff494.mp3', 'wb').write(r.content)

# Analyze sentiment of call transcrtip and save as ext_vibes
## ext_vibes = [strength, magnitude]
ext_vibes = transcribe_model_selection('404c2974-3c3e-45db-b3f8-2398956ff494.mp3', "phone_call") """
ext_vibes = [-0.44, 2.79] 
print("The external_vibes: " + ext_vibes + "which means we're feeling ~negative vibes, with ~low energy (sad)")

## Map [strength, magnitude] --> [valence, energy] assuming unif. dist.
## strength: [-1.0, 1.0] ; magnitude: [0.0 , ~13] (technically LUB=#inf, but approx. for relevant input)
## valence: [0.0, 1.0] ; energy: [0.0 , 1.0]
ext_vibes[0] = (1.0+ext_vibes[0])/2.0
ext_vibes[1] = (ext_vibes[1])/13.0

from recommendation import Recommender
Rec = Recommender(sp_user, sp_client, ext_vibes)
uri = Rec.generate_track_rec()
track_id = uri.split(":")[2] # TRACK ID
artists = [artist['name'] for artist in sp_client.track(track_id)['artists']]

print("The current vibe is: " + sp_client.track(track_id)['name'] + " by " + artists[0]) # expand to get all artists

"""
## Example Client API calls
print(sp_client.track(track_id)['name']) # TRACK NAME
print(sp_client.audio_features([track_id])) # FEATURES

## Example User API calls
followed = sp_user.current_user_followed_artists(limit=20, after=None)['artists']['items'] ## FOLLOWED_ARTISTS (list)
for artist in followed:
    res = sp_client.artist_top_tracks(artist['uri'])

    for track in res['tracks'][:10]:
        print(track['uri'])
"""
"""
for song in Rec.user_lib:
    uri = song['track']['uri']
    track_id = uri.split(":")[2]
    print(sp_client.audio_analysis(track_id))
"""
