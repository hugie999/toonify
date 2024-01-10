
# try:
#     assert sys.platform != "win32"
#     import pythonforandroid.logger as andlog
# except:
#     print("running on windows")
# else:
#     andlog.info("python for android loaded!")
import flet as ft
import sys
import base64 as b64
import webtoonpy as wtp
DEFAULTTEST = 300138
# wb = wtp.webtoonapi(tokeninput.value)
try:
    f = open("token")
    TOKEN = f.read()
    f.close()
except FileNotFoundError:
    TOKEN = False
def openInBrowser(link):
    pass

def readepisode(ep:wtp.episode,page:ft.Page,pep:wtp.partialEpisode):
    # def closealert():
    #     page.banner.open = False
    #     page.update()
    # alert = ft.Banner(bgcolor=ft.colors.AMBER_100,leading=ft.icons.WARNING_AMBER_SHARP,content=ft.Text("eyy broski this is EXPARIMENTLE so thare might be bugs"),actions=[ft.TextButton("oki",on_click=closealert)])
    # page.banner = alert
    # page.banner.open = True
    # page.update()
    pass

    
    images = []
    for i in ep.images:
        # imgb64 = i.imgb64
        img = b64.encodebytes(wtp.loadImage(i.url)).decode("ascii").replace("\n","") #yass
        images.append(ft.Image(src_base64=img,fit=ft.ImageFit.FIT_WIDTH))
        print(img)
        print(f"getting image: {i.order}")
    print(images)
    imagecol = ft.Column(images,scroll=ft.ScrollMode.ALWAYS,expand=True,alignment=ft.MainAxisAlignment.CENTER)
    print(imagecol.controls)
    sheet = ft.BottomSheet(ft.Column([ft.Text(pep.episodeName,size=30,weight=ft.FontWeight.BOLD,max_lines=1)],imagecol),
        open=True,
        show_drag_handle=True,
        enable_drag=True,
        is_scroll_controlled=True,
        use_safe_area=True,
        )
    page.overlay.append(sheet)
    sheet.open
    page.update()
    

def genEpisodesheet(epname,imgb64:str,ep:wtp.partialEpisode,wb:wtp.webtoonapi) -> ft.BottomSheet:
    def readclick(e:ft.ControlEvent):
        epf = wb.loadFullEpisode(ep)
        readepisode(epf,e.page,ep)
    if imgb64:
        sheet = ft.BottomSheet(ft.Container(ft.Column([
            ft.Text(epname,size=30,weight=ft.FontWeight.BOLD,max_lines=1),
            ft.Row([ft.Image(src_base64=imgb64,fit=ft.ImageFit.CONTAIN)],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.TextButton("view in browser",icon=ft.icons.OPEN_IN_BROWSER_OUTLINED,on_click=lambda a:openInBrowser("")),
            ft.ElevatedButton("read",icon=ft.icons.READ_MORE_OUTLINED,on_click=readclick)])
        ],tight=True,scroll=ft.ScrollMode.ADAPTIVE),padding=10),
        open=True,
        show_drag_handle=True,
        enable_drag=True,
        is_scroll_controlled=True)
    else:
        sheet = ft.BottomSheet(ft.Container(ft.Column([
            ft.Text(epname),
            ft.Image(src='icon.png')
        ],tight=True),padding=10),
        open=True,
        show_drag_handle=True,
        enable_drag=True,
        is_scroll_controlled=True)
    return sheet

def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text(f"webtoon api: {wtp.__version__}")))
    page.title = "webtoon test"
    if TOKEN:
        tokeninput = ft.TextField(label="token:",enable_suggestions=False,hint_text="1234567890abcdefghijklmnopqrstuvwxyz",icon=ft.icons.ABC_OUTLINED,password=True,can_reveal_password=False,value=TOKEN,read_only=True)
    else:
        tokeninput = ft.TextField(label="token:",enable_suggestions=False,hint_text="token",icon=ft.icons.ABC_OUTLINED,password=True,can_reveal_password=True)
    comicidinput = ft.TextField(label="comic id:",value="300138",enable_suggestions=False,hint_text="0000000000",icon=ft.icons.BOOK_OUTLINED,input_filter=ft.NumbersOnlyInputFilter())
    episodeidinput = ft.TextField(label="episode id:",value="0",enable_suggestions=False,hint_text="000",icon=ft.icons.NUMBERS_ROUNDED,input_filter=ft.NumbersOnlyInputFilter())
    
    def testbuttonaccept(e):
        pr = ft.ProgressRing()
        page.add(pr)#ft.Column([ft.Row([pr],vertical_alignment=ft.CrossAxisAlignment.CENTER)],horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        print("a")
        
        wb = wtp.webtoonapi(tokeninput.value)
        ep = wb.getEpisodes(comicToUse=int(comicidinput.value),startIndex=int(episodeidinput.value),size=1)
        print(ep)
        print(ep.episodes[0].episodeName)
        eps = ep.episodes[0]
        page.add(ft.Text(eps.episodeName))
        img = b64.encodebytes(wtp.loadImage(eps._json["thumbnailImageUrl"])).decode("ascii").replace("\n","") #yass
        print(img)
        page.add(ft.Image(src_base64=(img)))
        c = genEpisodesheet(eps.episodeName,img,eps,wb=wb)
        pr.visible = False
        page.overlay.append(c)
        page.update()
        c.open = True
        c.update()
    

    page.add(tokeninput,ft.Row([comicidinput,episodeidinput,ft.TextButton("submit",on_click=testbuttonaccept)],scroll=ft.ScrollMode.ADAPTIVE))
    # page.add(ft.Card(ft.Text("hi")))
ft.app(main)
