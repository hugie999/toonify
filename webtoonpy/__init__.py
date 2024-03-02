"""a small lil' wrapper for the webtoon rapidapi api
remember to use a token and always practice safe requesting"""
#webtoon in python moment
#made with: https://rapidapi.com/apidojo/api/webtoon
#this is my first python module please be nice😥

import requests
import base64
import time
import bs4

__version__ = '0.0.3'
BASECOMICURLS = ["https://www.webtoons.com/en/canvas/barry-and-bobby/list?title_no=","https://www.webtoons.com/en/thriller/dead-but-not-gone/list?title_no="] #for scraping
"""base comic urls for scrapers [1] = canvas (barry and bobby) [2] = original (dead 🅱️ut not gone)"""
# def createComicJson(name:str,id:int,author:str) -> dict:
#     """allows creation of comic() classes without request json"""

def strToInt(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return int(float(x.replace('K', '')) * 1000)
        return 1000
    if 'M' in x:
        if len(x) > 1:
            return int(float(x.replace('M', '')) * 1000000)
        return 1000000
    if 'B' in x:
        return int(float(x.replace('B', '')) * 1000000000)
    return 0
"""THANK YOU SO F#CKING MUCH PERSON ON STACK OVERFLOW (link : https://stackoverflow.com/a/41028390"""


def loadImage(url:str) -> bytes:
    "this litterally returns a png so be prepared"
    newurl = "https://webtoon-phinf.pstatic.net/"+url
    #fuck you webtoon
    resp = requests.get(newurl,headers={'User-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Mi MIX 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36','Referer':'http://m.webtoons.com/'})# <- teh secret sauce
    return resp.content
def getWebPage(url,session:requests.Session) -> str:
    resp = session.get(url)
    return resp.content.decode()

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

class episode():
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
    def __init__(self) -> None:
        pass

#its up here cus it returns a header info (sorry for the inconsistant placeing)
class partialEpisode():
    def __init__(self,raw:dict,type:str,comicId) -> None:
        """basically just episode class but without the images"""
        self._json = raw
        self.parentID:int    = raw["titleNo"]
        self.type:str        = type
        assert type in ["canvas","originals"]
        self.episodeNO:int   = raw["episodeNo"] #i deadass put "136" here originally lmfao
        self.episodeName:str = raw["episodeTitle"]
        self.thumbnail:str   = raw["thumbnailImageUrl"]
    def __str__(self) -> str:
        return f"name: {self.episodeName}, no: {self.episodeNO}, parent: {self.parentID}"
    
    pass

class episodeList():
    def __init__(self,raw:dict,type) -> None:
        """its the uh... list of episodes"""
        self._json = raw
        self.type:str        = type
        assert type in ["canvas","originals"]
        self.totalEpisodes = raw["totalServiceEpisodeCount"]
        self.episodes:list[partialEpisode] = []
        
        for i in raw["episode"]:
            self.episodes.append(partialEpisode(i,type))
    def __str__(self) -> str:
        return str(self.episodes)

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
        
        self._partialEpisodeCache:list[partialEpisode] = []
        self._comicOriginalsCache:list[episode]        = []
        self._episodeCacheCanvas:list[episode]         = []
        # self._comicOriginalsCache:list[comic]        = []
        # self._episodeOriginalsCache:list               = []
        self._comicCanvasCache:list[comic]             = []
        # self._searchCache:list[search]               = []
        self._genresCache:dict                         = None
        self.listedOriginals                           = False
        if rawJson:
            for i in rawJson["parEpisode"]:
                self._partialEpisodeCache.append(partialEpisode(i))
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
    def addEpisodeToCache(self,episodes:list[episode]|episodeList):
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
    def __init__(self,lang="en",testMode=False,verbose=True) -> None:
        """creates a webtoon api class with your token and languedge (me when i cant spell)
        (testmode uses preset values for testing)"""
        # if not token:
        #     print("hey you need a token for this!\ntokens are here: https://rapidapi.com/apidojo/api/webtoon/details")
        # assert token
        self._latestresp:requests.Response = None
        self.token = None
        self.lang  = lang
        self.testmode = testMode
        self.verbose = verbose
        self.useWaitTimer = True
        self.waitTime     = 1
        
        self._requestsSession = requests.Session()
        # self._soup = bs4.BeautifulSoup()
        self.cache = webtoonCache()
        self._defaultheader = {}
        # self._defaultheader = {
        #     "X-RapidAPI-Key": token,
        #     "X-RapidAPI-Host": "webtoon.p.rapidapi.com"}
        self._defaulturl = "https://webtoon.p.rapidapi.com/"
    def getRequestAmount(self) -> headerInfo:
        return None
        """idfk what to name its how many requests you have used (cus its limuted)"""
        assert self._latestresp
        return headerInfo(int(self._latestresp.headers["X-RateLimit-Requests-Remaining"]),int(self._latestresp.headers["X-RateLimit-Requests-Limit"]))
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
        assert type in ["canvas","originals"]
        params = {"language": self.lang}
        # time.sleep(1)
        # return []
        if self.verbose:
            print("listComics...")
        # print(self.cache.listedCanvas and type == "canvas")
        # print(self.cache.listedOriginals and type == "originals")
        if ((not self.cache.listedOriginals) and type == "originals") or type == "canvas":
            resp = requests.get(self._defaulturl+type+"/titles/list", headers=self._defaultheader, params=params).json()["message"] #really good practice totally
            
            #trust me you dont want to print this
            # if self.verbose:
            #     print(resp)
            
            items = []
            for i in resp["result"]["titleList"]["titles"]:
                items.append(comic(i,type=type))
            self.cache.addComicToCache(items,type)
            if type == "canvas":
                self.cache.listedCanvas = True
            else:
                self.cache.listedOriginals = True
            out = items
            self._latestresp = resp
            if type == "canvas":
                self.cache._comicCanvasCache
            if self.verbose:
                print("done!")
            return out
        else:
            print("already fetched!")
            if type == "canvas":
                return self.cache._comicCanvasCache
            else:
                return self.cache._comicOriginalsCache
                
    
    def getComic(self,id:int|str|None=None,url:str|None="",type="canvas") -> comic:
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
            wp = getWebPage(BASECOMICURLS[0]+str(id),self._requestsSession)
            soup = bs4.BeautifulSoup(wp,"html.parser")
            comicName = soup.find("meta",{"property":"og:title"}).attrs["content"]
            comicAuthorRaw = soup.find("a",{"class":"author"})
            comicAuthor = {"name":comicAuthorRaw.contents[0],"link":comicAuthorRaw.attrs["href"]}
            thumbnailURL = soup.find("img").attrs["src"]
            episodeCount = soup.find("li",attrs={"class":"_episodeItem"}).attrs["data-episode-no"]
            pageCount    = 0 #class="pg_next"
            summary  = soup.find("a",attrs={"class","summary"})
            raitingsArea = soup.find("ul",attrs={"class":"grade_area"}).find_all("em",attrs={"class":"cnt"})
            print(raitingsArea[0])
            
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
            wp = getWebPage(BASECOMICURLS[1]+str(id),self._requestsSession)
            soup = bs4.BeautifulSoup(wp,"html.parser")
            comicName = soup.find("meta",{"property":"og:title"}).attrs["content"]
            comicAuthorRaw = soup.find("a",{"class":"author"})
            comicAuthor = {"name":comicAuthorRaw.contents[0],"link":comicAuthorRaw.attrs["href"]}
            thumbnailURL = soup.find("img").attrs["src"]
            episodeCount = soup.find("li",attrs={"class":"_episodeItem"}).attrs["data-episode-no"]
            pageCount    = 0 #class="pg_next"
            summary  = soup.find("a",attrs={"class","summary"})
            raitingsArea = soup.find("ul",attrs={"class":"grade_area"}).find_all("em",attrs={"class":"cnt"})
            print(raitingsArea[0])
            
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
    
    def loadFullEpisode(self,oldEpisode:partialEpisode) -> episode:
        

        params = {"titleNo":oldEpisode.parentID,"episodeNo":oldEpisode.episodeNO,"language":self.lang}

        resp = requests.get(self._defaulturl+oldEpisode.type+"/episodes/get-info", headers=self._defaultheader, params=params)
        self._latestresp = resp
        return episode(resp.json()["message"]["result"]["episodeInfo"],oldEpisode.parentID)
    
    def getEpisodes(self,comicToUse:comic|int,startIndex=0,size=20,typeOf:str="canvas"):
        """returns episodes (reminder that episodes are returned in reverse order (last to first) so be carefulas)
        (note: currently dosent support cacheing)"""
        assert size <= 20
        assert startIndex >= 0
        assert type(comicToUse) in [comic,int]
        assert typeOf in ["canvas","originals"]
        if type(comicToUse) == comic:
            comicid = comicToUse.id
            typeOf  = comicToUse.type
        else:
            comicid = comicToUse
        params = {"titleNo":comicid,"startIndex":startIndex,"language":self.lang,"pageSize":size}
        req = requests.get(self._defaulturl+typeOf+"/episodes/list",params,headers=self._defaultheader)
        self._latestresp = req
        epl = episodeList(req.json()["message"]["result"]["episodeList"],typeOf)
        self.cache.addEpisodeToCache(epl)
        try:
            return epl
        except KeyError:
            # print("error with json!:")
            # print(req.json())
            raise KeyError("error with json",req.json(),f"type: {typeOf}")
        # "Something went wrong, we know it and trying to fix this Rapidly" - rapidapi 2024

class webtoonapi():
    def __init__(self,token:str,lang="en",testMode=False,verbose=True) -> None:
        raise DeprecationWarning("this class has been deprecated!\nsome or all functions may not work")
        """creates a webtoon api class with your token and languedge (me when i cant spell)
        (testmode uses preset values for testing)"""
        # if not token:
        #     print("hey you need a token for this!\ntokens are here: https://rapidapi.com/apidojo/api/webtoon/details")
        assert token
        self._latestresp:requests.Response = None
        self.token = token
        self.lang  = lang
        self.testmode = testMode
        self.verbose = verbose
        self.cache = webtoonCache()
        self._defaultheader = {
            "X-RapidAPI-Key": token,
            "X-RapidAPI-Host": "webtoon.p.rapidapi.com"}
        self._defaulturl = "https://webtoon.p.rapidapi.com/"
    def getRequestAmount(self) -> headerInfo:
        """idfk what to name its how many requests you have used (cus its limuted)"""
        assert self._latestresp
        return headerInfo(int(self._latestresp.headers["X-RateLimit-Requests-Remaining"]),int(self._latestresp.headers["X-RateLimit-Requests-Limit"]))
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

    def listComics(self,type) -> list[comic]:
        """list EVERY comic in a type as a list
        please only use this if you know what your doing!"""
        assert not self.testmode
        assert type in ["canvas","originals"]
        params = {"language": self.lang}
        # time.sleep(1)
        # return []
        if self.verbose:
            print("listComics...")
        # print(self.cache.listedCanvas and type == "canvas")
        # print(self.cache.listedOriginals and type == "originals")
        if ((not self.cache.listedOriginals) and type == "originals") or type == "canvas":
            resp = requests.get(self._defaulturl+type+"/titles/list", headers=self._defaultheader, params=params).json()["message"] #really good practice totally
            
            #trust me you dont want to print this
            # if self.verbose:
            #     print(resp)
            
            items = []
            for i in resp["result"]["titleList"]["titles"]:
                items.append(comic(i,type=type))
            self.cache.addComicToCache(items,type)
            if type == "canvas":
                self.cache.listedCanvas = True
            else:
                self.cache.listedOriginals = True
            out = items
            self._latestresp = resp
            if type == "canvas":
                self.cache._comicCanvasCache
            if self.verbose:
                print("done!")
            return out
        else:
            print("already fetched!")
            if type == "canvas":
                return self.cache._comicCanvasCache
            else:
                return self.cache._comicOriginalsCache
                
    
    def getComic(self,id:int|str,type="canvas") -> comic:
        assert not self.testmode
        assert type in ["canvas","originals"]
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
    
    def loadFullEpisode(self,oldEpisode:partialEpisode) -> episode:
        

        params = {"titleNo":oldEpisode.parentID,"episodeNo":oldEpisode.episodeNO,"language":self.lang}

        resp = requests.get(self._defaulturl+oldEpisode.type+"/episodes/get-info", headers=self._defaultheader, params=params)
        self._latestresp = resp
        return episode(resp.json()["message"]["result"]["episodeInfo"],oldEpisode.parentID)
    
    def getEpisodes(self,comicToUse:comic|int,startIndex=0,size=20,typeOf:str="canvas"):
        """returns episodes (reminder that episodes are returned in reverse order (last to first) so be carefulas)
        (note: currently dosent support cacheing)"""
        assert size <= 20
        assert startIndex >= 0
        assert type(comicToUse) in [comic,int]
        assert typeOf in ["canvas","originals"]
        if type(comicToUse) == comic:
            comicid = comicToUse.id
            typeOf  = comicToUse.type
        else:
            comicid = comicToUse
        params = {"titleNo":comicid,"startIndex":startIndex,"language":self.lang,"pageSize":size}
        req = requests.get(self._defaulturl+typeOf+"/episodes/list",params,headers=self._defaultheader)
        self._latestresp = req
        epl = episodeList(req.json()["message"]["result"]["episodeList"],typeOf)
        self.cache.addEpisodeToCache(epl)
        try:
            return epl
        except KeyError:
            # print("error with json!:")
            # print(req.json())
            raise KeyError("error with json",req.json(),f"type: {typeOf}")
        # "Something went wrong, we know it and trying to fix this Rapidly" - rapidapi 2024

