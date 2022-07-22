from googlesearch import search
import aiohttp

async def meme_search(qnt=1, subreddit=None) -> dict:
    async with aiohttp.ClientSession() as session:
        if(subreddit is None):
            async with session.get('https://meme-api.herokuapp.com/gimme') as r:
                if r.status == 200:
                    jsn = await r.json()
        else:
            async with session.get('https://meme-api.herokuapp.com/gimme/'+subreddit) as r:
                if r.status == 200:
                    jsn = await r.json()
        return jsn

def google_search(query) -> list:
    r = []
    for link in search(query, tld="co.in", lang='pt-br', num=3, start=0, stop=3, pause=2):
        r.append(link)
    return r

async def google_http_search(query=None) -> dict:
    request_params = {'q':query}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.com/search',params=request_params) as r:
            if r.status == 200:
                jsn = await r.json()
                return jsn

async def cat_search() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                jsn = await r.json()
                return jsn

async def dog_search(breed=None) -> dict:
    async with aiohttp.ClientSession() as session:
        if breed is None:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                if r.status == 200:
                    jsn = await r.json()
                    return jsn
        else:
            async with session.get('https://dog.ceo/api/breed/'+breed+'/images/random') as r:
                if r.status == 200:
                    jsn = await r.json()
                    return jsn


# r = meme_search()
# # print("Status code: ", r.status_code)
# # print("Headers: ", r.headers)
# # print("URL: ", r.url)
# # print("Text: ", r.text)

# jsn = json.loads(r.text)
# print(jsn['title'])
# print(jsn['url'])
# print(jsn['preview'][len(jsn['preview'])-1])