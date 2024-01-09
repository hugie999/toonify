import flet as ft
import webtoonpy as wtp
import base64 as b64
DEFAULTTEST = 300138

def main(page: ft.Page):
    page.add(ft.SafeArea(ft.Text(f"webtoon api: {wtp.__version__}")))
    page.title = "webtoon test"
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
        
        pr.visible = False
        page.update()
    

    page.add(tokeninput,ft.Row([comicidinput,episodeidinput,ft.TextButton("submit",on_click=testbuttonaccept)]))
    # page.add(ft.Card(ft.Text("hi")))
ft.app(main)
