#! /usr/bin/env python3

from urllib import error, parse, request
import xml.etree.ElementTree as ET

TORRENT_URL = 'http://itorrents.org/torrent/'
SEARCH_URL = 'http://www.torrentdownloads.me/rss.xml?type=search&search='

def plugin_search(query):
    url = SEARCH_URL + query.split('+')
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041202 Firefox/1.0'})
    result = request.urlopen(req)
    s = result.read().decode('utf-8')
    root = ET.fromstring(s)
    res = []
    for item in root[0].iter('item'):
        torrent_url = TORRENT_URL + item.find('info_hash').text.upper() + '.torrent'
        res.append({
            'title': item.find('title').text,
            'url': torrent_url,
            'seeders': item.find('seeders').text,
            'peers': item.find('leechers').text
        })
    return res
