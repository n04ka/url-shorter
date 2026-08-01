from hashlib import md5, sha256
# Happy Diwali!!!!! greetings from Indiaaaa
import os
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse

def generete_hash(url) -> hash:
    try:
        hash = sha256(url.encode()).hexdigest()
        return hash
    except Exception as e:
        print(f"Eroro generating hash: {hash}")
        exit()


class LinkRepo:
    def __init__(self):
        self.urls = {}

    def add_link(self, url: str) -> str:
        code = generete_hash(url)
        self.urls[code] = url
        return code

    def get_link(self, code: str) -> str|None:
        return self.urls.get(code)
            
app = FastAPI(debug=True, title="URL-Shorter")
repo = LinkRepo()


@app.post("/link")
def create_short_link(link: str):
    return repo.add_link(link)

@app.post("/delete/link", status_code=201)
def dlete_link(code: str = Query()):
    LinkRepo.urls.pop(code)
@app.get("/-/{code}")
def get_normal_link(code: str) -> RedirectResponse:
    url = repo.get_link(code)
    if url is None:
        raise HTTPException(404)
    return RedirectResponse(url)
@app.post("/link/get_all_link", status_code=200)
def get_all_link() -> str:
    json = str(LinkRepo().urls)
    return json

from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/home")   
def get_homepage() -> HTMLResponse:
    html = (TEMPLATES_DIR / "home.html").read_text()
    return HTMLResponse(html)


def run():
    uvicorn.run("url_shorter.main:app", host="0.0.0.0", port=8000, reload=True)