from urllib import error, parse, request
import json

URL = 'http://extratorrent.com/json/?search='

def plugin_search(query):
    url = URL + parse.quote(query)
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    result = request.urlopen(req)
    s = result.read().decode('utf-8')
    resjson = json.loads(s)
    reslist = resjson['list']
    return [{
        'title': r['title'],
        'url': r['torrentLink'],
        'seeders': r['seeds'],
        'peers': r['peers']
    } for r in reslist]
