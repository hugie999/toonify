"""a small lil' wrapper for the webtoon rapidapi api
remember to use a token and always practice safe requesting"""
#webtoon in python moment
#made with: https://rapidapi.com/apidojo/api/webtoon
#this is my first python module please be nice😥

import requests
import base64

__version__ = '0.0.2'

def loadImage(url:str) -> bytes:
    "this litterally returns a png so be prepared"
    newurl = "https://webtoon-phinf.pstatic.net/"+url
    #fuck you webtoon
    resp = requests.get(newurl,headers={'User-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Mi MIX 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36','Referer':'http://m.webtoons.com/'})# <- teh secret sauce
    return resp.content

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
    
class episode():
    def __init__(self,raw:dict) -> None:
        """its like the other episode class but with images
        raw should start from 'episodeInfo'"""
        self.no = raw["episodeSeq"]
        self.author = raw["writingAuthorName"]
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
        (idfk why i named it headerInfo lmfao😁🤷‍♂️😈🗿🗿😘😥😓
        well i mean i do know im just not saying it😎😎😎😎😎 #slay)"""
        self.requestsUsed = total-remaining
        self.remaining = remaining
        self.totalAvalible = total
    def __str__(self) -> str:
        return f"headerInfo -> (used: {self.requestsUsed}, remaining: {self.remaining}, avalible: {self.totalAvalible}) <-"

#its up here cus it returns a header info (sorry for the inconsistant placeing)
class partialEpisode():
    def __init__(self,raw:dict,type:str) -> None:
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
    def __init__(self,json:dict,type="canvas") -> None:
        """yes i know they are called webtoons or webcomics but it would get cofuseing fast if i had a webtoon and webtoonapi class ok?
        protip: just like most of the other classes this one shouldnt be made by your code"""
        self._json      = json
        """its literally just the raw json"""
        self.name       = json["title"]
        self.id         = json["titleNo"]
        """the cooler self.name"""
        self.author     = json["writingAuthorName"]
        self.previewImg = json["thumbnail"]
        "the thumbnail for the comic (use loadImage() to load this!)"
        try:
            self.isNSFW     = json["ageGradeNotice"]
            """'un actually its called ageGradeNotice🤓'"""
        except KeyError:
            self.isNSFW = None #should really just make a partialComic class
        self.type       = type
        assert type in ["canvas","originals"]
        """either 'canvas' or originals"""
        self.epNum = json["totalServiceEpisodeCount"]
    def __str__(self) -> str:
        return f"name: {self.name}, id: {self.id}, author:{self.author}"
class search():
    def __init__(self,query:str,start=0,size=20,lang="en",type="canvas",total=0,items:list[comic]=[],output={}) -> None:
        """search class that represents a search on webtoon (no duh) 
        (this shouldnt be made in your code only by webtoonapi() if you are makeing this then you should really consifer what choices lead up to this)"""
        self.type  = type
        assert type in ["canvas","originals"]
        self.query = query
        self.start = start
        self.size  = size
        self._rawOutput = output
        self.total  = total
        self.items = items
    def __str__(self) -> str:
        return self._rawOutput
    
class webtoonapi():
    def __init__(self,token:str,lang="en",testMode=False,verbose=True) -> None:
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
        self._defaultheader = {
            "X-RapidAPI-Key": token,
            "X-RapidAPI-Host": "webtoon.p.rapidapi.com"}
        self._defaulturl = "https://webtoon.p.rapidapi.com/"
    def getRequestAmount(self) -> headerInfo:
        """idfk what to name its how many requests you have used (cus its limuted)"""
        assert self._latestresp
        return headerInfo(self._latestresp.headers["X-RateLimit-Requests-Remaining"],self._latestresp.headers["X-RateLimit-Requests-Limit"])
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
        if self.verbose:
            print("listComics...")
        resp = requests.get(self._defaulturl+type+"/titles/list", headers=self._defaultheader, params=params).json()["message"] #really good practice totally
        
        #trust me you dont want to print this
        # if self.verbose:
        #     print(resp)
        
        items = []
        for i in resp["result"]["titleList"]["titles"]:
            items.append(comic(i,type=type))
        out = items
        self._latestresp = resp
        if self.verbose:
            print("done!")
        return out
    
    def getComic(self,id:int,type="canvas") -> comic:
        assert not self.testmode
        assert type in ["canvas","originals"]
        
        resp = requests.get(self._defaulturl+type+"/titles/get-info",{"titleNo":id,"language":self.lang},headers=self._defaultheader).json()["message"]
        print(resp)
        return comic(resp["result"]["titleInfo"])
    
    def loadFullEpisode(self,oldEpisode:partialEpisode) -> episode:
        

        params = {"titleNo":oldEpisode.parentID,"episodeNo":oldEpisode.episodeNO,"language":self.lang}

        resp = requests.get(self._defaulturl+oldEpisode.type+"/episodes/get-info", headers=self._defaultheader, params=params)
        self._latestresp = resp
        return episode(resp.json()["message"]["result"]["episodeInfo"])
    
    def getEpisodes(self,comicToUse:[comic,int],startIndex=0,size=20,typeOf:str="canvas"):
        """returns episodes (reminder that episodes are returned in reverse order (last to first) so be carefulas)"""
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
        try:
            return episodeList(req.json()["message"]["result"]["episodeList"],typeOf)
        except KeyError:
            # print("error with json!:")
            # print(req.json())
            raise KeyError("error with json",req.json(),f"type: {typeOf}")
        # "Something went wrong, we know it and trying to fix this Rapidly" - rapidapi 2024

