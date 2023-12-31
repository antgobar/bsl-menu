import os
from datetime import date

from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse

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
    return templates.TemplateResponse(
        "restaurant_register.html",
        {"request": request, "current_date": date.today()}
    )


@router.post('/register', response_class=HTMLResponse)
def register_restaurant_post(
        request: Request,
        db: DbSession,
        restaurant: RestaurantCreate = Depends(RestaurantCreate.as_form)
):
    created_restaurant = create_restaurant(db, restaurant)
    categories = list(set([item.category for item in created_restaurant.menu_items]))
    return templates.TemplateResponse(
        "restaurant_detail.html",
        {"request": request, "restaurant": created_restaurant, "categories": categories}
    )


@router.post("/", response_model=Restaurant)
async def post_restaurant(request: Request, db: DbSession, restaurant: RestaurantCreate):
    return create_restaurant(db, restaurant)


@router.get("/{_id}", response_class=HTMLResponse)
async def get_restaurant(request: Request, db: DbSession, _id: int):
    restaurant = read_restaurant(db, _id)
    categories = list(set([item.category for item in restaurant.menu_items]))
    return templates.TemplateResponse(
        "restaurant_detail.html",
        {"request": request, "restaurant": restaurant, "categories": categories}
    )


@router.get("/", response_class=HTMLResponse)
async def get_restaurants(request: Request, db: DbSession, skip: int = 0, limit: int = 100):
    restaurants = read_restaurants(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "restaurants.html",
        {
            "request": request,
            "restaurants": restaurants,
            "skip": skip, "limit": limit
        }
    )


@router.delete("/{_id}", response_model=Restaurant)
async def delete_restaurant(request: Request, db: DbSession, _id: int):
    result = remove_restaurant(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Restaurant with id: {_id} not found")


@router.get("/{restaurant_id}/menu/{restaurant_name}/", response_class=HTMLResponse)
def add_menu_item_to_restaurant_form(
    request: Request,
    restaurant_id: int,
    restaurant_name: str
):
    return templates.TemplateResponse(
        "menu_item_form.html",
        {
            "request": request,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant_name
        }
    )


@router.post("/{restaurant_id}/menu/{restaurant_name}/", response_class=HTMLResponse)
def add_menu_item_to_restaurant(
        request: Request,
        db: DbSession,
        restaurant_id: int,
        restaurant_name: str,
        menu_item: MenuItemCreate = Depends(MenuItemCreate.as_form)
):
    create_restaurant_menu_item(db, menu_item, restaurant_id)
    redirect_url = request.url_for('get_restaurant', _id=restaurant_id)
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


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
