from fastapi import APIRouter, Request, HTTPException

from bsl_menu.schemas import Visual, VisualCreate
from bsl_menu.crud import create_visual, read_visual, read_visuals, remove_visual
from bsl_menu.database import DbSession


router = APIRouter(prefix="/visuals", tags=["visuals"])


@router.post("/", response_model=Visual)
async def post_visual(request: Request, db: DbSession, visual: VisualCreate):
    return create_visual(db, visual)


@router.get("/{_id}", response_model=Visual)
async def get_visual(request: Request, db: DbSession, _id: int):
    result = read_visual(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Visual with id: {_id} not found")


@router.get("/", response_model=list[Visual])
async def get_visual(request: Request, db: DbSession, skip: int = 0, limit: int = 100):
    return read_visuals(db, skip=skip, limit=limit)


@router.delete("/{_id}", response_model=Visual)
async def delete_visual(request: Request, db: DbSession, _id: int):
    result = remove_visual(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Visual with id: {_id} not found")
