import urllib.request as urllib2
from bs4 import BeautifulSoup

URL = ['all.html', 'all_two.html', 'all_three.html', 'all_four.html', 'all_five.html']

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
