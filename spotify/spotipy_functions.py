import pandas as pd
from scrape_lyrics import get_lyrics
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

load_dotenv()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"),
                                                                              client_secret=os.getenv("CLIENT_SECRET"),
                                                                              ),
                          requests_timeout=None)


def search_artist_song(artist, song):
    results = spotify.search(q=f'artist:{artist} track:{song}', type='track')
    items = results['tracks']['items']
    if len(items) > 0:
        print(spotify.audio_features(items[0]['id']))
        return spotify.audio_features(items[0]['id'])
    else:
        return None


def get_artist_id(artist_name):
    results = spotify.search(q=f'artist:{artist_name}', type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]['id']
    else:
        return None


def get_artist_albums(artist_id):
    results = spotify.artist_albums(artist_id, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    return albums_list_to_dataframe(albums)


def albums_list_to_dataframe(albums):
    albums = pd.DataFrame(albums).drop_duplicates(subset=['name'], keep='first')
    albums = pd.DataFrame({'album_id': albums['id'],
                           'album_artist': albums['artists'].apply(lambda x: x[0]['name'] if len(x) != 2 else x[0]['name'] + "," + x[1]['name']),
                           'album_name': albums['name'],
                           'album_image_url': albums['images'].apply(lambda x: x[0]['url']),
                           'album_release_date': albums['release_date'],
                           'album_total_tracks': albums['total_tracks']})
    return albums

def get_all_artist_tracks(artist_albums):
    tracks = []
    for album_id in artist_albums['album_id']:
        album_tracks = spotify.album_tracks(album_id)
        tracks.extend(album_tracks['items'])

    return get_all_artist_tracks_dataframe(tracks)


def get_all_artist_tracks_dataframe(tracks):
    tracks = pd.DataFrame(tracks).drop_duplicates(subset=['name'], keep='first')
    tracks = pd.DataFrame({'track_id': tracks['id'],
                           'track_name': tracks['name'],
                           'track_duration_ms': tracks['duration_ms'],
                           'track_explicit': tracks['explicit'],
                           'track_preview_url': tracks['preview_url']})
    return tracks


def get_top_track_ids(artist_id):
    results = spotify.artist_top_tracks(artist_id, country='US')
    tracks = results['tracks']
    return pd.DataFrame({'track_id': [track['id'] for track in tracks]})


if __name__ == '__main__':

    searched_track_id = spotify.search(q='artist:Dedublüman,  track:Belki')['tracks']['items'][0]['id']
    print(spotify.search(q='track:Metalingus'))
    print(spotify.audio_features(searched_track_id))



    # artist_name = 'Dua Lipa'
    # artist_id = get_artist_id(artist_name)
    # top_track_ids = get_top_track_ids(artist_id)
    # top_tracks_audio = spotify.audio_features(top_track_ids['track_id'].tolist())
    # top_tracks_audio = pd.DataFrame(top_tracks_audio)
    # top_tracks = get_all_artist_tracks_dataframe(spotify.tracks(top_track_ids['track_id'].tolist())['tracks'])
    # merged = pd.merge(top_tracks_audio, top_tracks, left_on='id', right_on='track_id')
    # print(merged)


    # artist_name = 'Dua Lipa'
    # artist_id = get_artist_id(artist_name)
    # artist_albums = get_artist_albums(artist_id)
    # artist_all_tracks = get_all_artist_tracks(artist_albums)
    # sample_track = artist_all_tracks.sample(1)
    # print(sample_track)
    # print(artist_name, sample_track['track_name'].values[0], sample_track['track_preview_url'].values[0])
    # print(get_lyrics(artist_name.lower().replace(' ', ''), sample_track['track_name'].values[0].lower().replace(' ', '')))
