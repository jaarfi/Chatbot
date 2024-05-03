import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Spoti:

    def __init__(self) -> None:
        scope = [
            "user-read-playback-state",
            "user-modify-playback-state",
            "user-read-currently-playing",
        ]
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def addToQueue(self, url):
        self.sp.add_to_queue(url)

    def getQueue(self):
        return self.sp.queue()
