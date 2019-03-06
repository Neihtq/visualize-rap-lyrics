from urllib.request import Request, urlopen, quote
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as sm 
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import requests, json, os, time
import lyricsgenius as genius

# Client access Token from envrionment variable
client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
assert client_access_token is not None, "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
api = genius.Genius(client_access_token)

def getArtistsFromList(URL):
    # URL is a BIllboard list,
    # 
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser")
    chart_items = html.finad_all("div", class_="ye-chart-item__title")
    return [item.get_text().strip() for item in chart_items]

def songsAreSame(song1, song2):
    seqA = sm(None, song1.lyrics, song2['lyrics'])
    seqB = sm(None, song2['lyrics'], song1.lyrics)
    return seqA.ratio() > 0.5 or seqB.ratio() > 0.5

def songInArtist(new_song, artist_lyrics):
    for song in artist_lyrics['artists'][-1]['songs']:
        return songsAreSame(new_song, song)
    return False

def downloadLyrics(artist_names, max_songs=None):
    artist_objects = [api.search_artist(name, max_songs=max_songs, take_first_result=True) for name in artist_names]

def main():
    url = ""
    artist_names = getArtistsFromList(url)
    print(artist_names)
    downloadLyrics(artist_names[:2])