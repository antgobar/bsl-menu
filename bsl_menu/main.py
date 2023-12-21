import os
from typing import Annotated

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import crud, schemas
from .models import Base
from .database import SessionLocal, engine
from .dummy_setup import add_dummy_data


Base.metadata.create_all(bind=engine)
app = FastAPI()
current_directory = os.path.dirname(os.path.realpath(__file__))
static_files = StaticFiles(directory=os.path.join(current_directory, "static"))
app.mount("/static", static_files, name="static")
templates = Jinja2Templates(directory=os.path.join(current_directory, "templates"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
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


@app.post("/restaurants", response_model=schemas.Restaurant)
async def post_restaurant(request: Request, restaurant: schemas.CreateRestaurant, db: Session = Depends(get_db)):
    return crud.create_restaurant(db=db, restaurant=restaurant)


@app.get("/restaurants", response_model=list[schemas.Restaurant])
async def get_restaurants(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_restaurants(db, skip=skip, limit=limit)


@app.get("/search")
async def search_restaurants(request: Request, name: str, db: Session = Depends(get_db)):
    restaurants = crud.search_restaurants_by_name(db, name=name, limit=20)
    return templates.TemplateResponse(
        "restaurants.html",
        {"request": request, "restaurants": restaurants, "headers": request.headers}
    )


@app.get("/restaurants/{_id}", response_model=schemas.Restaurant)
async def get_restaurant(request: Request, _id: int, db: Session = Depends(get_db)):
    result = crud.read_restaurant(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Restaurant with id: {_id} not found")


@app.delete("/restaurants/{_id}", response_model=schemas.Restaurant)
async def delete_restaurant(request: Request, _id: int, db: Session = Depends(get_db)):
    result = crud.delete_restaurant(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Restaurant with id: {_id} not found")


@app.post("/restaurants/{restaurant_id}/menu/", response_model=schemas.MenuItem)
def post_menu_item_for_restaurant(
    request: Request,
    restaurant_id: int,
    menu_item: schemas.CreateMenuItem,
    db: Session = Depends(get_db)
):
    return crud.create_restaurant_menu_item(db=db, menu_item=menu_item, restaurant_id=restaurant_id)


@app.get("/restaurants/{restaurant_id}/menu", response_model=list[schemas.MenuItem])
def get_menu_for_restaurant(
    request: Request,
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    return crud.read_restaurant_menu_item(db=db, restaurant_id=restaurant_id)


@app.get("/menu/{_id}", response_model=schemas.MenuItem)
async def get_menu_item(request: Request, _id: int, db: Session = Depends(get_db)):
    result = crud.read_menu_item(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Menu item with id: {_id} not found")


@app.post("/visuals", response_model=schemas.Visual)
async def post_visual(request: Request, visual: schemas.CreateVisual, db: Session = Depends(get_db)):
    return crud.create_visual(db, visual)


@app.get("/visuals/{_id}", response_model=schemas.Visual)
async def get_restaurant(request: Request, _id: int, db: Session = Depends(get_db)):
    result = crud.read_visual(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Visual with id: {_id} not found")


@app.get("/visuals", response_model=list[schemas.Visual])
async def get_visual(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_visuals(db, skip=skip, limit=limit)
