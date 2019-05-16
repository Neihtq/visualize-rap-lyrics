import urllib.request as urllib2
from bs4 import BeautifulSoup
import csv, panda

URLs = ['all.html', 'all_two.html', 'all_three.html', 'all_four.html', 'all_five.html']
KEYS = ["title", "artist", "album", "release", "lyrics"]
BASE_URL = 'http://ohhla.com/'
AMAZON_REF_LINK = ' BUY NOW!\n'
csv_file = 'ohhla.csv'

def get_html(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup        

def get_rappers(soup):
    ''' store name and url of artis in a dicitonary
    returns list of dictionaries'''
    pre = soup.find('pre')
    artists = pre.find_all('a', href=True)
    dict_list = []
    for a in artists:
        stored_obj = {}
        stored_obj['name'] = a.text
        stored_obj['href'] = a['href']
        dict_list.append(stored_obj)
    return dict_list

def get_dir_ftp(href):
    soup = get_html(href)
    links = soup.find_all('a', text=True)
    dict_list = []
    for a in links[5:]:
        stored_obj = {}
        stored_obj['album'] = a.text
        stored_obj['href'] = a['href']
        dict_list.append(stored_obj)
    return dict_list

def get_track_dir_ftp(href):
    soup = get_html(href)
    links = soup.find_all('a', text=True)
    dict_list = []
    for a in links[5:]:
        stored_obj = {}
        stored_obj['title'] = a.text
        stored_obj['href'] = a['href']
        dict_list.append(stored_obj)
    return dict_list

def get_lyrics_raw(href):
    soup = get_html(href)
    text = soup.text.splitlines()[5:]
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
        stored_obj["tracks"] = []
        for a in links:
            stored_obj["tracks"].append({'title': a.text, 'href': a['href']})

        dict_list.append(stored_obj)
    return dict_list

def write_lyrics_to_csv(db):
    for url in URLs:
        
        soup = get_html(BASE_URL + URLs)
        rappers = get_rappers(soup)

        for artist in rappers:
            name = artist.name
            albums =
            if "html" in artist.href:
                continue
            else:
                albums = get_dir_ftp(artist.href)
                for album in album:
                    write_songtext(name, artist.href)

def write_songtext(name, hrefs):    
    # scrape all albums
    albums = []
    for a in hrefs:
        soup = get_html(a)
        albums = soup.find_all('a', text=True)[5:]

    for t in tracks:
        soup = get_html(t)
        # TODO

    with open(csv_file, 'a') as f:
        w = csv.DictWriter(f, KEYS)
        w.writerow(my_dict)


# TODO:
# - program to scrape whole OHHLA page
# - store in file and database
# - sort and clean data
# - Change dict structure