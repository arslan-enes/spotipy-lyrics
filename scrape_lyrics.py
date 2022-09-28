from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_lyrics(artist, song):
    soup = BeautifulSoup(requests.get(f'https://www.azlyrics.com/lyrics/{artist}/{song}.html').text, 'html.parser')
    lyrics = soup.findAll('div')[22].text  #.replace('?', '').replace('!', '').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('\'', '').replace('\"', '').replace(';', '').replace(':', '').replace('\n', ' ').lower()
    words_df = pd.DataFrame(lyrics.split(), columns=['lyrics'])
    return lyrics

print(get_lyrics('acdc', 'tnt'))
