import __init__ as webtoonpy

api = webtoonpy.webtoonScraper()

print(api.getComic(916339).previewImg)

