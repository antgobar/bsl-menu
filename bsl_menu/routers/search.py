from fastapi import APIRouter, Request, HTTPException

from bsl_menu.crud import search_entities_by_key_value
from bsl_menu.database import DbSession
from bsl_menu import models
from bsl_menu import schemas


router = APIRouter(prefix="/search", tags=["search"])


MODELS = {
    "restaurant": models.Restaurant,
    "menu_item": models.MenuItem,
    "visual": models.Visual
}


@router.get("/")
def search_entity(
        request: Request,
        db: DbSession,
        entity: str,
        field: str,
        value: str,
        skip: int = 0,
        limit: int = 100
):
    model = MODELS.get(entity)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Entity {entity} does not exist")
    column = model.__dict__.get(field)
    if column is None:
        raise HTTPException(status_code=404, detail=f"Field {field} in {entity} does not exist")
    result = search_entities_by_key_value(db, model, column, value, skip, limit)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No results for {value} found")
    return result
