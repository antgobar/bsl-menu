from uuid import uuid4

from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse

from bsl_menu.schemas import Visual, VisualCreate
from bsl_menu.crud import (
    create_visual,
    read_visual,
    read_visuals,
    remove_visual,
    update_visual_reference_link,
    search_visual_by_name
)
from bsl_menu.database import DbSession
from bsl_menu.templates import templates


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


@router.get("/", response_class=HTMLResponse)
async def get_visuals(request: Request, db: DbSession, skip: int = 0, limit: int = 5):
    visuals = read_visuals(db, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "visuals.html",
        {
            "request": request,
            "visuals": visuals,
            "skip": skip, "limit": limit
        }
    )


@router.patch("/{_id}", response_model=Visual)
async def patch_visual_reference_id(request: Request, db: DbSession, _id: int, reference_link: str):
    return update_visual_reference_link(
        db, _id, reference_link
    )


@router.delete("/{_id}", response_model=Visual)
async def delete_visual(request: Request, db: DbSession, _id: int):
    result = remove_visual(db, _id)
    if result:
        return result
    raise HTTPException(status_code=404, detail=f"Visual with id: {_id} not found")


@router.get("/search/", response_class=HTMLResponse)
async def search_visuals_by_name_view(request: Request, db: DbSession, name: str, skip: int = 0, limit: int = 10):
    visuals = search_visual_by_name(db, name, limit=3)
    return templates.TemplateResponse(
        "visuals_search.html",
        {
            "request": request,
            "visuals": visuals,
            "skip": skip, "limit": limit
        }
    )


@router.get("/search-form/")
def visuals_search_form(request: Request):
    return templates.TemplateResponse(
        "visual_search_form.html", {"request": request}
    )


@router.get("/upload/")
def visual_upload_form(request: Request):
    return templates.TemplateResponse(
        "visual_upload_form.html", {"request": request}
    )


@router.post("/upload")
def upload_visual(
    request: Request,
    db: DbSession,
    visual_name: str,
    visual_description: str,
    visual_file: UploadFile = File(...),
):
    try:
        filename = f"bsl_menu/static/img/{uuid4()}-{visual_file.filename}"
        contents = visual_file.file.read()
        with open(filename, "wb") as f:
            f.write(contents)
        visual = VisualCreate(
            name=visual_name,
            description=visual_description,
            reference_link=filename
        )
        created_visual = create_visual(db, visual)
        return {"message": f"Successfully uploaded {filename}"}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        visual_file.file.close()
