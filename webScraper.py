import urllib.request as urllib2
from bs4 import BeautifulSoup

def get_html(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_rappers(soup):
    artists = soup.find_all('pre').find_all('a')
    dict_set = set()
    for a in artists:
        stored_obj = {}
        stored_obj["name"] = a.text
        stored_obj["href"] = a['href']
        dict_lists.add(stored_obj)
    return dict_set
