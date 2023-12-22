import os
from typing import Annotated

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from . import crud, schemas
from .database import DbSession
from .dummy_setup import add_dummy_data
from . import routers


app = FastAPI()
app.include_router(routers.restaurants.router)
app.include_router(routers.visuals.router)
app.include_router(routers.menu.router)
app.include_router(routers.search.router)

current_directory = os.path.dirname(os.path.realpath(__file__))
static_files = StaticFiles(directory=os.path.join(current_directory, "static"))
app.mount("/static", static_files, name="static")
templates = Jinja2Templates(directory=os.path.join(current_directory, "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: DbSession):
    restaurants = crud.read_restaurants(db, limit=3)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "restaurants": restaurants}
    )


def on_startup():
    # add_dummy_data()
    pass


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse("bsl_menu/static/img/favicon.ico")


@app.get("/search")
async def search_restaurants(request: Request, db: DbSession, name: str):
    restaurants = crud.search_restaurants_by_name(db, name=name, limit=20)
    return templates.TemplateResponse(
        "restaurants.html",
        {"request": request, "restaurants": restaurants, "headers": request.headers}
    )


@app.post("/restaurants/{restaurant_id}/menu/", response_model=schemas.MenuItem)
def add_menu_item_to_restaurant(
    request: Request,
    db: DbSession,
    restaurant_id: int,
    menu_item: schemas.MenuItemCreate
):
    return crud.create_restaurant_menu_item(db=db, menu_item=menu_item, restaurant_id=restaurant_id)


@app.get("/restaurants/{restaurant_id}/menu", response_model=list[schemas.MenuItem])
def get_menu_for_restaurant(
    request: Request,
    db: DbSession,
    restaurant_id: int,
):
    return crud.read_restaurant_menu(db=db, restaurant_id=restaurant_id)


@app.get("/menu/{_id}", response_model=schemas.MenuItem)
async def get_menu_item(request: Request, _id: int, db: DbSession):
    result = crud.read_menu_item(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Menu item with id: {_id} not found")
