import os

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from . import crud
from .database import DbSession
from .dummy_setup import dummy_setup
from . import routers
from .templates import templates

app = FastAPI()
app.include_router(routers.restaurants.router)
app.include_router(routers.visuals.router)
app.include_router(routers.menu.router)
app.include_router(routers.search.router)

current_directory = os.path.dirname(os.path.realpath(__file__))
static_files = StaticFiles(directory=os.path.join(current_directory, "static"))
app.mount("/static", static_files, name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: DbSession):
    restaurants = crud.read_restaurants(db, limit=3)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "restaurants": restaurants}
    )


@app.on_event("startup")
async def startup_event():
    dummy_setup()


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse("bsl_menu/static/img/favicon.ico")
