from datetime import datetime
from hashlib import md5
from pathlib import Path
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
)
from fastapi.staticfiles import StaticFiles
from fastapi_cache.decorator import cache
from .dependencies import CACHE, DB, lifespan, LINK_REPO
from .generator import to_code_obf, from_code_obf
from pydantic import HttpUrl
# Happy Diwali!!!!! greetings from Indiaaaa

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
app = FastAPI(debug=True, title="URL-Shorter", lifespan=lifespan)




@app.post("/link", status_code=201)
async def create_short_link(link: HttpUrl, repo: LINK_REPO) -> PlainTextResponse:
    return PlainTextResponse(
        to_code_obf((await repo.add_link(str(link))).id)
        )


@app.delete("/link", status_code=204)
async def delete(repo: LINK_REPO, code: str = Query()):
    id = from_code_obf(code)
    await repo.delete_link(id)


@app.get("/-/{code}")
@cache(60, namespace="links")
async def get_normal_link(code: str, repo:LINK_REPO) -> RedirectResponse:
    url = (await repo.get_link(from_code_obf(code))).url
    if url is None:
        raise HTTPException(404)
    return RedirectResponse(url)


@app.get("/links", status_code=200)
async def get_all_link(repo: LINK_REPO) -> JSONResponse:
    return await repo.get_links()


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/home")
# @cache()
def get_homepage() -> HTMLResponse:
    return HTMLResponse((TEMPLATES_DIR / "home.html").read_text(encoding="utf-8"))


# @app.get("/test")
# @cache(60)
# async def test():
#     await asyncio.sleep(5)
#     return "Very important work"


def run():
    uvicorn.run("url_shorter.main:app", host="0.0.0.0", port=8000, reload=True)
