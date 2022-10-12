from bs4 import BeautifulSoup
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords

def get_lyrics(artist, song):
    soup = BeautifulSoup(requests.get(f'https://www.azlyrics.com/lyrics/{artist}/{song}.html').text, 'html.parser')
    lyrics = soup.findAll('div')[22].text #replace('?', '').replace('!', '').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('\'', '').replace('\"', '').replace(';', '').replace(':', '').replace('\n', ' ').lower()
    words_df = pd.DataFrame(lyrics.split(), columns=['lyrics'])
    for word in stopwords.words('english'):
        words_df = words_df[words_df.lyrics != word]
    return lyrics
