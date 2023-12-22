from fastapi import APIRouter, Request

from bsl_menu.database import DbSession


router = APIRouter(prefix="/menu", tags=["menu"])


@router.get("/")
async def get_menu_items(request: Request, db: DbSession, skip: int = 0, limit: int = 100):
    return {"not": "implemented"}
