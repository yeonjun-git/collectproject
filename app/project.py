from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.book import BookModel
#-----------------------------------------------------
# mongodb(NoSQL) connect library
from app.models import mongodb
#-----------------------------------------------------


from pathlib import Path
Base_dir = Path(__file__).resolve().parent

app_project = FastAPI()
templates = Jinja2Templates(directory=Base_dir/"project_templates")

@app_project.get("/", response_class=HTMLResponse) 
async def read_root(request: Request):
    book = BookModel(keyword="파이썬", publisher="BJPublic", price=1200, image="me.png")
    print(await mongodb.engine.save(book)) # DB에 저장하는 코드. save가 async 함수이므로 await 사용
    return templates.TemplateResponse(
        "./project_index.html",
        {
        "request": request, "title": "콜렉터스 북북이"
        })

@app_project.get("/search", response_class=HTMLResponse) 
async def search(request: Request, q: str):
    return templates.TemplateResponse(
        "./project_index.html",
        {
        "request": request, "title": "콜렉터스 북북이", "keyword": q
        })


## 이벤트 발생 시(서버 가동이 시작될 때 / 종료될 때)
## mongodb connect / disconnect

@app_project.on_event("startup") # startup이라는 이벤트 실행될 때
def on_app_start():
    mongodb.connect()

@app_project.on_event("shutdown") # shutdown이라는 이벤트 실행될 때
def on_app_shutdown():
    mongodb.close()