import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"),
                                                                              client_secret=os.getenv("CLIENT_SECRET")))

eminem_uri = 'spotify:artist:7dGJo4pcD2V6oG8kP0tJRR'

results = spotify.artist_top_tracks(eminem_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
