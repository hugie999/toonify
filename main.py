import flet as ft
import webtoonpy as wtp
import base64 as b64
DEFAULTTEST = 300138
try:
    f = open("token")
    TOKEN = f.read()
    f.close()
except FileNotFoundError:
    TOKEN = False
def openInBrowser(link):
    pass

def genEpisodesheet(epname,imgb64:str,ep:wtp.episode) -> ft.BottomSheet:
    if imgb64:
        sheet = ft.BottomSheet(ft.Container(ft.Column([
            ft.Text(epname,size=30,weight=ft.FontWeight.BOLD,max_lines=1),
            ft.Row([ft.Image(src_base64=imgb64,fit=ft.ImageFit.FIT_HEIGHT,width=500)],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.TextButton("view in browser",icon=ft.icons.OPEN_IN_BROWSER_OUTLINED,on_click=lambda a:openInBrowser("")),
            ft.ElevatedButton("read",icon=ft.icons.READ_MORE_OUTLINED)])
        ],tight=True),padding=10),
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
        c = genEpisodesheet(eps.episodeName,img)
        pr.visible = False
        page.overlay.append(c)
        page.update()
        c.open = True
        c.update()
    

    page.add(tokeninput,ft.Row([comicidinput,episodeidinput,ft.TextButton("submit",on_click=testbuttonaccept)]))
    # page.add(ft.Card(ft.Text("hi")))
ft.app(main)
