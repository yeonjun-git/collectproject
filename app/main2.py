from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
# StaticFiles는 CSS 등 HTML에 색을 입히고 웹상에 이미지를 처리하는 메서드

from pathlib import Path
Base_dir = Path(__file__).resolve().parent


templates = Jinja2Templates(directory=Base_dir/"templates")
# 해당하는 HTML 파일을 서빙할건데, 그 HTML파일의 위치를 저장
# templates의 parent 경로 폴더의 이름이 바뀌어도 항상 지정될 수 있도록
# Base_dir 변수에 절대경로를 지정해준다.

# 아래의 라우터가 HTML 파일을 서빙하는 라우터임.
@app.get("/items/{id}", response_class=HTMLResponse) # response 타입을 HTMLResponse로.
async def read_item(request: Request, id: str): # request는 반드시 지정해야함
    return templates.TemplateResponse("item.html", {"request": request, "id": id, "data":"냅니 바보"})



## ../Project 경로에서 uvicorn app.main2:app --reload
# templates = Jinja2Templates(directory="templates") --> 오류
# templates = Jinja2Templates(directory="app/templates") --> 정상

## ../Project/app 경로에서 uvicorn main2:app --reload
# templates = Jinja2Templates(directory="app/templates") --> 오류
# templates = Jinja2Templates(directory="templates") --> 정상

## 결론
# uvicorn 실행 위치와 Jinja2Templates의 directory 위치는 동일해야 한다.
