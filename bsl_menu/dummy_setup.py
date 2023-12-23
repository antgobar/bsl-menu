import random
import os

from . import crud, models, schemas, database


LOREM = """Lorem ipsum dolor sit amet. Qui quia amet in eaque consectetur in rerum accusantium eum itaque aperiam. 
Vel totam laborum non rerum nesciunt aut expedita omnis ut nihil molestiae et amet magni sed perspiciatis enim a 
officia autem. Et eius facilis ut fugit quis quo dolore iste qui laborum facilis qui illum ipsa aut nemo sunt! 
Et voluptate aspernatur et aliquam tempora aut accusantium quidem eos doloremque rerum ad beatae odio aut nisi 
voluptatibus."""
CITIES = ["Leeds", "London", "Liverpool", "Leciestair", "Lincon"]
CUISINES = ["Pub Grub", "Seafood", "Vegan", "American", "Pasta"]
YEARS_OPENED = list(range(2000, 2023))
# VISUAL_SOURCES = ["sl-burgerking.gif", "sl-fish.gif", "sl-pasta.gif", "sl-vegetarian.gif"]
LOCALES = ["Pub", "Restaurant", "Bistro", "Cafe"]


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


def populate_restaurants(db, visual_ids, no=3):
    all_restaurants = crud.read_restaurants(db)
    if len(all_restaurants) > 15:
        return
    for _ in range(no):
        restaurant = dummy_restaurant(visual_ids)
        crud.create_restaurant(db=db, restaurant=restaurant)
    db.close()


def dummy_setup():
    db = database.SessionLocal()
    all_visuals = populate_visuals(db)
    visual_ids = [visual.id for visual in all_visuals]
    populate_restaurants(db, visual_ids)


def generate_description():
    lorem = LOREM.replace("\n", "").split(". ")
    selected_length = random.randint(0, len(lorem))
    return ". ".join(lorem[:selected_length])


def dummy_restaurant(visual_ids):
    city = random.choice(CITIES)
    category = random.choice(CUISINES)
    locale = random.choice(LOCALES)
    return schemas.RestaurantCreate(
        name=f"The {city} {category} {locale}",
        city=city,
        category=category,
        description=generate_description(),
        year_opened=random.choice(YEARS_OPENED),
        is_active=True,
        visual_id=random.choice(visual_ids)
    )
