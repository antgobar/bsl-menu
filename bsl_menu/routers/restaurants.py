import os

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from bsl_menu.templates import templates
from bsl_menu.schemas import Restaurant, RestaurantCreate, MenuItem, MenuItemCreate
from bsl_menu.crud import (
    create_restaurant,
    read_restaurant,
    read_restaurants,
    remove_restaurant,
    create_restaurant_menu_item,
    read_restaurant_menu,
    search_restaurants_by_name
)
from bsl_menu.database import DbSession

ENDPOINT = os.path.basename(__file__).split(".")[0]
router = APIRouter(prefix=f"/{ENDPOINT}", tags=[ENDPOINT])


@router.get("/register")
async def register_restaurant_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/", response_model=Restaurant)
async def post_restaurant(request: Request, db: DbSession, restaurant: RestaurantCreate):
    return create_restaurant(db, restaurant)


@router.get("/{_id}", response_class=HTMLResponse)
async def get_restaurant(request: Request, db: DbSession, _id: int):
    restaurant = read_restaurant(db, _id)
    return templates.TemplateResponse(
        "restaurant_detail.html",
        {"request": request, "restaurant": restaurant}
    )


@router.get("/", response_class=HTMLResponse)
async def get_restaurants(request: Request, db: DbSession, skip: int = 0, limit: int = 100):
    restaurants = read_restaurants(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "restaurants.html",
        {
            "request": request,
            "restaurants": restaurants,
            "skip": skip, "limit": limit, "endpoint": ENDPOINT
        }
    )


@router.delete("/{_id}", response_model=Restaurant)
async def delete_restaurant(request: Request, db: DbSession, _id: int):
    result = remove_restaurant(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Restaurant with id: {_id} not found")


@router.post("/{_id}/menu", response_model=MenuItem)
def add_menu_item_to_restaurant(
    request: Request,
    db: DbSession,
    _id: int,
    menu_item: MenuItemCreate
):
    return create_restaurant_menu_item(db=db, menu_item=menu_item, restaurant_id=_id)


@router.get("/{_id}/menu", response_model=list[MenuItem])
def get_menu_for_restaurant(
    request: Request,
    db: DbSession,
    _id: int,
):
    return read_restaurant_menu(db=db, restaurant_id=_id)


@router.get("/search/")
async def search_restaurants(
    request: Request,
    db: DbSession,
    name: str,
    skip: int = 0,
    limit: int = 100
):
    restaurants = search_restaurants_by_name(db, name=name, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "restaurants.html",
        {
            "request": request,
            "restaurants": restaurants,
            "headers": request.headers,
            "skip": skip, "limit": limit, "endpoint": "restaurants"
        }
    )