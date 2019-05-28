from bs4 import BeautifulSoup
import urllib.request as urllib2
import csv
import re

# TODO:
# - optimize runtime
# - sort and clean data (Maybe do with excel)
# - big artists: strip name and release from album title

URLs = ['all.html', 'all_two.html', 'all_three.html', 'all_four.html', 'all_five.html']
KEYS = ["title", "artist", "album", "release_year", "release_month", "lyrics"]
BASE_URL = 'http://ohhla.com/'
AMAZON_REF_LINK = ' BUY NOW!\n'
csv_file = 'ohhla.csv'


def scrape():
    for url in URLs:
        
        artist_obj = get_rappers(BASE_URL + url)
        
        small_artists = {}
        big_artists = {}
        for key, value in artist_obj:
            if "YT Cracker" in key:
                value = "anonymous/YT_crack/"
            url = BASE_URL + value
            soup = get_html(url)
            if 'html' in value:
                big_artists[key] = { "album": soup.find_all("table")[2:], "url": url}
            else:
                small_artists[key] = { "album": soup.find_all('a', text=True)[5:], "url": url}
        
        tmp = get_albums_small_artists(small_artists)
        albums = tmp[0]
        album_artist = tmp[1]

        albums_release = get_albums_big_artists(big_artists, albums, album_artist)

        for key, value in albums:
            for track in value["tracks"]:
                url = BASE_URL + value["url"] + track["href"]
                lyric = get_lyrics(url)
                write_to_csv(track.text, key, album_artist[key], albums_release[key], lyric)
            


def get_html(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup        


def get_rappers(url):
    soup = get_html(url)
    pre = soup.find('pre')
    artists = pre.find_all('a', href=True)
    artist_obj = {}
    for a in artists:
        name = a.text
        artist_obj[name] = a['href']
    return artist_obj

def get_lyrics(href):
    soup = get_html(href)
    text = soup.text.splitlines()[39:]
    lyrics = ""
    for line in text:
        lyrics += line
        if text.index(line) != len(text)-1:
            lyrics += "\n"
    return lyrics


def get_albums_small_artists(artists):
    albums = {}
    album_artist = {}
    for key, value in artists:
        for a in value["album"]:
            url = value["url"] + a["href"]
            titles = scrape_ftp_page(url)
            albums[a.text] = {"tracks": titles, "url": url}
            album_artist[a.text] = key
    return albums, album_artist


def get_albums_big_artists(big_artists, albums, album_artist):
    albums_release = {}
    for key, value in big_artists:
        for table in value["album"]:
            links = table.find_all('a', href=True)[1:]
            header = table.find("th").text.replace(AMAZON_REF_LINK, '').split("-")
            try:
                title = header[1]
            except IndexError:
                title = header[0]
            release = get_release_year_from_album(title)[0], get_release_year_from_album(title)[1]
            albums_release[title] = release
            albums[title] = {"tracks":links, "url": ""}
            album_artist[title] = key
    return albums_release


def download_lyrics():
    with open(csv_file, 'w') as f:
        w = csv.DictWriter(f, KEYS)
        w.writeheader()

    rappers = []
    for url in URLs:   
        soup = get_html(BASE_URL + url)
        rappers = get_rappers(soup)

    for artist in rappers:
        if 'html' in artist['href']:
            albums_big_artists = get_albums_big_artists(BASE_URL + artist['href'])
            store_lyrics_of_big_artist(artist['name'], albums_big_artists)
        else:
            store_lyrics(artist['name'], artist['href'])


def store_lyrics_of_big_artist(name, albums):
    for album in albums:
        tracks = album['tracks']
        for track in tracks:
            url = BASE_URL + track['href']
            album_title = album['album']
            release = get_release_year_from_album(album_title)[0], get_release_year_from_album(album_title)[1]
            write_to_csv(track['title'], album_title, name, release, get_lyrics(url))


def get_release_year_from_album(title):
    reg = r'([A-Z][a-z]+\.*\s)*(1|2)[0-9]+(\/[1|2][0-9]+)*'
    release = re.search(reg, title)
    if release is not None:
        release = release.group()
        if len(release.split()) > 1:
            return release.split()[0], release.split()[1]
        return "", release
    return "", ""


def scrape_ftp_page(href):
    url = BASE_URL + href
    return get_html(url).find_all('a', text=True)[5:]


def store_lyrics(name, href):
    if "YT Cracker" in name:
        href = "anonymous/YT_crack/"
        albums = scrape_ftp_page(href)
    else:
        albums = scrape_ftp_page(href)

    try:
        for album in albums:
            url = href + album['href']
            titles = scrape_ftp_page(url)
            for title in titles:
                write_to_csv(title.text[:-4], album.text[:-1], name, ("", ""), get_lyrics(BASE_URL + url + title['href']))
    except:
        print("Error at store_lyrics with ", name, )
                

def write_to_csv(title, album, artist, release, lyrics):
    row_dict = {"title": title,
                "album": album,
                "artist": artist,
                "release_year": release[1],
                "release_month": release[0],
                "lyrics": lyrics}
    with open(csv_file, 'a', encoding='utf-8') as f:
        w = csv.DictWriter(f, KEYS)
        w.writerow(row_dict)

