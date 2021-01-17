## Recommendation module linking text_sentiment score w sentiment scores from user_library
import spotipy
import spotipy.oauth2
import math
import os

def distance_between(P1, P2):
        x_dist = P2[0] - P1[0]
        y_dist = P2[1] - P1[1]
        return math.sqrt(x_dist ** 2 + y_dist ** 2)

class Recommender:
    def __init__(self, sp_user, sp_client, curr_state, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET):
        """
            params: spotipy.Spotify, spotipy.client.Spotify, [valence, energy] --> Recommender
        """
        self.user_id = SPOTIFY_CLIENT_ID
        self.secret_id = SPOTIFY_CLIENT_SECRET
        self.user = sp_user
        self.client = sp_client
        self.current_state = curr_state ## strength: [0.0, 1.0] ; magnitude: [0.0 , 1.0]
        self.last_rec_tracks = []
        self.followed_artists = self.user.current_user_followed_artists(limit=10, after=None)['artists']['items'] # want to sort by most preferred, rn j first 20

    # want to make this generic for any set of tracks we might want to test
    ## in the future, use Browse API Recommendations call as a benchmark to the metrics we test
    ## for like science ig
    def generate_trackSentiment_distances(self, n):
        """
            Calculate distance between current_state and set of tracks' (followed_artists) sentiment
            n (top_n) --> [list[distances], list[list[valence, energy]]] (2x2 matrix of artists' top n songs' features)
        """
        tracks = []
        distances_from_currentState = []
        for artist in self.followed_artists:
            artist_top_tracks = self.client.artist_top_tracks(artist['uri'])
            top_n = artist_top_tracks['tracks'][:n] # top number is arbitrary
            for track in top_n:
                audio_features = self.client.audio_features([track['uri']])[0]
                sentiment_point = [audio_features['valence'], audio_features['energy']] ## valence: [0.0, 1.0] ; energy: [0.0 , 1.0]

                distances_from_currentState.append(distance_between(self.current_state, sentiment_point))
                tracks.append(track['uri'])
        self.last_rec_tracks = sorted(tracks)
        return distances_from_currentState

    def generate_track_rec(self):
        """
            --> track_uri (song recommendation) 
        """
        distances = self.generate_trackSentiment_distances(3)
        min_index = distances.index(min(distances))
        return self.last_rec_tracks[min_index]

    # generalize for other identifiers maybe
    def generate_playlist(self, token, pl_name, pl_len, pl_desc):
        """
            track_id (song rec) --> playlist_URL (?) (song recommendation) 
        """

        ## !! need to reauthorize the client for some reason, this should be handled better for sure
        SPOTIFY_CLIENT_ID="56c1ae8e401640d6b90b8066c3821f95"
        SPOTIFY_CLIENT_SECRET="665045e7a1a44db7ae68b220bf1f12a3" # !!! hide key
        SPOTIPY_REDIRECT_URI="https://abhivk23.github.io"
        REQUESTED_SCOPES="user-library-read, user-follow-read, playlist-modify-public, playlist-modify-private"
        username = "npby7v4xwgsty64kobmk9xb3w"

        # Generate Spotify auth_token
        try:
            token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

        except:
            os.remove(f".cache-{username}")
            token = spotipy.util.prompt_for_user_token(username, scope=REQUESTED_SCOPES, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
        
        # Configure user/client
        sp_user = spotipy.Spotify(auth=token)
        sp_client = spotipy.client.Spotify(auth=token)
        user_id = sp_user.me()['id']

        # build playlist
        sp_client.user_playlist_create(user_id, pl_name, public=True, collaborative=False, description=pl_desc)
        playlist = self.client.user_playlists(user_id)['items'][0]
        url = playlist['external_urls']['spotify']
        playlist_id = playlist['id']

        # add top "pl_len" tracks minimized w.r.t distance to current_state to playlist
        sp_user.playlist_add_items(playlist_id, self.last_rec_tracks[:pl_len])

        return url



