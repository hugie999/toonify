
import flet as ft
import flet.version #why is this its own liberary
import sys
import time
import base64 as b64
import webtoonpy as wtp
import flet_navigator as fletnav #flet navigator
import time #mainly used for debuging (fake loading times)
print("====>app start<====")
print(f"flet version           : {flet.version.version}")
print(f"flet navigator version : {fletnav.FLET_NAVIGATOR_VERSION}")
imgs = ["iVBORw0KGgoAAAANSUhEUgAAAqsAAAGACAMAAAC9RturAAADAFBMVEX///8AAAC6urqvr6+CgoJKSkoUFBTa2tqioqJqamoyMjL29vYEBATCwsLo6OjMzMzAwMC0tLS3t7fDw8PZ2dn5+fmKioqGhoZZWVk5OTkcHBwQEBAFBQUPDw8bGxs2NjZVVVV/f3+4uLjx8fHs7Ozn5+fp6en9/f3ExMR7e3tNTU0kJCQSEhIJCQkWFhYoKChRUVF+fn7Gxsb+/v7j4+OUlJRgYGAzMzMZGRkLCwsDAwM4ODhlZWWfn5/q6uqPj4+Li4vV1dWHh4c+Pj4RERErKytra2txcXEGBgYKCgqampqzs7NWVlalpaX6+vpCQkL19fWNjY0eHh6SkpK1tbU8PDwBAQHS0tL09PTBwcFERESWlpb7+/tnZ2eTk5OoqKgpKSmXl5dTU1Pz8/PY2Njh4eE/Pz8lJSXg4OBsbGzQ0NDf3983NzfW1tZeXl6dnZ3IyMi5ublaWlovLy8HBweqqqq7u7sTExMNDQ1mZmbb29ukpKQCAgIaGhoICAj39/esrKzPz8/Ozs7Hx8dAQECMjIzX19fu7u5JSUlvb2/FxcUnJydoaGiJiYmjo6N1dXU1NTVMTEybm5uIiIgVFRWwsLB9fX3c3Nzt7e0jIyNhYWHm5uZycnK9vb16enre3t5YWFhdXV1ubm6QkJDw8PD8/PycnJwYGBhDQ0OYmJjKyspLS0tzc3OEhISAgIAODg7Nzc09PT1FRUUmJiZiYmIMDAwiIiLd3d2Ojo5QUFDLy8tGRkYxMTF2dnZHR0ctLS2ZmZkhISGenp6tra13d3fy8vK/v79XV1ehoaGxsbGVlZWurq40NDRjY2P4+PhkZGTr6+uBgYEfHx9SUlKysrJpaWltbW2np6fv7+98fHzU1NR5eXlcXFzi4uJUVFRBQUFfX19PT09bW1s7OzsuLi4qKiq2trbl5eWrq6sgICDT09OgoKAdHR2RkZFISEhwcHAsLCx0dHSpqakXFxeFhYV4eHg6OjqDg4O+vr4wMDDR0dG8vLympqZOTk7Jycnk5OTPBksDAAAVVklEQVR4nO3dCXwU5f3H8fmBUoWgeKKYUDwgWglqAyJBEUrUIKIUJAWNF6CigAUaDNoQz6ISlSIqIF5FgketRyXUPyoUz6qAaNUiXmitt/5Raj3a/zG78zwzOzPP7G6SXZINn/frpTt5rnk282WyMzs7a1kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0DgizT0DhLWRmLbNPY2WJfYrae45IGQ7shpGVluk7cmqAVFtidqRVeSGHwlZRW7YgawiR+xIVpEj2pNV5IYOeWQVuaGj5FRWd9q50y677rb7Hs09DzSDPdPJaodOnffau8s++fkFXX/cbd/99o9qd0D3uB7658IDD/rJwT3zi3odcuhhPy0ONO7d5/C+R/Qr6de1/5FHDTCNdvTAuKP1z4N+NrhUzbbkmGPbFKb5DJH7jiuIKVNbf0iBcnywXfHQE4aIT/72w040DnmSSpLz0/Cfd03sNWJkYqeTR5Un1JV0+0V4tF6qcnT8pzGn+CchI06taPLvALnhNDE6PdDsjDNNrUacZdqtjVW142I/HDgi2OmQ8brh2ecE6/IOCw14rqqaYC93OM8wiWPOz+gvBC1WWlmdGNybuSZNDg95garrbi//siTcZ58pTrup+xgGnBYM669UhZ3I/fc2zqFyelZ+M2hp0snqhVVRURWZMTQ05EWq6mLL+nW1qc/MnWLN9qsxDnhQYLRJqryjdckkYweR6mHZ+/2g5Ugjq5fmRUfVDsoZwSGPVTWXWZeXmfuMtVv9oihivMv9o41S5SdbR0bOofIK01PjwpNWJnVWd/Gimnflb8bMumrA5I6/udo70MpvExjyGlUxe3Rt/LHrtdddP2zknN96LwfKd7bGOXVlcw87a/oN87rd6K36av9oV6riM25yHg+5+ab5CyqGn73rnIRjtoUdws8sVp7xXxeand7shnNWFxe4e7xbFnnFB8xx03rjIn+PW1X5bbfH/t+3kz5NdcedbrZ+Zy2OPcy4a4mqq1t6txvk+b7R7lHF98YPsn7Vyaup6DPDHTD4ysEiq61VdFbr2us43H2fv2Z+ra75vb/iflV8VuwF6R/qEmoe0D0efCi2s364d0LdHe4Jg86+0f6oSh+J/W9Zna9uchfdp/6A8JMiqq1SdFbv0mlY/qdg1VXuYfl+vvI5qrSn/d+j/i7/5e6L7f8mjfPVrdCnWkf5ih8Tz+HBKUyu11UPpP9kkdMis7q/fgVQPz/cq8dMVfm4r/gJL1znBXpcnhC8uxcEKrdXFUW+s/srvR6rLglN4c+6bnXwDTG0UpFZ7ayz8KSp21O6dkxi6dNuuGY+E+yR8JbCDsG6YbpmUGJpQlafDc+g7hBdeWDqZ4nWICqrhXrPOdjc77eq+rnEQi+rfwl1ONat6xuq666rnk8s9bL6mGkGfXSt4egKrVFUVtsY4+PRu8J+ieeM3KwWhP9mL3WT1yc8mj4V8EJioZfVF00zWKDPhK1J+gTRakRlda0qPzji1eC6ekNHN6svhTuM0XV568OVD6u6lxML3axWmS9S0Z3y1yV5fmg9orL6iio/LqrjX1WDxQllblYNZ2vn67r+hsH0+df7EwvdrD5n6GG7XdeviJojWpWIrLrJejWq40jVoH1CmZvVCeH2C3TdtYbBXlN1rycWulm9wTyD53W98egPrU5EVv+mc7AhquN9qkFJwl9gndVSQ/s99Ij3Gir1iVlfjt2sRlz6t7uuvzlqjmhVIrL6hiquiuw4Wp/A3+iV6az+1tC+UCcreBFBzJuq7rTEQp3V6vCBWlyFvpTrrchJojWJyKq+anpV6p6XekU6q/eY2uusTjHUHZQsqwujZnB3stWh1YnIan9VvDK6p27yG69IZ/VQU3ud1UGGuqRZfThqBo+rBo9HNUCrEpFVfRogDU97vXRWLzCtSbd/21CXNKvvRM39XdVgRAOer286jemHZhORVffKkNRu8XrprG4yrUm3722oS5rV16Lm/p5qEP2iOkrC9BvcF80lIquGD0tFGev1yk5W7zd0iDtBNZiR/tNNnAiBzTHmrNalH1WZ63XLTlZvj5r7+6pBZQOerzGqBDYnmLN6YgOy+kevW3ay+rKhQ5z+2GxZA55vqmfTgKGwlUW8BihPukF9rvR6beWs7qUa1Kf9bEOZJK05JCKrlar4J8+mdJnXKztZfSNq7t1Ug57pPtmIOBLW3BCRVX1fgGkNGmwrH1tdrRp0SXN6ScNIWlu8iKzqq/jnmntFyE5W10at7u+qwQdpTi91EIlrSxaRVX2aPeJTARGyk1Xju2Ax/1ANroxqYJhAWo0Ia4sUkdVNqviRBg2WnaxGXvev74p1Z1qTSzOCZLXFisjqPFVcPbohg2Unq+0i1jZaj/hmOnNLP4GEtYWKyOpQnYOfNmSw7GRVdjKvzf0Yd8S12Ia1p9GwwY2xtURktYfOwQvmbmZZyuqH5rX9uiH/nhqWPrLaEkV93kqfCDilIYNlKatPG3rY9O2DS4annllDw0dYW6CorC5W5dUfNWCwLGU14pzUB6o6yfXg/pWn0a6x7bEVRGX1QB2U6yI6Fr9507hgWZayKoZbaFvW2bo28qO2gXWnbtakHsg2ndWPA+XFn6iKKsN9+GJ2ESl7d89PfWXZyuqOpvG207X7mWoN607dLDTbBnVBlul7Q34WrPi5jsKRxn6XqPtadkm832W2slozMdylg76J0Y3m74QJrTplq6b3QVbpLzvZN1gxTn+XVPmupn7LVO3niUnJVlbl6vDdX9zd6uJQlXnNKZuZejW0E7Kor9ri4dubfaHD8ODsUF2h+xU+RycWZy2r4furzc5XNdU/Sv4ErcamrnEJR/Z8qTZ5XmiT1+mPiUpR8MYmH+nbo8shvtv1Zyer8e8O+m//X/rZeq+fxhusjc0cWW1h3Nv6bL7YKahzv+t09wfd3dq7CTfrt96+3f3CgLwVxsE2mdbU6Kx+sTqe2F291wHDX3a/5mWI4XZEphWnbJXJjsiKF9085t1z6wNPTOtb492X99WErww6+LwdZs+af37Hv3zVP+EzAwP9g2Unq3e1dR4X3t920PrhC2Zdeq27Uw3d6j1qvSlbZbYnsqFD6Cv8Eu4h/XWKj7MGP12SnawOtF6PnEHkvQMC603dLMNdkQW3Bjd/4v3Op/ZMktS8gcGxspPVedaJh0ZM4Z7Ub682JW9ktWV5ZnWSrFoT/ihRasO3Pc1OVjvbL6JfMk5hr4i7soXWmrJZFjoj8y7bkiSrlvXxKmNMRow0fGFfdrL6z9gPbY8ITaHd0jSeXZPSRlZbmokrfRHYLVg/9a2CQEoeHDvM+GZRdrL6h/hPl5z1D98cRmy3xDCQcaVptEvSm6y2KFO+6d+1pqRf1zXdDnuxh6F+j9mPXjD4k9LKkhlHnDv4tC+e3cPQJvP8WbXN77P2X10K8sp6/uO97WYHv8HdjKxia9BZ/bYJYzQxa2QVaclAVpueNaKKNLSIrAJpyFBWMzchIELTs8puFVsHWUWuyExWMzghIAJZRa4gq8gVZBW5gqwiV5BV5IqMvBeQuekAkTJx7QqwNZBV5AqyilxBVpEryCoAAAAAAAAAAAAAAAAAAAAAAI1U/I5U3WFZC6Xf1l5zrVQ2eYxJIim/Tii0nk9F3m/ympM4S8qnZ3P8bdYbUvKdRVYz6jQp2jmrK9g2fVctb8Yer3lu09Zeda5k9Yx9JzawaYdaOXd0A9aAdAwfIbVb54uBwnIlq8uD31qXuulskfMasAakY1+R55tr3TmS1UWhb1hMo2k3KdmY/iqQhg31sqbZVp4jWf06/ax6TSeXp/PN3GiAeSI7OEvq2OoQ+d565tvN/UrXvFBoWeMvWl65z5Vtdese3466Mb/ok3e8PfGY57pUHvHlq1ZFufzEKSk8450RNf2Wv7VrcFVbZLP1TOf2PStfueB8p8TNUHjcdS+csiW/YO89n7FSjGpntaLwqHO25Pfa/mRdtsfxc7vW9Htl7PV1gfV0emdm2ZZzji/0shocd6H0tX5YWSreC1T9pZxHhZt3byf1bzutfsiTzzf4mj4mJWm/ykU6zpQh6puBVVbbyyMLjnF+5YdbU+udpdOdJkNnqI0hh6ovaT1M/XzRepHn4iUfrdFtfj/Ov6rlMmKR+qLVEue7gHWGwuOOX6gKujyUYtRJUtJhrqrr7BRtXK4br5rgW892qviUh3RWQ+NuljM/2sf+0ZzVYPOn7IV4o8JJUn6bP9bXc2uOzJpsx0Mtqqz+WD5/rt3IHy7fs1JkaOnjHw+afa1IfXzLjC+S6q9m33FfnxtF5sT7XCpS+cCgj9oMlvvV1n/GDtnYMeu7f3iSyGP+dT0iVXOLbr1t44V7iVTH96wqQ+Fx198t5bd8uPPzJ4hU9U4+6iR5cMf8xZ0GfbfMHvWOWMmiKpFpY3p0/7cd4YWjE9bzqsiQPecvuOyJ/KsjZ9tePnldRr3+kvddtYUVi0X+XVFRbGq+SeRvsccvRI7zNbWsJfnyeBO2DIJOFflCLaqs2vup+vGxBfvVQX774bEle5u/Gns8UuSgeNP5+TJkXWzhTJH/xB7rxparrX+syDfxNoXvqDpXrUj51PjSeSJ/dUoqzeMu07vyb0ReSj6qPd+8/eJLdm4Gxh7vFLndqbP/UdycsJ5VIi/Gy/8mkbP9sfQsPTXwS7pGvwgNN9//Fem1wLJ6z5DN63xN40OVb7CQMYeLTFGLblZVcOxdrlwYXzpe5LrY4wPv9f+T0/Yxkfus+CHKKqdg/Qxn6y8ZIqvVi8TeefKwb112Vsc6SwvypWa45WYoNO5VNXKw8+XW+5fJ58VJR7Xne62ztKvIBfZDj3zZsk41LpeZxe56Zon9gtnRP3K2k0I7bi+Apml0qrZfKln/I2Xn+5rG2PvYqcGh0Hh7i+h/+15W74v/PFyknxOYqeK8W+CxdzAf2g9LRZ5QJS85W/95/Vfc9i8pGZ7Yyc7qdLcqvpLQ8bka9yaRxapk/R4pRrXnu5uzZP/jih3eTRdZpiv7iuzurueX8b/TcddFztYe7vrA78gNoHEaX9l/9T8WmedvGvOC+zofmTBTCvSil9Ul8Z+L3d1QR5H7/d3sV6dD7Yc5Ip+pkmHO1rePteZNVKaJXJHYqdY7Ylnm/AkNZVWNu6/IWYnFyUa153uAs/S2yEr74XbvZU3sZcFT7nrmeKOeHDlbe7hZwV+SDqBxGutWycIj5OFCf9OYD0W+Cg6FxiuS1XrRy2qFUyAyyVnYTWf1kif/eu6D1c6xbixTLzm7QdUmtvVfEx/fuwx2VtUpBx0bndXguDt6e+C4ZKN651d7O1m9SORrXWnv9I5317PWG/V/I2c7yftD49IBNE/jhzKRGRMDTWOuEFkbHAqNVy7H6MXUWd24OraJKquqqoqcTNk7l9tU7184W3+Tf3P6/pzWSp5evFnkaMvNamjcTYE8Jhs1lNX3Ezq/IXKXu55pXsX5kbM1vbWgA2ieRp19yNa/ONBU/Ur2Cg6FxmtIVoe/InJSm/jJefW3+haR/VTvA52tf17CTi3I3q/qTWrvV/9s6QyFx7X3q2ck9kw2qmm/6na2x1vqrmeZt1+dHTnbZFk1T+Ofsdw+Gmga8wNZzaiGvAY4SuQcdRh8mpOpa7wTSF87W//bJMcTdlYHqEUVGydD4XHt16s/T+yZbNRQVtU+O07tY531HOe9Xo2ebbKsGqdxWZmc8JjUbPQ3jeE1QGZ1NR1bRWTVPkj/tWq7xsnUFyIPqJJrna1/snPeyMjO6ndq8e8in1o6Q+FxbxJ5S5VMGTq0Q9JRQ1l9MaHxZpGz3fWcKnKNKv8mcrbJsmqaxrrN0m7AhHr5/kRf0xiOrTLrX6ZzVhFZtXeGuzgFF6oji44ig52SDaXO1h9XLwV6wFOnX+VbV617JmpDvpRWWAl/mwPjXlUjpc5bnnVVMqQi6aihrNqdq9RZrfEitZa7nhUiZzrldQdHzjYiq/F/ZKZpfBV/4+p0/SbBNd6/x9i/jT7BodB4t5jeC4jI6sv6/aBBW2aK3GAv1LUT6RgrKZyWr94JWixyp3P+Zmi1ukJAs7Na9Gl86Sv119HJUHjc2FsUr8WLOotsSj5qKKux431nf1axUqVFHcN9IjIsXvEziZytKatv6h1/uHnHannPfigeJdUH+ppa8dy2CQ6FxrtXZKRaTJnVT8ulcuTbC1bMKfrefr23d++r4ufUS/tMHPDdKfKHhHfYRz01/+IL15ZI/QTfumplxuCej84acNlrIjUTnZJK87gDetm5u3TKi93KpbR38lHDWT3ATvxeu+10dlv7j8aoOm891pMiZd9cMejkO+WWyNmasnq8yKoPx3Q0NB+3WkoXxZrsXiPLxyU2jQ9VvqQRmwQRxoeuXUlyzkpfRvTBRxsK7Ie+9p7rUKekuvMsfeXS/7mXIo34wb+uWhlyx7lOVWVbVVJpHteavFqVdVmRYtRwVq2La3Xj7Zckrid2fiHu6u76qrDQuKasLojNKt4h2HytuqYqfvXEMl/T2NvDXLuSUccErwlM9l7ApfeU5h9x0g3rLOvf39f0ih2oFH/2bs/KT96fEnuzXR0OFU/vNqKo38Fffhb8vFGt1Fj7x69fXbu7LqmMGNda1+eeXvkF/efpPVPkqIasWicu/f3MsvqFv9N/gt33x4bO3ZLf68qlhXXV+mrb4LjGS7f/d9SMIecODDcfKvKlalJnp/gmX9P/iPwzNBKaYKB7rXXTrNCvMKNl4lMAOWSllExI3QrpW5Khz7B87Z2+irJtZXV8eeAgEE32clM+G3j64aPUh0wu8C4NiLJtZfUEyZvc3HNobTq80oTPXJ+gL3adkidbUo2yTWV1tvfGAzLm2Wp5urF9N9aITJs6/r6XZ4g8marxtpTVDrXyCPeyyLybpeS21K3MXlUfHpTqzinbbktZPU2KHmruObRGsXuv/amxnRcdtKagpOCD10MXKIdtQ1m9l3uvAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQPP4fbQjrjzvFSuwAAAAASUVORK5CYII="]
#above is the test image
#github desktop hates him for he spoke the truth

token = ""              #token value
closeAppForReal = False #used at home screen to check wether to close the app
DEFAULTTEST = 300138    #default value in debug page
preferences = {"themeM2":False}        #to be used later
webtoonapi:wtp.webtoonapi = None
def saveCache(page:ft.Page):
    page.client_storage.set("ca.hugie999.toonify.storedcache",webtoonapi.cache.serialise())
# wb = wtp.webtoonapi(tokeninput.value)

def openInBrowser(link):
    pass

def loadAsB64(url:str) -> str:
    return b64.encodebytes(wtp.loadImage(url)).decode('ascii').replace("\n","")

def readepisode(ep:wtp.episode,page:fletnav.PageData,pep:wtp.partialEpisode,progress:ft.ProgressRing):
    # def closealert():
    #     page.banner.open = False
    #     page.update()
    # alert = ft.Banner(bgcolor=ft.colors.AMBER_100,leading=ft.icons.WARNING_AMBER_SHARP,content=ft.Text("eyy broski this is EXPARIMENTLE so thare might be bugs"),actions=[ft.TextButton("oki",on_click=closealert)])
    # page.banner = alert
    # page.banner.open = True
    # page.update()
    
    # exitbutton = ft.Row([ft.ElevatedButton("exit",expand=True,on_click=exitEpisode)],expand=True)
    pass
    # view = ft.View("/read",[ft.Text("original images copyright to respective authors")],scroll=ft.ScrollMode.ADAPTIVE)#,scroll=ft.ScrollMode.ALWAYS)
    images = []
    # images = ft.Column([],scroll=ft.ScrollMode.ALWAYS,spacing=0,alignment=ft.MainAxisAlignment.CENTER)
    progress.value = 0
    for i in ep.images:
        # imgb64 = i.imgb64
        img = imgs[0]
        #testing image
        print(i.url)
        img = b64.encodebytes(wtp.loadImage(i.url)).decode("ascii").replace("\n","") #yass
        # images.append(ft.Image(src_base64=img,fit=ft.ImageFit.FIT_WIDTH,expand=True))#,width=page.width,height=page.height))#,width=300))
        images.append(img)
        # print(img)
        print(f"getting image: {i.order}")
        progress.value += 1.0/len(ep.images)
        progress.update()
    progress.value = None
    # print(images)
    # view.controls.append(images)
    # view.controls.append(exitbutton)
    # print(view.controls)

    # imagecol = ft.Column(images,scroll=ft.ScrollMode.ALWAYS,expand=True,alignment=ft.MainAxisAlignment.CENTER)
    
    # print(imagecol.controls)

    # sheet = ft.BottomSheet(ft.Column([ft.Text(pep.episodeName,size=30,weight=ft.FontWeight.BOLD,max_lines=1)]+images,expand=True,scroll=ft.ScrollMode.ADAPTIVE),
    #     open=True,
    #     show_drag_handle=True,
    #     enable_drag=True,
    #     is_scroll_controlled=True,
    #     use_safe_area=True,
    #     maintain_bottom_view_insets_padding=True
    #     )
    # page.overlay.append(sheet)
    # sheet.open
    # sheet.expand = True

    # imagecol.update()
    # view.floating_action_button = ft.FloatingActionButton(icon=ft.icons.EXIT_TO_APP_OUTLINED,on_click=exitEpisode,tooltip="exit the episode")
    page.navigator.navigate("/read",page.page,args=[images])
    # page.go("/read")
    # page.update()
    # images.update()
    # view.appbar = ft.AppBar(title=pep.episodeName,center_title=False,leading=ft.icons.PAGEVIEW_OUTLINED,leading_width=40,bgcolor=ft.colors.SURFACE_TINT,actions=[])
    # view.update()
    
def genEpisodesheet(epname,imgb64:str,ep:wtp.partialEpisode,wb:wtp.webtoonapi,naviPage:fletnav.PageData) -> ft.BottomSheet:
    def readclick(e:ft.ControlEvent):
        prg = ft.ProgressRing()
        sheet.content.content.controls[2].controls.append(prg)
        sheet.update()
        epf = wb.loadFullEpisode(ep)

        readepisode(epf,naviPage,ep,prg)
        prg.visible=False
        sheet.open = False
        # sheet.update()
    if imgb64:
        sheet = ft.BottomSheet(ft.Container(ft.Column([
            ft.Text(epname,size=30,weight=ft.FontWeight.BOLD,max_lines=1),
            ft.Image(src_base64=imgb64,fit=ft.ImageFit.SCALE_DOWN),#,alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.TextButton("view in browser",icon=ft.icons.OPEN_IN_BROWSER_OUTLINED,on_click=lambda a:openInBrowser("")),
            ft.OutlinedButton("read",icon=ft.icons.READ_MORE_OUTLINED,on_click=readclick)])
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
    
    # print(f"used: {wb.getRequestAmount().requestsUsed})")#/{wb.getRequestAmount().totalAvalible}")
    return sheet

def genComicsheet(com:wtp.comic,wtb:wtp.webtoonapi,naviPage:fletnav.PageData) -> ft.BottomSheet:
    print(type(com))
    print(com.id)
    print(com.epNum)
    epnumpicker = ft.TextField(hint_text="001",value="",label="episode:",input_filter=ft.NumbersOnlyInputFilter())
    def readclick(e:ft.ControlEvent):
        prg = ft.ProgressRing()
        sheet.content.content.controls[2].controls.append(prg)
        
        sheet.update()
        print(f"total: {com.epNum}")
        print(f"ep   : {(com.epNum)-int(epnumpicker.value)}")
        print(f"rawep: {epnumpicker.value}")
        ep = wtb.getEpisodes(com,(com.epNum+1)-int(epnumpicker.value)-1,1,typeOf=com.type).episodes[0]
        e.page.add(
            genEpisodesheet(ep.episodeName,loadAsB64(ep.thumbnail),ep,wtb,naviPage)
        )
        prg.visible=False
        sheet.open = False
        # sheet.update()
    # if imgb64:
    imgb64 = b64.encodebytes(wtp.loadImage(com.previewImg)).decode('ascii').replace("\n","")
    com.epNum
    sheet = ft.BottomSheet(ft.Container(ft.Column([
        ft.Text(com.name,size=30,weight=ft.FontWeight.BOLD,max_lines=1),
        ft.Image(src_base64=imgb64,fit=ft.ImageFit.SCALE_DOWN),#,alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
        # ft.TextButton("view in browser",icon=ft.icons.OPEN_IN_BROWSER_OUTLINED,on_click=lambda a:openInBrowser("")),
        
        epnumpicker,
        ft.Text(f"/{com.epNum}"),]),
        ft.OutlinedButton("read",icon=ft.icons.READ_MORE_OUTLINED,on_click=readclick)
    ],tight=True,scroll=ft.ScrollMode.ADAPTIVE),padding=10),
    open=True,
    show_drag_handle=True,
    enable_drag=True,
    is_scroll_controlled=True)
    # else:
    #     sheet = ft.BottomSheet(ft.Container(ft.Column([
    #         ft.Text(epname),
    #         ft.Image(src='icon.png')
    #     ],tight=True),padding=10),
    #     open=True,
    #     show_drag_handle=True,
    #     enable_drag=True,
    #     is_scroll_controlled=True)
    
    # print(f"used: {wb.getRequestAmount().requestsUsed})")#/{wb.getRequestAmount().totalAvalible}")
    return sheet

def genComicCard(comic:wtp.comic, wb, pageData:fletnav.PageData) -> ft.Card:
    def containerclicked(e:ft.ControlEvent):
        print("clicked me!")
        e.page.add(genComicsheet(comic,wb,pageData))

        pass
    return ft.Container(
        ft.Row([
            ft.Image(src_base64=b64.encodebytes(wtp.loadImage(comic.previewImg)).decode('ascii').replace("\n",""),fit=ft.ImageFit.SCALE_DOWN,width=64,height=64,border_radius=5 if preferences["themeM2"] else 20),
            ft.Column([
                ft.Text(comic.name),
                ft.Text(f"by: {comic.author}")
    ])
    ]),
    bgcolor=ft.colors.GREEN_900,
    margin=5,
    padding=10,
    border_radius= 5 if preferences["themeM2"] else 20,
    on_click=containerclicked,
    ink=True
    )

def genSearchSheet(wb:wtp.webtoonapi,search:str,page:ft.Page):
    search = wb.doSearch(search)

@fletnav.route(fletnav.ROUTE_404)
def route_404(pg: fletnav.PageData):
    pg.add(ft.SafeArea(ft.Text("uh oh that dosent seem right😢 (404)"),expand=True))
    print(f"404 page!: {pg.navigator.route}")
    pg.add(ft.TextButton("back",on_click=lambda _: pg.navigator.navigate_homepage(pg.page)))

@fletnav.route("/errorPage")
def errorPage(pg:fletnav.PageData):
    print("ERROR PAGE: ",pg.arguments)
    if pg.arguments == ["readError1"]:
        pg.add(ft.SafeArea(ft.Row([
            ft.Icon(ft.icons.ERROR_OUTLINE),
            ft.Text("uh oh thare was an error!")
        ])))
        pg.add(ft.Icon(ft.icons.INFO_OUTLINE))
        pg.add(ft.Text("no arguments for read route"))
    elif pg.arguments == ["notReadyYet1"]:
        pg.add(ft.SafeArea(ft.Row([
            ft.Icon(ft.icons.ERROR_OUTLINE),
            ft.Text("sorry searching is'nt ready yet :(")
        ])))
    else:
        pg.add(ft.SafeArea(ft.Row([
            ft.Icon(ft.icons.ERROR_OUTLINE),
            ft.Text("uh oh thare was an error!")
        ])))
    pg.add(ft.ElevatedButton("Home",on_click=lambda _:pg.navigator.navigate_homepage(pg.page)))

@fletnav.route("/read")
def readPage(pg:fletnav.PageData):
    # print(pg.arguments)
    pg.page.scroll = True
    imgConts = []
    if not pg.arguments:
        pg.page.floating_action_button = None
        pg.navigator.navigate("/errorPage",pg.page,["readError1"])
        return
    # pg.add(ft.SafeArea())
    def exitEpisode(e):
        pg.page.floating_action_button = None
        pg.navigator.navigate(pg.previous_page,pg.page)
    print(len(pg.arguments))
    # print(pg.arguments[0][:40])
    images = ft.Column([],spacing=0)
    for i in pg.arguments[0]:
        images.controls.append(ft.Image(src_base64=i,fit=ft.ImageFit.FILL))
    pg.add(ft.SafeArea(images))
    pg.page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.EXIT_TO_APP_OUTLINED,on_click=exitEpisode,tooltip="exit the episode")
    pg.page.update()

@fletnav.route("/search")
def searchPage(pg:fletnav.PageData):
    # pg.navigator.navigate("/errorPage",pg.page,["notReadyYet1"])
    pg.set_appbar(ft.AppBar(leading=ft.Icon(ft.icons.SEARCH),title=ft.Text("Search"),elevation=20,actions=[ft.IconButton(ft.icons.ARROW_BACK,on_click=lambda _:pg.navigator.navigate("/",pg.page))]))
    
    pg.page.scroll = True
    searchBar = ft.TextField(label="Search",icon=ft.icons.SEARCH,expand=True)
    loadIndicator = ft.ProgressBar(animate_size=ft.Animation(100,ft.AnimationCurve.EASE_OUT),animate_opacity=ft.Animation(100,ft.AnimationCurve.EASE_OUT))
    
    def search(e):
        if len(pg.page.controls) > 2:
            for i in pg.page.controls[2:]:
                pg.page.remove(i)
            pg.page.update()
            loadIndicator.value = None
            loadIndicator.height = None
            loadIndicator.update()
        if typePicker.value == "canvas":
            print("==> do search <==")
            if searchBar.value == "":
                print("no input text!")
                searchBar.error_text = "Please input text!"
                searchBar.update()
                return
            # searchRow.width = 0
            searchArea.height = 0
            # searchRow.disabled = True
            print(f"query: {searchBar.value}")
            pg.add(loadIndicator)
            webtoon = webtoonapi
            print("search...")
            result:wtp.search =  webtoon.doSearch(searchBar.value,type="canvas")
            comics = []
            
            loadIndicator.value = 0
            for i in result.items:
                comics.append(genComicCard(i,webtoon,pg))
                print(i.name)
                print(loadIndicator.value)
                loadIndicator.value += 1.0/result.size
                loadIndicator.update()
            for i in comics:
                pg.add(i)
            loadIndicator.value = 1
            loadIndicator.height = 0
            loadIndicator.update()
            # loadIndicator.visible = False
        elif typePicker.value == "originals":
            print("==> do search (originals) <==")
            if searchBar.value == "":
                print("no input text!")
                searchBar.error_text = "Please input text!"
                searchBar.update()
                return
            # searchRow.width = 0
            searchArea.height = 0
            searchArea.update()
            # searchRow.disabled = True
            print(f"query: {searchBar.value}")
            pg.add(loadIndicator)
            webtoon = webtoonapi
            print("search...")
            
            everyComic = webtoon.listComics("originals")
            
            #cant find i way to do this yet
            comics = []
            
            #thare is 100% a better way to do this but i cant use binary liberarys like numpy so i tried
            for i in everyComic:
                print(i)
                if searchBar.value.lower() in i.name.lower():
                    print("match!")
                    if len(comics) < 20: #might change this later
                        comics.append(i)
                    else:
                        break
            
            print("done!")
            if len(comics) == 0:
                #add no results condition here soon
                print("no results!")
                cont = ft.Container(ft.Text("no results found!"),padding=ft.Padding(10,10,10,10),height = 0,animate=ft.Animation(600,ft.AnimationCurve.EASE_OUT_CIRC))
                pg.page.add(ft.Card(cont,
                    elevation=20,
                    color=ft.colors.RED_400,
                    width=pg.page.width
                    
                ))
                cont.height = None
                # cont.update()
                
                loadIndicator.value = 1
                searchArea.disabled = False
                # searchArea.scale = ft.Scale(1)
                loadIndicator.height = None
                searchArea.height = None
                searchArea.update()
                loadIndicator.update()
                return
            pg.page.update()
            # result:wtp.search =  webtoon.doSearch(searchBar.value,type="canvas")
            comicCards = []
            
            loadIndicator.value = 0
            for i in comics:
                comicCards.append(genComicCard(i,webtoon,pg))
                print(i.name)
                print(loadIndicator.value)
                loadIndicator.value += 1.0/len(comics)
                loadIndicator.update()
            colom = ft.Column(comicCards)
            cont = ft.Container(colom,animate_size=ft.Animation(500),height=0)
            pg.add(cont)
            cont.height = None
            cont.update()
            # for i in comicCards:
            #     pg.add(i)
            loadIndicator.value = 1
            loadIndicator.height = None
            # searchArea.scale = ft.Scale(1)
            # loadIndicator.width = 0
            searchArea.height = None
            loadIndicator.update()
            searchArea.update()
            # loadIndicator.visible = False
        searchArea.disabled = False
        searchArea.update()
        saveCache(pg.page)
    typePicker = ft.RadioGroup(ft.Row([ft.Radio(value="originals",label="originals",disabled=False),ft.Radio(value="canvas",label="canvas")],expand=True),value="canvas")
    searchRow = ft.Row([searchBar,ft.FilledTonalButton("GO!",on_click=search)])
    searchArea = ft.Container(
            ft.Column([searchRow,typePicker]),
                padding=ft.Padding(10,10,10,10),
                animate_size=ft.Animation(800,ft.AnimationCurve.EASE_OUT_QUART)
                    )
    print(f"h:{searchArea.height}")
    pg.add(ft.Card(ft.Card(searchArea,elevation=20)))
@fletnav.route("/setup")
def settingsPage(pg:fletnav.PageData):
    pg.set_appbar(ft.AppBar(leading=ft.Icon(ft.icons.SETTINGS),title=ft.Text("Settings"),elevation=20,actions=[ft.IconButton(ft.icons.ARROW_BACK,on_click=lambda _:pg.navigator.navigate("/",pg.page))]))
    def setM2theme(e:ft.ControlEvent):
        global preferences
        
        preferences["themeM2"] = {"true":True,"false":False}[e.data]
        print(e.data)
        pg.page.theme.use_material3 = not preferences["themeM2"]
        print(pg.page.theme)
        pg.page.update()
        pg.page.client_storage.set("ca.hugie999.toonify.prefs",preferences)
    pg.add(ft.Switch(label="Material 2 theme:",on_change=setM2theme,value=preferences["themeM2"]))
    pg.add(ft.Container(
        ft.FilledButton("RESET ALL USER DATA",
                        icon=ft.icons.DELETE_FOREVER_OUTLINED,
                        icon_color=ft.colors.RED,
                        on_click=lambda _: pg.page.client_storage.clear())
        ))
@fletnav.route("/debugpg")
def debugPage(pg:fletnav.PageData):
    # pg.add(ft.SafeArea())
    
    pg.set_appbar(ft.AppBar(
            leading=ft.Icon(ft.icons.TERMINAL),
            title=ft.Text("debug"),
            elevation=20,
            actions=[ft.IconButton(ft.icons.ARROW_BACK,on_click=lambda _:pg.navigator.navigate("/",pg.page))]
        ))
    comicidinput = ft.TextField(label="comic id:",value="300138",enable_suggestions=False,hint_text="0000000000",icon=ft.icons.BOOK_OUTLINED,input_filter=ft.NumbersOnlyInputFilter())
    episodeidinput = ft.TextField(label="episode id:",value="0",enable_suggestions=False,hint_text="000",icon=ft.icons.NUMBERS_ROUNDED,input_filter=ft.NumbersOnlyInputFilter(),disabled=True)
    comictypeinput = ft.RadioGroup(content=ft.Row([ft.Radio(value="originals",label="originals"),ft.Radio(value="canvas",label="canvas")]))
    def testbuttonaccept(e):
        pr = ft.ProgressRing()
        pg.add(pr)#ft.Column([ft.Row([pr],vertical_alignment=ft.CrossAxisAlignment.CENTER)],horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        print("aa")
        
        wb = webtoonapi
        comic = wb.getComic(comicidinput.value,type=comictypeinput.value)
        pg.add(genComicCard(comic,wb,pg))
        return
        ep = wb.getEpisodes(comicToUse=int(comicidinput.value),startIndex=int(episodeidinput.value),size=1,typeOf=comictypeinput.value)
        print(ep)
        print(ep.episodes[0].episodeName)
        eps = ep.episodes[0]
        # page.add(ft.Text(eps.episodeName))
        img = b64.encodebytes(wtp.loadImage(eps._json["thumbnailImageUrl"])).decode("ascii").replace("\n","") #yass
        # print(img)
        # page.add(ft.Image(src_base64=(img)))
        c = genEpisodesheet(eps.episodeName,img,eps,wb=wb,naviPage=pg)
        pr.visible = False
        pg.page.overlay.append(c)
        pg.page.update()
        c.open = True
        c.update()
    # logsSheet = ft.BottomSheet()
    isLogFile = True
    try:
        with open("out.log") as logFile:
            logsSheet = ft.BottomSheet(ft.TextField(value=logFile.read(),multiline=True,read_only=True),is_scroll_controlled=True)
            pg.add(logsSheet)
    except:
        isLogFile = False
        def closeMe(e):
            logError.open = False
            logError.update()
        logError = ft.AlertDialog(title=ft.Text("No log file!"),content=ft.Text("You might be running from the python file directly"),actions=[ft.TextButton("ok!",on_click=closeMe)])
        pg.add(logError)
    
    
    # print("a")
    pg.add(ft.SafeArea(comictypeinput),ft.Divider(),ft.Text("manual",size=30),ft.Row([comicidinput,episodeidinput,ft.TextButton("submit",on_click=testbuttonaccept)],scroll=ft.ScrollMode.ADAPTIVE))
    def openLogSheet(e):
        print("open!")
        if isLogFile:
            logsSheet.open = True
            logsSheet.update()
        else:
            logError.open = True
            logError.update()
            
    pg.add(ft.ElevatedButton("logs",on_click=openLogSheet))
    pg.page.update()

# @fletnav.route("read")
# def episodePage(pg:fletnav.PageData):
#     print(pg.arguments)

@fletnav.route("/")
def homePage(pg:fletnav.PageData):
    #do this thing
    global webtoonapi
    print(f"dimentions 2: [{pg.page.width},{pg.page.height},{pg.page.window_width},{pg.page.window_height}]")
    saveCache(pg.page)
    
    # pg.page.views.clear()
    print(pg.page.views)
    pg.page.scroll = False
    appbar = ft.AppBar(leading=ft.Icon(ft.icons.HOME),title=ft.Text("Home"),elevation=20)
        
    
    pg.set_appbar(appbar)
    pg.add(ft.SafeArea(ft.Row([ft.Icon(ft.icons.INFO,color=ft.colors.BLUE_400),ft.Text("looks like thares nothing here... ):")])))
    # pg.add(ft.Row([
    #     ft.ElevatedButton("go!",on_click=lambda _:pg.navigator.navigate("/read",pg.page,[0])),
    #     ft.ElevatedButton("debug!",on_click=lambda _:pg.navigator.navigate("/debugpg",pg.page,[0]))]
    #               ))
    if preferences["themeM2"]:
        BOXBUTTON = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
    else: 
        BOXBUTTON = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
    # pg.add(ft.ElevatedButton("Debug2",style=BOXBUTTON,on_click=lambda _:pg.navigator.navigate("/debugpg",pg.page,[0]))) <- this is from when i forgor that you cant use expand on buttons on mobile for some reason
    
    pg.add(
        ft.Column([
            ft.ElevatedButton("Search",width=pg.page.width,height=pg.page.height/3,style=BOXBUTTON,on_click=lambda _:pg.navigator.navigate("/search",pg.page,[0]),elevation=10),
            ft.ElevatedButton("Settings",width=pg.page.width,height=pg.page.height/8,style=BOXBUTTON,on_click=lambda _:pg.navigator.navigate("/setup",pg.page,[0]),elevation=10),
            ft.ElevatedButton("Debug",width=pg.page.width,height=pg.page.height/8,style=BOXBUTTON,on_click=lambda _:pg.navigator.navigate("/debugpg",pg.page,[0]),elevation=10)
        ],
        scroll=ft.ScrollMode.ALWAYS
    ))
    print(pg.page.platform)
    # if pg.page.platform == "android":
    
        
def main(page: ft.Page):
    page.add(ft.Container(
        ft.Card(ft.Container(
            ft.ProgressRing()
            ,padding=ft.Padding(50,50,50,50)),elevation=50) #container-seption
        ,alignment=ft.alignment.center,width=page.width,height=page.height))
    TOKEN = page.client_storage.get("ca.hugie999.toonify.token")
    global tokeninput
    global token
    global preferences
    print(page.client_storage.get("ca.hugie999.toonify.prefs"))
    if page.client_storage.contains_key("ca.hugie999.toonify.prefs"):
        preferences = page.client_storage.get("ca.hugie999.toonify.prefs")
    #note to self: this -> 1435 <- is the comic for testing originals
    print(f"dimentions: [{page.width},{page.height},{page.window_width},{page.window_height}]")
    
    def debugEvent(e:ft.ControlEvent):
        print()
        print(e)
        print(dir(e))
        print(e.__dict__)
        print()
    
    # page.on_window_event   = debugEvent
    # page.on_keyboard_event = debugEvent
    # page.window_close = debugEvent
    # page.window_prevent_close = True
    
    page.theme = ft.Theme(color_scheme_seed="green",color_scheme=ft.ColorScheme(ft.colors.GREEN))
    page.theme.use_material3 = not preferences["themeM2"]
    print(page.theme)
    print(page.theme.color_scheme)
    page.update()
    # page.views.append(ft.View("/h",[ft.Text("a")]))
    # page.views.pop()
    def search(e):
        pass
    img = imgs[0]
    # searcher = ft.SearchBar(bar_hint_text="search webtoons...")
    # page.add(searcher)
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.CONTAIN))
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.COVER))
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.FILL))
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.FIT_HEIGHT))
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.FIT_WIDTH))
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.NONE))
    # page.add(ft.Image(src_base64=img,fit=ft.ImageFit.SCALE_DOWN))
    page.scroll = True
    
    # page.client_storage.clear()
    
    # page.add(ft.ElevatedButton(ft.Text("test",expand=True)))
    # page.add()
    # page.add(ft.SafeArea(content=ft.Text(f"webtoon api: {wtp.__version__}")))
    page.title = "webtoon test"
    tokeninput = ft.TextField(hint_text="abcdefghijklmnopqrstuvwxyz1234567890",label="token:",password=True,can_reveal_password=True,enable_suggestions=False,expand=True)
    def settoken(e:ft.ControlEvent):
        global tokeninput
        
        # print(e.target)
        print(tokenpage)
        tokeninput.error_text = ""
        tokeninput.update()
        if tokeninput.value:
            tokenpage.open = False
            page.client_storage.set("ca.hugie999.toonify.token",tokeninput.value)
            snack = ft.SnackBar(ft.Text("Token saved!"),open=True)
            page.add(snack)
            page.update()
            page.window_destroy()
        else:
            tokeninput.error_text = "Please input a token!"
            tokeninput.update()
    
    tokenpage = ft.BottomSheet(ft.Container(
        ft.Column([
            ft.SafeArea(ft.Text("Add a token.",size=40)),
            ft.Text("A token is required to use the app"),
            ft.Row([ft.Icon(ft.icons.WARNING_OUTLINED,color=ft.colors.RED_400),ft.Text("NOTICE: currently tokens are unecryted in storage",color=ft.colors.RED_400)]),
            ft.Row([tokeninput,ft.ElevatedButton("Submit",icon=ft.icons.ADD,on_click=settoken)]),
            ft.Icon(ft.icons.INFO_OUTLINE,color=ft.colors.GREY_500),
            ft.Text("A token is required to access the api\ntokens can be found at rapidapi",color=ft.colors.GREY_500)])
    ,margin=10),dismissible= False,
    is_scroll_controlled=False,
    )
    page.add(tokenpage)
    if TOKEN:
        print("token pre-defined")
        tokeninput = ft.TextField(label="token:",enable_suggestions=False,hint_text="1234567890abcdefghijklmnopqrstuvwxyz",icon=ft.icons.ABC_OUTLINED,password=True,can_reveal_password=False,value=TOKEN,read_only=True,visible=False)
    else:
        tokenpage.open = True
        page.update()
        # tokeninput = ft.TextField(label="token:",enable_suggestions=False,hint_text="token",icon=ft.icons.ABC_OUTLINED,password=True,can_reveal_password=True)
    
    token = TOKEN
    while tokenpage.open == True:
        time.sleep(1)
    
    #this is just so back button works on android
    
    def navSetRoute(e):
        page.route = e
        page.update()
        print("nav route change")
        print(e)
        print(navigator._nav_previous_routes)
        
    def pageSetRoute(e:ft.RouteChangeEvent):
        
        print("page change")
        print(e.route)
        if e.route != page.route:
            navigator.navigate(e.route,page)
        print("already in route")
    def goBack(e):
        global closeAppForReal
        print("android back gesture!")
        if navigator.route == "/":
            if closeAppForReal:
                print("kill it!")
                page.window_destroy()
            else:
                print("close next time")
                closeAppForReal = True
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Back again to close"),open=True
            )
            # closeForReal = True
        else:
            pass
            # closeForReal = False
        print(page.views)
        print(navigator._nav_previous_routes[-1])
        print(f"prev routes ==> {navigator._nav_previous_routes}")
        navigator.navigate(navigator._nav_previous_routes[-1],page) #cant do it the normal way ):
        navigator._nav_previous_routes.pop() #remove ^ so it dosent broke
        page.floating_action_button = None
        print(f"prev routes2 => {navigator._nav_previous_routes}")
        page.update()
    page.on_view_pop = goBack
    
    # page.on_route_change = pageSetRoute #<== uncomment if your makeing this for a browser
    
    navanim = fletnav.NavigatorAnimation(
        fletnav.NavigatorAnimation.FADE,
        fletnav.NavigatorAnimation.SMOOTHNESS_10
    )
    navigator = fletnav.VirtualFletNavigator(route_changed_handler=navSetRoute,navigator_animation=navanim) #navigator_animation=fletnav.NavigatorAnimation(fletnav.NavigatorAnimation.FADE,fletnav.NavigatorAnimation.SMOOTHNESS_10),
    
    
    page.views.insert(-1,ft.View("BACKINTERCEPTER",[ft.Text("this should not appear")]))
    # navigator.route_changed_handler
    
    global webtoonapi
    print(type(webtoonapi))
    webtoonapi = wtp.webtoonapi(token)
    if page.client_storage.contains_key("ca.hugie999.toonify.storedcache"):
        webtoonapi.cache = wtp.webtoonCache(page.client_storage.get("ca.hugie999.toonify.storedcache"))
        print(webtoonapi.cache)
    else:
        saveCache(page)
    print(type(webtoonapi))
    # time.sleep(10) <== used for testing loading animation
    navigator.render(page)
    
    #comment this for id input area 
    return
    
    comicidinput = ft.TextField(label="comic id:",value="300138",enable_suggestions=False,hint_text="0000000000",icon=ft.icons.BOOK_OUTLINED,input_filter=ft.NumbersOnlyInputFilter())
    episodeidinput = ft.TextField(label="episode id:",value="0",enable_suggestions=False,hint_text="000",icon=ft.icons.NUMBERS_ROUNDED,input_filter=ft.NumbersOnlyInputFilter(),disabled=True)
    comictypeinput = ft.RadioGroup(content=ft.Row([ft.Radio(value="originals",label="originals"),ft.Radio(value="canvas",label="canvas")]))
    def testbuttonaccept(e):
        pr = ft.ProgressRing()
        page.add(pr)#ft.Column([ft.Row([pr],vertical_alignment=ft.CrossAxisAlignment.CENTER)],horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        print("aa")
        
        wb = wtp.webtoonapi(tokeninput.value)
        comic = wb.getComic(comicidinput.value,type=comictypeinput.value)
        page.add(genComicCard(comic,wb))
        return
        ep = wb.getEpisodes(comicToUse=int(comicidinput.value),startIndex=int(episodeidinput.value),size=1,typeOfComic=comictypeinput.value)
        print(ep)
        print(ep.episodes[0].episodeName)
        eps = ep.episodes[0]
        # page.add(ft.Text(eps.episodeName))
        img = b64.encodebytes(wtp.loadImage(eps._json["thumbnailImageUrl"])).decode("ascii").replace("\n","") #yass
        print(img)
        # page.add(ft.Image(src_base64=(img)))
        c = genEpisodesheet(eps.episodeName,img,eps,wb=wb)
        pr.visible = False
        page.overlay.append(c)
        page.update()
        c.open = True
        c.update()
        
    
    # print("a")
    page.add(comictypeinput,ft.Divider(),ft.Text("manual",size=30),ft.Row([comicidinput,episodeidinput,ft.TextButton("submit",on_click=testbuttonaccept)],scroll=ft.ScrollMode.ADAPTIVE))
    page.update()
    # page.add(ft.Card(ft.Text("hi")))
print("ft.app()")
ft.app(main)
