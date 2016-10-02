#! /usr/bin/env python3

from urllib import error, parse, request
import lxml.html
from io import StringIO
import os
#import xml.etree.ElementTree as ET

#TORRENT_URL = 'http://itorrents.org/torrent/'
TORRENT_URL = 'http://www.cpasbien.cm/telechargement/'
SEARCH_URL = 'http://www.cpasbien.cm/recherche/'

def plugin_search(query):
    url = SEARCH_URL + query.replace(' ', '-') + '.html'
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041202 Firefox/1.0'})
    result = request.urlopen(req)
    s = result.read().decode('utf-8')
    html = lxml.html.fromstring(s)
    lines0 = html.find_class('ligne0')
    lines1 = html.find_class('ligne1')
    lines = lines0 + lines1
    res = []
    for line in lines:
        data = line.find_class('titre')[0]
        href = data.get('href')
        torrent_url = TORRENT_URL + os.path.basename(href).replace('.html','.torrent')
        seeders = 0
        peers = 0
        try:
            seeders = int(line.find_class('seed_ok')[0].text)
        except:
            seeders = 0
        try:
            peers = int(line.find_class('down')[0].text)
        except:
            peers = 0
        res.append({
            'title': data.text,
            'url': torrent_url,
            'seeders': seeders,
            'peers': peers
        })
    return res
