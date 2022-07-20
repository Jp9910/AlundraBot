import requests
import json
from googlesearch import search

def meme_search(qnt=1, subreddit=None) -> requests.Response:
    if(subreddit is None):
        r = requests.get('https://meme-api.herokuapp.com/gimme')
        return r
    r = requests.get('https://meme-api.herokuapp.com/gimme/'+subreddit)
    return r

def google_search(query) -> list:
    r = []
    for link in search(query, tld="co.in", lang='pt-br', num=3, start=0, stop=3, pause=2):
        r.append(link)
    return r

def google_http_search(query=None) -> requests.Response:
    request_params = {'q':query}
    r = requests.get('https://www.google.com/search',params=request_params)
    return r

r = meme_search()
# print("Status code: ", r.status_code)
# print("Headers: ", r.headers)
# print("URL: ", r.url)
# print("Text: ", r.text)

jsn = json.loads(r.text)
print(jsn['title'])
print(jsn['url'])
print(jsn['preview'][len(jsn['preview'])-1])