#########################################################################
# Remember to provide authentication keys.
# Future: $ python3 client.py SPOTIFY_USERNAME SPOTIFY_CLIENT_SECRET NEXMO_SECRET
#########################################################################
import os, sys, requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#from speech_to_text import transcribe_model_selection
#from sentiment import analyze_sentiment

## Configure authentication
SPOTIFY_CLIENT_ID="56c1ae8e401640d6b90b8066c3821f95"
SPOTIFY_CLIENT_SECRET="" # !!! hide key
SPOTIPY_REDIRECT_URI="https://abhivk23.github.io"
REQUESTED_SCOPES="user-library-read, user-follow-read, playlist-modify-public, playlist-modify-private"
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


""" url = ''
r = requests.get(url, allow_redirects=True)
open('d179e484-c31e-400e-88ed-60508a4a8864.mp3', 'wb').write(r.content)
ext_vibes = transcribe_model_selection('d179e484-c31e-400e-88ed-60508a4a8864.mp3', "phone_call") 
ext_vibes = analyze_sentiment("I'm kinda nervous about this demonstration I'm doing right now. We spent the past weekend working on this and I hope I don't mess it up.")"""
ext_vibes = [ -0.800000011920929, 2.4000000953674316]

## Map [strength, magnitude] --> [valence, energy] assuming unif. dist.
## strength: [-1.0, 1.0] ; magnitude: [0.0 , ~13] (technically LUB=#inf, but approx. for relevant input)
## valence: [0.0, 1.0] ; energy: [0.0 , 1.0]
ext_vibes[0] = (1.0+ext_vibes[0])/2.0
ext_vibes[1] = (ext_vibes[1])/4.0

print("The external_vibes [{stre:.4f}, {mag:.4f}] correspond to [insert emotions here]".format(stre=ext_vibes[0], mag=ext_vibes[1]))

print("Building your playlist...")
from recommendation import Recommender
Rec = Recommender(sp_user, sp_client, ext_vibes, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
uri = Rec.generate_track_rec()
track_id = uri.split(":")[2] # TRACK ID
artists = [artist['name'] for artist in sp_client.track(track_id)['artists']]
print("Your VibeCheck recommendation is: " + sp_client.track(track_id)['name'] + " by " + artists[0]) # expand to get all artists

# Generate a shareable playlist of some other similarly feeling songs
playlist_url = Rec.generate_playlist(username, "vibecheck4", 10, "Happy")
print("Check this playlist out to continue to ride the vibe: " + playlist_url)

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
