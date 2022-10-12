import pandas as pd
import spotify.spotipy_functions as sf
import re
import json
import numpy as np

countries = ['global', 'us', 'gb', 'ar', 'au', 'at', 'be', 'bo', 'br', 'bg', 'ca', 'cl', 'co', 'cr', 'cy', 'cz', 'dk', 'do', 'ec', 'sv', 'ee', 'fi', 'fr', 'de', 'gr', 'gt', 'hn', 'hk', 'hu', 'is', 'in', 'id', 'ie', 'il', 'it', 'jp', 'lv', 'lt', 'lu', 'my', 'mt', 'mx', 'nl', 'nz', 'ni', 'no', 'pa', 'py', 'pe', 'ph', 'pl', 'pt', 'ro', 'ru', 'sa', 'sg', 'sk', 'za', 'kr', 'es', 'se', 'ch', 'tw', 'th', 'tr', 'ua', 'ae', 'uy', 'vn']


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)
    # df = pd.read_csv('kworb.csv')
    # df = data_preparation(df)
    # df.to_csv('kworb_after_prep.csv', index=False)
    # print(df.iloc[:200, :])
    # df = add_spotify_data(df.iloc[:200, :])
    # df.to_csv('kworb_spotify_raw.csv', index=False)
    # print(df.head())
    df = pd.read_csv('kworb_spotify_raw.csv')
    spotify_features(df).to_csv('spotify_global_top_200.csv')


def add_spotify_data(dataframe):
    dataframe['spotify_audio_features'] = dataframe.apply(lambda x: sf.search_artist_song(x['artist'], x['track']), axis=1)
    return dataframe


def spotify_data_to_dataframe(spo_features):
    spo_features = spo_features.apply(lambda x: json.loads(x.replace('[', '').replace(']', '').replace("'", "\"")) if isinstance(x, str) else x)
    spotify_dataframe = pd.DataFrame()
    for feature in spo_features:
        if feature in [np.nan]:
            spotify_dataframe = pd.concat([spotify_dataframe, pd.DataFrame(np.nan, index=[0], columns=spotify_dataframe.columns)])
        else:
            spotify_dataframe = pd.concat([spotify_dataframe, pd.DataFrame(feature, index=[0])])
    return spotify_dataframe


def spotify_features(dataframe):
    spotify_dataframe = spotify_data_to_dataframe(dataframe.spotify_audio_features)
    spotify_dataframe.reset_index(inplace=True, drop=True)
    dataframe.reset_index(inplace=True, drop=True)
    columns = dataframe.columns.to_list() + spotify_dataframe.columns.to_list()
    dataframe = pd.concat([dataframe, spotify_dataframe], axis=1, ignore_index=True)
    dataframe.columns = columns
    return dataframe


def get_data():
    df = pd.DataFrame()
    for country in countries:
        df = df.append(pd.read_html(f'https://kworb.net/spotify/country/{country}_weekly.html')[0])
        print(country, pd.read_html(f'https://kworb.net/spotify/country/{country}_weekly.html')[0].shape[0])
    return df


def data_preparation(dataframe):
    dataframe = dataframe.reset_index()
    dataframe['artist'] = dataframe['Artist and Title'].apply(lambda x: x.split(' - ')[0].strip())
    dataframe['track'] = dataframe['Artist and Title'].apply(lambda x: x.split(' - ')[1].strip())
    dataframe['country'] = dataframe['index'].apply(lambda x: countries[x//200])
    dataframe.drop('index', axis=1, inplace=True)
    return dataframe


if __name__ == '__main__':
    main()
