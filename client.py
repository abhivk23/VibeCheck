#########################################################################
# Provide username on startup. API keys should be configured locally.
# $ python3 client.py username
#########################################################################
import os, sys, requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from recommendation import Recommender
from speech_to_text import transcribe_model_selection
from sentiment import analyze_sentiment

""" SPOTIFY_CLIENT_ID="56c1ae8e401640d6b90b8066c3821f95"
SPOTIFY_CLIENT_SECRET="665045e7a1a44db7ae68b220bf1f12a3" # !!! hide key
SPOTIPY_REDIRECT_URI="https://abhivk23.github.io" """

# grab username
if len(sys.argv)>1:
    username = sys.argv[1]
else:
    username = os.environ["username"]

# Generate Spotify auth_token
REQUESTED_SCOPES="user-library-read, user-follow-read, playlist-modify-public, playlist-modify-private"
try:
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=os.environ['SPOTIFY_CLIENT_ID'], client_secret=os.environ['SPOTIFY_CLIENT_SECRET'], redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'])
except:
    os.remove(f".cache-{username}")
    token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=os.environ['SPOTIFY_CLIENT_ID'], client_secret=os.environ['SPOTIFY_CLIENT_SECRET'], redirect_uri=os.environ['SPOTIFY_REDIRECT_URI'])

# Initialize Spotify user and client modules
sp_user = spotipy.Spotify(auth=token)
sp_client = spotipy.client.Spotify(auth=token)

# Request audio 
""" url = 'https://api.nexmo.com/v1/files/a711dfc0-53d3-497f-9687-c742a4931531?api_key=42b5fe7d&api_secret='+os.environ["NEXMO_SECRET"]
r = requests.get(url, allow_redirects=True)
open('demo_audio/d179e484-c31e-400e-88ed-60508a4a8864.mp3', 'wb').write(r.content)

## The following are all equivalent test cases ##
ext_vibes = transcribe_model_selection('demo_audio/d179e484-c31e-400e-88ed-60508a4a8864.mp3', "phone_call") 
ext_vibes = [ -0.800000011920929, 2.4000000953674316] 
"""
ext_vibes = analyze_sentiment("I'm kinda nervous about this demonstration I'm doing right now. We spent the past weekend working on this and I hope I don't mess it up.")

## Map [strength, magnitude] --> [valence, energy] assuming unif. dist.
# strength: [-1.0, 1.0] ; magnitude: [0.0 , ~13] (technically LUB=#inf, but approx. for relevant input)
# valence: [0.0, 1.0] ; energy: [0.0 , 1.0]
ext_vibes[0] = (1.0+ext_vibes[0])/2.0
ext_vibes[1] = (ext_vibes[1])/4.0

## Display results ##
print("The external_vibes [{stre:.4f}, {mag:.4f}] correspond to [insert emotions here]".format(stre=ext_vibes[0], mag=ext_vibes[1]))

print("Building your playlist...")
Rec = Recommender(sp_user, sp_client, ext_vibes)
uri = Rec.generate_track_rec()
track_id = uri.split(":")[2] 
artists = [artist['name'] for artist in sp_client.track(track_id)['artists']]
print("Your VibeCheck recommendation is: " + sp_client.track(track_id)['name'] + " by " + artists[0]) # expand to get all artists

# Generate a shareable playlist of some other similarly feeling songs
playlist_url = Rec.generate_playlist(username, "vibecheck4", 10, "Happy")
print("Check this playlist out to continue to ride the vibe: " + playlist_url)