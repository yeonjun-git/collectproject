from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
Base_dir = Path(__file__).resolve().parent

app_project = FastAPI()
templates = Jinja2Templates(directory=Base_dir/"project_templates")

@app_project.get("/", response_class=HTMLResponse) 
async def read_root(request: Request):
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