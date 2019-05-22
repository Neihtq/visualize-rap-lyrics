from bs4 import BeautifulSoup
import urllib.request as urllib2
import csv
import re

# TODO:
# - sort and clean data (Maybe do with excel)
# - big artists: strip name and release from album title


URLs = ['all.html', 'all_two.html', 'all_three.html', 'all_four.html', 'all_five.html']
KEYS = ["title", "artist", "album", "release_year", "release_month", "lyrics"]
BASE_URL = 'http://ohhla.com/'
AMAZON_REF_LINK = ' BUY NOW!\n'
csv_file = 'ohhla.csv'


def get_html(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup        


def get_rappers(soup):
    pre = soup.find('pre')
    artists = pre.find_all('a', href=True)
    dict_list = []
    for a in artists:
        stored_obj = {'name': a.text, 'href': a['href']}
        dict_list.append(stored_obj)
    return dict_list


def get_lyrics(href):
    soup = get_html(href)
    text = soup.text.splitlines()[39:]
    lyrics = ""
    for line in text:
        lyrics += line
        if text.index(line) != len(text)-1:
            lyrics += "\n"
    return lyrics


def get_albums_big_artists(href):
    soup = get_html(href)
    dict_list = []
    tables = soup.find_all("table")[2:]
    for t in tables:
        links = t.find_all("a", href=True)[1:]
        stored_obj = {}
        header = t.find("th").text.replace(AMAZON_REF_LINK, '').split("-")
        try:
            title = header[1]
        except IndexError:
            title = header[0]
        stored_obj["album"] = title
        stored_obj["tracks"] = [{'title': a.text, 'href': a['href']} for a in links]
        dict_list.append(stored_obj)
    return dict_list


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
    try:
        return get_html(url).find_all('a', text=True)[5:]
    except:
        print("exception at with " + url)


def store_lyrics(name, href):
    albums = scrape_ftp_page(href)
    for album in albums:
        url = href + album['href']
        titles = scrape_ftp_page(url)
        for title in titles:
            write_to_csv(title.text[:-4], album.text[:-1], name, ("", ""), get_lyrics(BASE_URL + url + title['href']))
                

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

