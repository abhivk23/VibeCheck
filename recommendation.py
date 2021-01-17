## Recommendation module linking text_sentiment score w sentiment scores from user_library
import spotipy
import math

def distance_between(P1, P2):
        x_dist = P2[0] - P1[0]
        y_dist = P2[1] - P1[1]
        return math.sqrt(x_dist ** 2 + y_dist ** 2)

class Recommender:
    def __init__(self, sp_user, sp_client, curr_state):
        """
            params: spotipy.Spotify, spotipy.client.Spotify, [valence, energy] --> Recommender
        """
        self.user = sp_user
        self.client = sp_client
        self.current_state = curr_state ## strength: [0.0, 1.0] ; magnitude: [0.0 , 1.0]
        self.followed_artists = self.user.current_user_followed_artists(limit=10, after=None)['artists']['items'] # want to sort by most preferred, rn j first 20

    # want to make this generic for any 
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
        return tracks, distances_from_currentState

    def generate_track_rec(self):
        """
            --> track_uri (song recommendation) 
        """
        tracks, distances = self.generate_trackSentiment_distances(3)
        min_index = distances.index(min(distances))
        return tracks[min_index]