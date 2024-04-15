import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

scope = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
]
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

before = spotify.queue()

results = spotify.add_to_queue(
    "https://open.spotify.com/track/4soYlU8WomPSHIr7RQiAun?si=9fe32e2c045549562"
)

after = spotify.queue()

print(before == after)
