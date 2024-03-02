import __init__ as webtoonpy

api = webtoonpy.webtoonScraper()
print(webtoonpy.strToInt("1.5M"))
print(api.getComic(url="https://www.webtoons.com/en/thriller/dead-but-not-gone/list?title_no=4838",type="originals").previewImg)

