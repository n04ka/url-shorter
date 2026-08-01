from hashlib import md5

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse


class LinkRepo:
    def __init__(self):
        self.urls = {}

    def add_link(self, url: str) -> str:
        code = md5(url.encode()).hexdigest()[:5]
        self.urls[code] = url
        return code

    def get_link(self, code: str) -> str|None:
        return self.urls.get(code)
            
app = FastAPI(debug=True, title="URL-Shorter")
repo = LinkRepo()


@app.post("/link")
def create_short_link(link: str):
    return repo.add_link(link)


@app.get("/-/{code}")
def get_normal_link(code: str) -> RedirectResponse:
    url = repo.get_link(code)
    if url is None:
        raise HTTPException(404)
    return RedirectResponse(url)


def main():
    uvicorn.run(app, port=8000)
