from fastapi import APIRouter, Request, HTTPException

from bsl_menu.schemas import Restaurant, RestaurantCreate
from bsl_menu.crud import create_restaurant, read_restaurant, read_restaurants, remove_restaurant
from bsl_menu.database import DbSession


router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post("/", response_model=Restaurant)
async def post_restaurant(request: Request, db: DbSession, restaurant: RestaurantCreate):
    return create_restaurant(db, restaurant)


@router.get("/{_id}", response_model=Restaurant)
async def get_restaurant(request: Request, db: DbSession, _id: int):
    result = read_restaurant(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"restaurant with id: {_id} not found")


@router.get("/", response_model=list[Restaurant])
async def get_restaurants(request: Request, db: DbSession, skip: int = 0, limit: int = 100):
    return read_restaurants(db, skip=skip, limit=limit)


@router.delete("/{_id}", response_model=Restaurant)
async def delete_restaurant(request: Request, db: DbSession, _id: int):
    result = remove_restaurant(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Restaurant with id: {_id} not found")
