import os

from . import crud, schemas, database


def dummy_setup():
    db = database.SessionLocal()
    populate_visuals(db)
    pass


def populate_visuals(db):
    files = os.listdir("bsl_menu/static/img")
    all_visuals = crud.read_visuals(db, skip=0, limit=100)
    reference_links = [visual.reference_link for visual in all_visuals]
    for file in files:
        filename, extension = file.split(".")
        if extension not in ["gif", "png"]:
            continue
        if file in reference_links:
            continue

        schema = schemas.VisualCreate(
            name=filename,
            description="A nice gif here",
            reference_link=file
        )
        crud.create_visual(db, schema)
    return crud.read_visuals(db, skip=0, limit=100)
