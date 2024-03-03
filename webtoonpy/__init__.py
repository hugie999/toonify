"""a small lil' wrapper for the webtoon rapidapi api
remember to use a token and always practice safe requesting"""
#webtoon in python moment
#made with: https://rapidapi.com/apidojo/api/webtoon
#this is my first python module please be nice😥

import requests
import base64
import time
import bs4
import datetime
import re

__version__ = '0.0.3'
BASECOMICURLS = ["https://www.webtoons.com/en/canvas/barry-and-bobby/list?title_no=",
                 "https://www.webtoons.com/en/thriller/dead-but-not-gone/list?title_no=",
                 "https://www.webtoons.com/en/canvas/the-little-trashmaid/new-dock/viewer?title_no={TITLENO}&episode_no={EPISODENO}"] #for scraping
"""base comic urls for scrapers [0] = canvas (barry and bobby) [1] = original (dead 🅱️ut not gone), 
    [2] = episode (canvas) has two formats: 'TITLENO' and 'EPISODENO' pretty self explanitory"""
# def createComicJson(name:str,id:int,author:str) -> dict:
#     """allows creation of comic() classes without request json"""

def strToInt(x:str):
    if type(x) == float or type(x) == int:
        return x.replace(",","")
    if 'K' in x:
        if len(x) > 1:
            return int(float(x.replace('K', '').replace(",","")) * 1000)
        return 1000
    if 'M' in x:
        if len(x) > 1:
            return int(float(x.replace('M', '').replace(",","")) * 1000000)
        return 1000000
    if 'B' in x:
        return int(float(x.replace('B', '').replace(",","")) * 1000000000)
    else:
        return int(float(x.replace(",","")))
    return 0
"""THANK YOU SO F#CKING MUCH PERSON ON STACK OVERFLOW (link : https://stackoverflow.com/a/41028390"""


def loadImage(url:str) -> bytes:
    "this litterally returns a png so be prepared"
    newurl = "https://webtoon-phinf.pstatic.net/"+url
    #fuck you webtoon
    resp = requests.get(newurl,headers={'User-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Mi MIX 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36','Referer':'http://m.webtoons.com/'})# <- teh secret sauce
    return resp.content
def getWebPage(url) -> list[str]:
    """returns the content of the page and the final url in a list"""
    resp = requests.get(url,allow_redirects=True)
    return [resp.content.decode(),resp.url]

class webtoonImage():
    def __init__(self,raw:dict) -> None:
        """dw this can just be turned into an str to get the adress"""
        #this is what it should look like
        # {
        #    "sortOrder": 1,
        #    "cutId": 0,
        #    "url": "/20200404_14/158599346155149eBt_JPEG/a0aa0a1d-9562-4e0e-a80c-c0fd98151a6a.jpg?type=q70",
        #    "fileSize": 3003,
        #    "width": 800,
        #    "height": 200
        #  }
        self._json:dict = raw
        self.order = raw["sortOrder"]
        self.url:str = raw["url"]
        self.fileSize = raw["fileSize"]
        self.size = [raw["width"],raw["height"]]
        """-> [width,height] <-"""
    def __str__(self) -> str:
        return self.url
    @property
    def imgdata(self) -> bytes:
        return loadImage(self.url)
    @property
    def imgb64(self)  -> str:
        return base64.encodebytes(loadImage(self.url)).decode().replace("\n","")

class homePage():
    def __init__(self,raw:dict) -> None:
        """this class represents the webtoon homepage"""
        #reccommended list
        self.recTitleList:list[comic] = []
        """reccommended titles for the home page"""
        for i in raw['challengeHomeRecommendTitleList']:
            self.recTitleList.append(comic(i['titleInfo'],"canvas",i['linkTitleNo']))

class episodeImages():
    def __init__(self) -> None:
        """the images for a webtoon episode
        along with some other metadata maybey"""

class oldEpisode():
    def __init__(self,raw:dict,comicId:int) -> None:
        """its like the other episode class but with images
        raw should start from 'episodeInfo'"""
        self._json = raw
        self.no = raw["episodeSeq"]
        self.author = raw["writingAuthorName"]
        self.comicId = comicId
        try:
            self.next = raw["nextEpisodeNo"]
            """ps its good practice to check if next exsists"""
        except:
            print("no next episode!")
        else:
            self.nextEpisodeThumbnail = raw["nextEpisodeThumbnailUrl"]
        self.thumbnail = raw["thumbnailImageUrl"]
        
        self.images:list[webtoonImage] = []
        for i in raw["imageInfo"]:
            self.images.append(webtoonImage(i))

class headerInfo():
    def __init__(self,remaining:int,total:int) -> None:
        """represents how many api calls are left
        (its called headerinfo because thats in the header)"""
        self.requestsUsed = total-remaining
        self.remaining = remaining
        self.totalAvalible = total
    def __str__(self) -> str:
        return f"headerInfo -> (used: {self.requestsUsed}, remaining: {self.remaining}, avalible: {self.totalAvalible}) <-"

class partialComic():
    def __init__(self,json:dict) -> None:
        """returned by listComics
        thease dont have as much metadata as the normal comic class"""
        # <li>
        #     <a href="https://www.webtoons.com/en/comedy/cursed-princess-club/list?title_no=1537" class="daily_card_item NPI=a:list,i=1537,r=1,g:en_en" data-title-unsuitable-for-children="false" data-title-unsuitable-for-children-skin="harmful_white_skin1">
        #         <img src="https://webtoon-phinf.pstatic.net/20190226_224/1551120711003gUe7B_JPEG/10_EC8DB8EB84A4EC9DBC_ipad.jpg?type=a138" width="138" height="138" alt="Cursed Princess Club">
        #         <p class="genre g_comedy">Comedy</p>
        #         <div class="info">
        #             <p class="subj">Cursed Princess Club</p>
        #             <p class="author">LambCat</p>
        #             <p class="icon_area"></p>
        #         </div>
        #         <p class="grade_area"><span class="ico_like3">like</span><em class="grade_num">23.6M</em></p>
        #     </a>
        # </li>
        self.genre:str     = json["genre"]
        self.author:str    = json["author"]
        self.name:str      = json["name"]
        self.likes:int     = json["likes"]
        self.id:int        = json["id"]
        self.thumbNail:str = json["thumb"]
        self.isNSFW:bool   = json["isNSFW"]
        
        pass

#its up here cus it returns a header info (sorry for the inconsistant placeing)
class episode():
    def __init__(self,raw:dict) -> None:
        """basically just episode class"""
        self._json = raw
        self.parentID:int    = raw["titleNo"]
        self.type:str        = raw["type"]
        self.episodeNO:int     = raw["episodeNo"] #i deadass put "136" here originally lmfao
        self.episodeName:str   = raw["episodeTitle"]
        self.thumbnail:str     = raw["thumbnailImageUrl"]
        self.likeCount:int     = raw["likeCount"]
        self.publishedDate:str = raw["publishedDate"]
    def __str__(self) -> str:
        return f"name: {self.episodeName}, no: {self.episodeNO}, parent: {self.parentID}"
    
    pass

class comic():
    def __init__(self,json:dict,type="canvas",id:int|None =None) -> None:
        """yes i know they are called webtoons or webcomics but it would get cofuseing fast if i had a webtoon and webtoonapi class ok?
        protip: just like most of the other classes this one shouldnt be made by your code"""
        self._json      = json
        """its literally just the raw json"""
        self.name       = json["title"]
        if id:
            self.id         = id
        else:
            self.id         = json["titleNo"]
        
        self.views       = json["views"]
        self.subscribers = json["subscribers"]
        self.raiting     = json["stars"]
        
        """the cooler self.name"""
        self.author     = json["author"]
        self.authorURL  = json["authorLink"]
        self.previewImg = json["thumbnail"]
        "the thumbnail for the comic (use loadImage() to load this!)"
        try:
            self.showNotice     = json["ageGradeNotice"]
            """wether to show a notice about a webtoon being adult"""
        except KeyError:
            self.showNotice = None #should really just make a partialComic class
        self.type       = type
        assert type in ["canvas","originals"]
        """either 'canvas' or originals"""
        self.epNum = json["totalServiceEpisodeCount"]
        self.summary = json["summary"]
        
        
    def __str__(self) -> str:
        return f"name: {self.name}, id: {self.id}, author:{self.author}"
class search():
    def __init__(self,query:str,start=0,size=20,lang="en",type="canvas",total=0,items:list[comic]=[],output={}) -> None:
        """search class that represents a search on webtoon (no duh) 
        (this shouldnt be made in your code only by webtoonapi() if you are makeing this then you should really consifer what choices lead up to this)"""
        self.type  = type
        assert type in ["canvas","originals"]
        self.query      = query
        self.start      = start
        self.size       = size
        self._rawOutput = output
        self.total      = total
        self.items      = items
    def __str__(self) -> str:
        return self._rawOutput
    
class webtoonCache():
    def __init__(self,rawJson:dict|None=None) -> None:
        """a cache of api data so you dont have to use 50 api requests😎
        ps: dont make this yourself this is just for webtoonapi() to make"""
        
        # self._partialEpisodeCache:list[partialEpisode] = []
        self._comicOriginalsCache:list[episode]        = []
        self._episodeCacheCanvas:list[episode]         = []
        # self._comicOriginalsCache:list[comic]        = []
        # self._episodeOriginalsCache:list               = []
        self._comicCanvasCache:list[comic]             = []
        # self._searchCache:list[search]               = []
        self._genresCache:dict                         = None
        self.listedOriginals                           = False
        if rawJson:
            # for i in rawJson["parEpisode"]:
            #     self._partialEpisodeCache.append(partialEpisode(i))
            # for i in rawJson["comicOriginals"]:
            #     self._comicOriginalsCache.append(episode(i[0],i[1]))
            # for i in rawJson["comicCanvas"]:
            #     self._episodeCacheCanvas.append(episode(i[0],i[1]))
            for i in rawJson["comicOriginals"]:
                self._comicOriginalsCache.append(comic(i,"originals"))
            for i in rawJson["comicCanvas"]:
                self._comicCanvasCache.append(comic(i,"canvas"))
            self.listedOriginals      = rawJson["hasListedOriginals"]
    def clean(self) -> None:
        pass
        # self._partialEpisodeCache = list(set(self._partialEpisodeCache))
        # self._episodeCacheCanvas        = list(set(self._episodeCacheCanvas))
        # self._episodeCacheCanvas        = list(set(self._episodeCacheCanvas))
        # self._comicOriginalsCache = list(set(self._comicOriginalsCache))
        # self._comicCanvasCache    = list(set(self._comicCanvasCache))
    def addComicToCache(self,comics:list[comic],type:str):
        if type == "canvas":
            self._comicCanvasCache += comics
            print(self._comicCanvasCache)
        elif type == "originals":
            self._comicOriginalsCache += comics
        else:
            raise TypeError(f"argument 'type' was not 'canvas' or 'originals'! (instead it was '{type}')")
    def checkComic(self,id:int,type:str) -> comic|None:
        if type == "canvas":
            for i in self._comicCanvasCache:
                # print(i.id)
                # print(id)
                # print(id == i.id)
                if i.id == id:
                    return i
        elif type == "originals":
            for i in self._comicOriginalsCache:
                if i.id == id:
                    return i
        else:
            raise TypeError(f"argument 'type' was not 'canvas' or 'originals'! (instead it was '{type}')")
        return None
    def reset(self):
        self = webtoonCache()
    def addEpisodeToCache(self,episodes:list[episode]):
        raise NotImplementedError("episode cacheing isnt done yet!")
        if type(episodes) == list:
            self._episodeCache += episodes
        elif type(episodes) == episodeList:
            self._partialEpisodeCache += episodes.episodes
        else:
            raise ValueError("bad type for the function.")
        # print(self._comicCanvasCache)
    def checkEpisodeOriginals(self,comicId:int,id:int) -> episode|None:
        raise NotImplementedError("episode cacheing isnt done yet!")
        for i in self._comicOriginalsCache:
            if i.comicId == comicId:
                if i.no == id:
                    return i
        return None
    def checkEpisodeCanvas(self,comicId:int,id:int) -> episode|None:
        for i in self._comicCanvasCache:
            if i.comicId == comicId:
                if i.no == id:
                    return i
        return None
    def serialise(self) -> dict:
        """turn the ENTIRE cache into a dict for easy storage"""
        retvar =  {
            "parEpisode":[],
            "episodeCanvas":[],
            "episodeOriginals":[],
            "comicOriginals":[],
            "comicCanvas":[],
            "hasListedOriginals":[],
            "hasListedCanvas":[]
            }
        for i in self._partialEpisodeCache:
            retvar["parEpisode"].append(i._json)
        for i in self._comicOriginalsCache:
            retvar["comicOriginals"].append(i._json)
        for i in self._comicCanvasCache:
            retvar["comicCanvas"].append(i._json)
        retvar["hasListedOriginals"] = self.listedOriginals
        return retvar

class webtoonScraper():
    def __init__(self,testMode=False,verbose=True) -> None:
        """creates a webtoon api class with your token and languedge (me when i cant spell)
        (testmode uses preset values for testing)"""
        # if not token:
        #     print("hey you need a token for this!\ntokens are here: https://rapidapi.com/apidojo/api/webtoon/details")
        # assert token
        self._latestresp:requests.Response = None
        self.token = None
        self.lang  = "en"
        self.testmode = testMode
        self.verbose = verbose
        self.useWaitTimer = True
        self.waitTime     = 1
        # self._soup = bs4.BeautifulSoup()
        self.cache = webtoonCache()
        self._defaultheader = {}
        # self._defaultheader = {
        #     "X-RapidAPI-Key": token,
        #     "X-RapidAPI-Host": "webtoon.p.rapidapi.com"}
        self._defaulturl = "https://webtoon.p.rapidapi.com/"
    def getRequestAmount(self) -> None:
        """returns none
        will be removed eventually"""
        return None
    
    def getGenres(self) -> dict:
        if self.verbose:
            print("getGenres")
        if self.testmode:
            #test mode go brrr
            return {'message': {'type': 'response', 'service': 'com.naver.webtoon', 'version': '0.0.1', 'result': {'genreTabList': {'genreTabs': [{'name': 'All', 'index': 0, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/ALL.png?dt=2022022201', 'code': 'ALL'}, {'name': 'Comedy', 'index': 1, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/COMEDY.png?dt=2022022201', 'code': 'COMEDY'}, {'name': 'Fantasy', 'index': 2, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/FANTASY.png?dt=2022022201', 'code': 'FANTASY'}, {'name': 'Romance', 'index': 3, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/ROMANCE.png?dt=2022022201', 'code': 'ROMANCE'}, {'name': 'Slice of life', 'index': 4, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SLICE_OF_LIFE.png?dt=2022022201', 'code': 'SLICE_OF_LIFE'}, {'name': 'Sci-fi', 'index': 5, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SF.png?dt=2022022201', 'code': 'SF'}, {'name': 'Drama', 'index': 6, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/DRAMA.png?dt=2022022201', 'code': 'DRAMA'}, {'name': 'Short story', 'index': 7, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SHORT_STORY.png?dt=2022022201', 'code': 'SHORT_STORY'}, {'name': 'Action', 'index': 8, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/ACTION.png?dt=2022022201', 'code': 'ACTION'}, {'name': 'Superhero', 'index': 9, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SUPER_HERO.png?dt=2022022201', 'code': 'SUPER_HERO'}, {'name': 'Heart-warming', 'index': 10, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/HEARTWARMING.png?dt=2022022201', 'code': 'HEARTWARMING'}, {'name': 'Thriller', 'index': 11, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/THRILLER.png?dt=2022022201', 'code': 'THRILLER'}, {'name': 'Horror', 'index': 12, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/HORROR.png?dt=2022022201', 'code': 'HORROR'}, {'name': 'Post-Apocalyptic', 'index': 13, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/POST_APOCALYPTIC.png?dt=2022022201', 'code': 'POST_APOCALYPTIC'}, {'name': 'Zombies', 'index': 14, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/ZOMBIES.png?dt=2022022201', 'code': 'ZOMBIES'}, {'name': 'School', 'index': 15, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SCHOOL.png?dt=2022022201', 'code': 'SCHOOL'}, {'name': 'Supernatural', 'index': 16, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SUPERNATURAL.png?dt=2022022201', 'code': 'SUPERNATURAL'}, {'name': 'Animals', 'index': 17, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/ANIMALS.png?dt=2022022201', 'code': 'ANIMALS'}, {'name': 'Crime/Mystery', 'index': 18, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/CRIME_MYSTERY.png?dt=2022022201', 'code': 'CRIME_MYSTERY'}, {'name': 'Historical', 'index': 19, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/HISTORICAL.png?dt=2022022201', 'code': 'HISTORICAL'}, {'name': 'Informative', 'index': 20, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/TIPTOON.png?dt=2022022201', 'code': 'TIPTOON'}, {'name': 'Sports', 'index': 21, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/SPORTS.png?dt=2022022201', 'code': 'SPORTS'}, {'name': 'Inspirational', 'index': 22, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/INSPIRATIONAL.png?dt=2022022201', 'code': 'INSPIRATIONAL'}, {'name': 'All Ages', 'index': 23, 'iconImage': 'https://webtoons-static.pstatic.net/image/genre/challenge_icon/ALL_AGES.png?dt=2022022201', 'code': 'ALL_AGES'}], 'count': 24}}}}
        resp = requests.get(self._defaulturl+"canvas/genres/list", headers=self._defaultheader, params={"language":self.lang})
        print(resp.json())
        print(resp.headers)
        self._latestresp = resp
        return resp.json()
    def doSearch(self,query:str,start=0,size=20,type="canvas") -> search:
        """search webtoon for comics"""
        if self.testmode:
            print("doSearch() does not support test mode!")
        if self.verbose:
            print("doSearch()")
        assert not self.testmode
        assert start > -1
        assert size <= 20
        assert type in ["canvas","originals"]
        if type == "originals":
            raise NotImplementedError("originals are not supported at the moment ):")
        params = {"query": query,"startIndex": start,"pageSize": size,"language": self.lang}
        resp = requests.get(self._defaulturl+type+"/search", headers=self._defaultheader, params=params).json()["message"] #really good practice totally
        if self.verbose:
            print(resp)
        items = []
        for i in resp["result"]["challengeSearch"]["titleList"]:
            items.append(comic(i))
        out = search(query,start,size,self.lang,type,resp["result"]["challengeSearch"]["total"],items,resp)
        self._latestresp = resp
        return out

    def listComics(self) -> list[comic]: 
        """list EVERY comic in the originals section as a list
        please only use this if you know what your doing!"""
        assert not self.testmode
        wp = getWebPage("https://www.webtoons.com/en/originals")[0]
        #<ul class="daily_card">
        soup = bs4.BeautifulSoup(wp)
        pot:bs4.Tag #get it like soup pot... please laugh
        bowl:bs4.Tag
        comics:list[partialComic] = []
        for pot in soup.find_all("ul",{"class":"daily_card"}):
            print(f"{type(pot)}")
            for bowl in pot.find_all("li"):
                print(type(bowl))
                # <li>
                #     <a href="https://www.webtoons.com/en/comedy/cursed-princess-club/list?title_no=1537" class="daily_card_item NPI=a:list,i=1537,r=1,g:en_en" data-title-unsuitable-for-children="false" data-title-unsuitable-for-children-skin="harmful_white_skin1">
                #         <img src="https://webtoon-phinf.pstatic.net/20190226_224/1551120711003gUe7B_JPEG/10_EC8DB8EB84A4EC9DBC_ipad.jpg?type=a138" width="138" height="138" alt="Cursed Princess Club">
                #         <p class="genre g_comedy">Comedy</p>
                #         <div class="info">
                #             <p class="subj">Cursed Princess Club</p>
                #             <p class="author">LambCat</p>
                #             <p class="icon_area"></p>
                #         </div>
                #         <p class="grade_area"><span class="ico_like3">like</span><em class="grade_num">23.6M</em></p>
                #     </a>
                # </li>
                #===to get===
                # ["author"]
                # ["genre"]
                # ["name"]
                # ["likes"]
                # ["id"]
                # ["thumb"]
                # ["isNSFW"]
                print(partialComic(
                    {"genre":bowl.find("p").string,
                     "author":bowl.find("p",{"class":"author"}).string,
                     "name":bowl.find("p",{"class":"subj"}).string,
                     "likes":strToInt(
                         bowl.find("p",{"class":"grade_area"}).find("em").string
                         ),
                     "id":int(re.findall(
                         "i=[0-9]*",bowl.find("a").attrs["class"])[0].removeprefix("i=")),
                     "thumb":bowl.find("img").src,
                     "isNSFW":{"true":True,"false":False}[bowl.find("a").attrs["data-title-unsuitable-for-children"]]
                     }
                )).__dict__
                quit()

    def getComic(self,id:int|str|None=None,url:str|None="",type="canvas") -> comic: #done!
        assert not self.testmode
        assert type in ["canvas","originals"]
        assert url or id
        if url:
            id = url.split("?title_no=")[1].split("&page=")[0]
            print(id)
        if id.__class__ != int:
            id = int(id) #fixes cache not working if id is an str
        if type == "canvas":
            # print(self._requestsSession.cookies)
            wp = getWebPage(BASECOMICURLS[0]+str(id))[0]
            soup = bs4.BeautifulSoup(wp,"html.parser")
            comicName = soup.find("meta",{"property":"og:title"}).attrs["content"]
            comicAuthorRaw = soup.find("a",{"class":"author"})
            comicAuthor = {"name":comicAuthorRaw.contents[0],"link":comicAuthorRaw.attrs["href"]}
            thumbnailURL = soup.find("img").attrs["src"]
            episodeCount = soup.find("li",attrs={"class":"_episodeItem"}).attrs["data-episode-no"]
            pageCount    = 0 #class="pg_next"
            summary  = soup.find("p",attrs={"class","summary"}).contents[0]
            raitingsArea = soup.find("ul",attrs={"class":"grade_area"}).find_all("em",attrs={"class":"cnt"})
            # print(raitingsArea[0])
            
            # print(thumbnailURL)
            comicJson = {"title":comicName,
                         "titleNo":id,
                         "author":comicAuthorRaw.contents[0],
                         "authorLink":comicAuthorRaw.attrs["href"],
                         "thumbnail":thumbnailURL,
                         "ageGradeNotice":False, #implement later ):
                         "totalServiceEpisodeCount":episodeCount,
                         "summary":summary,
                         "views":strToInt(raitingsArea[0].contents[0].replace(",","")),
                         "subscribers":strToInt(raitingsArea[1].contents[0].replace(",","")),
                         "stars":float(raitingsArea[2].contents[0])}
            return comic(comicJson)
        else:
            wp = getWebPage(BASECOMICURLS[1]+str(id))[0]
            soup = bs4.BeautifulSoup(wp,"html.parser")
            comicName = soup.find("meta",{"property":"og:title"}).attrs["content"]
            comicAuthorRaw = soup.find("a",{"class":"author"})
            comicAuthor = {"name":comicAuthorRaw.contents[0],"link":comicAuthorRaw.attrs["href"]}
            thumbnailURL = soup.find("meta",{"property":"og:image"}).attrs["content"]
            episodeCount = soup.find("li",attrs={"class":"_episodeItem"}).attrs["data-episode-no"]
            pageCount    = 0 #class="pg_next"
            summary  = soup.find("p",attrs={"class","summary"}).contents[0]
            raitingsArea = soup.find("ul",attrs={"class":"grade_area"}).find_all("em",attrs={"class":"cnt"})
            # print(raitingsArea[0])
            
            # print(thumbnailURL)
            comicJson = {"title":comicName,
                         "titleNo":id,
                         "author":comicAuthorRaw.contents[0],
                         "authorLink":comicAuthorRaw.attrs["href"],
                         "thumbnail":thumbnailURL,
                         "ageGradeNotice":False, #implement later ):
                         "totalServiceEpisodeCount":episodeCount,
                         "summary":summary,
                         "views":strToInt(raitingsArea[0].contents[0].replace(",","")),
                         "subscribers":strToInt(raitingsArea[1].contents[0].replace(",","")),
                         "stars":float(raitingsArea[2].contents[0])}
            return comic(comicJson,"originals")
        return
        
        if id.__class__ != int:
            id = int(id) #fixes cache not working if id is an str
        cachedComic = self.cache.checkComic(id,type)
        print(cachedComic)
        if cachedComic:
            return cachedComic
        else:
            resp = requests.get(self._defaulturl+type+"/titles/get-info",{"titleNo":id,"language":self.lang},headers=self._defaultheader).json()["message"]
            print(resp)
            self.cache.addComicToCache([comic(resp["result"]["titleInfo"])],type)
            return comic(resp["result"]["titleInfo"])
    
    def loadFullEpisode(self,oldEpisode:episode) -> None:
        #note: every page has 10 episodes
        raise NotImplementedError("full episodes aren't implemented yet!")
        if oldEpisode.type == "canvas":
            wp = getWebPage(BASECOMICURLS[2].format(TITLENO=oldEpisode.parentID,EPISODENO=oldEpisode.episodeNO))
            print(wp)
            print(BASECOMICURLS[2].format(TITLENO=oldEpisode.parentID,EPISODENO=oldEpisode.episodeNO))
            

        return
        params = {"titleNo":oldEpisode.parentID,"episodeNo":oldEpisode.episodeNO,"language":self.lang}

        resp = requests.get(self._defaulturl+oldEpisode.type+"/episodes/get-info", headers=self._defaultheader, params=params)
        self._latestresp = resp
        return episode(resp.json()["message"]["result"]["episodeInfo"],oldEpisode.parentID)
    
    def getEpisodes(self,comicToUse:comic|int,page:int=1,typeOf:str="canvas") -> list[episode]: #done!
        """returns episodes (reminder that episodes are returned in reverse order (last to first) so be carefulas)
        (note: currently dosent support cacheing)
        (note2: page starts at 1 and not 0)"""
        assert page > 0
        assert type(comicToUse) in [comic,int]
        assert typeOf in ["canvas","originals"]
        if type(comicToUse) == comic:
            comicid = comicToUse.id
            typeOf  = comicToUse.type
        else:
            comicid = comicToUse
        
        if typeOf == "canvas":
            wpPre = getWebPage(BASECOMICURLS[0]+str(comicid)+f"&page={page}")
            self.spamWait()
            wp    = getWebPage(wpPre[1]+f"&page={page}")[0]
            # print(wp)
            soup = bs4.BeautifulSoup(wp,"html.parser")
            episodes = []
            bowl:bs4.Tag
            # print(soup.find("li",{"class":"_episodeItem"}))
            for bowl in soup.find("ul",{"id":"_listUl"}).findChildren("li"): #hehe soup bowl
                # print(bowl)
                # print(bowl.find("span",{"class":"date"}))
                json = (
                    {"titleNo":comicid,
                     "type":typeOf,
                     "episodeNo":int(bowl.attrs["data-episode-no"]),
                     "episodeTitle":bowl.find("span",{"class":"subj"}).contents[0].content,
                     "thumbnailImageUrl":bowl.find("span",{"class":"thmb"}).contents[0],
                     "publishedDate":str(bowl.find("span",{"class":"date"}).contents[0]).replace("\n","").replace("\t",""),
                     "likeCount":strToInt(bowl.find("span",{"class":"like_area _likeitArea"}).contents[1])
                    }
                )
                # print(json)
                episodes.append(episode(json))
            return episodes
        else:
            wpPre = getWebPage(BASECOMICURLS[1]+str(comicid)+f"&page={page}")
            self.spamWait()
            wp    = getWebPage(wpPre[1]+f"&page={page}")[0]
            print(BASECOMICURLS[1]+str(comicid)+f"&page={page}")
            # print(wp)
            soup = bs4.BeautifulSoup(wp,"html.parser")
            episodes = []
            bowl:bs4.Tag
            # print(soup.find("li",{"class":"_episodeItem"}))
            for bowl in soup.find("ul",{"id":"_listUl"}).findChildren("li"): #hehe soup bowl
                # print(bowl)
                # print(bowl.find("span",{"class":"date"}))
                json = (
                    {"titleNo":comicid,
                     "type":typeOf,
                     "episodeNo":int(bowl.attrs["data-episode-no"]),
                     "episodeTitle":bowl.find("span",{"class":"subj"}).contents[0].content,
                     "thumbnailImageUrl":bowl.find("span",{"class":"thmb"}).contents[0],
                     "publishedDate":str(bowl.find("span",{"class":"date"}).contents[0]).replace("\n","").replace("\t",""),
                     "likeCount":strToInt(bowl.find("span",{"class":"like_area _likeitArea"}).contents[1])
                    }
                )
                # print(json)
                episodes.append(episode(json))
            return episodes

    def spamWait(self):
        """wait so that we dont spam webtoon"""
        if self.useWaitTimer:
            time.sleep(self.waitTime)
