## Recommendation module linking text_sentiment score w sentiment scores from user_library
import spotipy
#from all.ai import sentiment

class Recommendation:
    def __init__(self, user_sp):
        self.sp = user_sp
        self.user_lib = self.sp.current_user_saved_tracks()['items']
        #self.lib_sentiment = generate_library_sentimenet()

    def generate_library_sentiment(self):
        """
        Return dictionary of TRACK-->TRACK_SENTIMENT.
        """
        #for song in self.user_lib: