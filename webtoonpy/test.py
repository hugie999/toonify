import __init__ as webtoonpy

api = webtoonpy.webtoonScraper()
print(webtoonpy.strToInt("1.5M"))
# com = (api.getComic(url="https://www.webtoons.com/en/canvas/the-little-trashmaid/list?title_no=300138&page=1",type="canvas"))
# print(com)
# for i in api.getEpisodes(com):
#     print(i.__dict__)

com = api.getComic(id=599,type="originals")
print(com.__dict__)
eps = (api.getEpisodes(com,1))
for i in eps:
    print(i.__dict__)