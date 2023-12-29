from fastapi import APIRouter, Request, HTTPException

from bsl_menu.database import DbSession
from bsl_menu.schemas import MenuItem
from bsl_menu.crud import read_menu_item
from bsl_menu.templates import templates


router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/")
async def get_menu_items(request: Request, db: DbSession, skip: int = 0, limit: int = 100):
    return {"not": "implemented"}


@router.get("/{_id}", response_model=MenuItem)
async def get_menu_item(request: Request, _id: int, db: DbSession):
    result = read_menu_item(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Menu item with id: {_id} not found")


@router.get("/add-to-restaurant/{restaurant_id}/{restaurant_name}")
async def add_menu_item_for_restaurant(request: Request, restaurant_id: int, restaurant_name: str):
    return templates.TemplateResponse(
        "menu_item_add.html",
        {"request": request, "restaurant_id": restaurant_id, "restaurant_name": restaurant_name}
    )
