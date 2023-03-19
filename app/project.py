from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.book import BookModel

from app.bookscraper import NaverBookScraper
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
    return templates.TemplateResponse(
        "./project_index.html",
        {
        "request": request, "title": "Book Collector"
        })

@app_project.get("/search", response_class=HTMLResponse) 
async def search(request: Request, q: str):


    # 1. 쿼리(q)에서 검색어 추출
    keyword = q

    # ------------------------------------------------------------
    ### 예외 처리

    ## 1. 검색어가 없다면 사용자에게 검색을 요구하는 것
    if not keyword:
        context = {"request": request, "title": "Book Collector"}
        return templates.TemplateResponse(
            "./project_index.html",
            context   
        )

    ## 2. 중복저장 방지 처리
    # 한번 검색해서 MongoDB에 저장된 데이터를 다시 검색한 경우,
    # 또 다시 DB에 저장하지 않고 바로 웹에서 보여주기만 하는 처리
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        # mongodb.engine에서 BookModel을 찾는다. 어떤 조건으로 찾냐면,
        # BookModel.keyword가 상단 q로 저장된 keyword와 같은 조건인 것.


        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        # 같은 조건인 것이 있다면 그것을 books에 지정하고 html에서 보여주도록 한다.
        return templates.TemplateResponse(
            "./project_index.html",
            {"request": request, "title": "Book Collector", "books": books})
    # ------------------------------------------------------------

    # 2. 데이터 수집기로 검색어에 대해 수집
    naver_book_scraper = NaverBookScraper()
    book_models = [] # DB 저장 전 수집데이터를 리스트에 담아준다. (비동기 저장을 위해서)
    books = await naver_book_scraper.search(keyword = keyword, total_page = 10)
    for book in books:
        book_model = BookModel(
        keyword = keyword,
        title = book['title'],
        publisher = book['publisher'],
        price = book['discount'],
        image = book['image']
        )
        book_models.append(book_model)

    # 3. 수집한 데이터 저장
    await mongodb.engine.save_all(book_models)
    ## save_all: 비동기 방식으로 데이터 저장
    ## save_all은 mongodb.engine에서 asyncio.gather를 사용해 구동하는 방식이다.
    
    
        
    return templates.TemplateResponse(
        "./project_index.html",
        {
        "request": request, "title": "Book Collector", "books": books
        })


## 이벤트 발생 시(서버 가동이 시작될 때 / 종료될 때)
## mongodb connect / disconnect

@app_project.on_event("startup") # startup이라는 이벤트 실행될 때
def on_app_start():
    mongodb.connect()

@app_project.on_event("shutdown") # shutdown이라는 이벤트 실행될 때
def on_app_shutdown():
    mongodb.close()


    