import os
from datetime import date

from . import crud, schemas, database


RESTAURANTS = [
    {"name": "Culinary Haven", "city": "Metropolis", "category": "Fine Dining", "description": "A haven for culinary delights", "date_opened": date(2022, 1, 1), "visual_id": 1},
    {"name": "Gourmet Grove", "city": "Cityville", "category": "Gourmet", "description": "Experience the grove of gourmet flavors", "date_opened": date(2022, 3, 15), "visual_id": 2},
    {"name": "Flavor Fusion", "city": "Townsville", "category": "Fusion", "description": "Where flavors collide and create magic", "date_opened": date(2022, 5, 20), "visual_id": 3},
    {"name": "Palate Paradise", "city": "Vibrant City", "category": "Eclectic", "description": "A paradise for your taste buds", "date_opened": date(2022, 7, 10), "visual_id": 4},
    {"name": "Urban Bites", "city": "Downtown", "category": "Casual Dining", "description": "Bites that define urban flavor", "date_opened": date(2022, 9, 5), "visual_id": 5},
    {"name": "Savory Oasis", "city": "Serene Town", "category": "Mediterranean", "description": "An oasis of savory delights", "date_opened": date(2022, 11, 18), "visual_id": 6},
    {"name": "Spice Street Kitchen", "city": "Spiceville", "category": "Spicy Cuisine", "description": "Explore the flavors of Spice Street", "date_opened": date(2023, 2, 28), "visual_id": 7},
    {"name": "Tasteful Trends", "city": "Trendy Heights", "category": "Trendy Cuisine", "description": "Setting the trends in tasteful dining", "date_opened": date(2023, 4, 12), "visual_id": 8},
    {"name": "Fusion Feast", "city": "Flavor City", "category": "Global Fusion", "description": "Feast on a global fusion of flavors", "date_opened": date(2023, 6, 8), "visual_id": 9},
    {"name": "Epicurean Echo", "city": "Echo Springs", "category": "Epicurean", "description": "An echo of epicurean delights", "date_opened": date(2023, 8, 15), "visual_id": 10},
    {"name": "Gastronomy Gallery", "city": "Artisan Town", "category": "Artisanal Cuisine", "description": "A gallery of gastronomic creations", "date_opened": date(2023, 10, 25), "visual_id": 11},
    {"name": "SavorCraft", "city": "Craftville", "category": "Crafted Delicacies", "description": "Crafting the art of savoring", "date_opened": date(2023, 12, 5), "visual_id": 12},
    {"name": "The Culinary Canvas", "city": "Canvas City", "category": "Artistic Dining", "description": "A canvas of culinary masterpieces", "date_opened": date(2024, 2, 14), "visual_id": 13},
    {"name": "Exquisite Eats", "city": "Eleganceville", "category": "Elegant Dining", "description": "Elegance meets exquisite flavors", "date_opened": date(2024, 4, 1), "visual_id": 14},
    {"name": "Epic Flavor Journeys", "city": "Journey Junction", "category": "Journey-inspired Cuisine", "description": "Embark on epic flavor journeys", "date_opened": date(2024, 6, 20), "visual_id": 15},
    {"name": "Delightful Dish Dunes", "city": "Dishville", "category": "Dish-centric Dining", "description": "Dunes of delightful dishes", "date_opened": date(2024, 8, 10), "visual_id": 16},
    {"name": "Urban Spice Palette", "city": "Spice District", "category": "Urban Spice", "description": "A palette of urban spice", "date_opened": date(2024, 10, 5), "visual_id": 17},
    {"name": "Taste Enclave", "city": "Enclave City", "category": "Enclave Dining", "description": "An exclusive enclave of taste", "date_opened": date(2024, 12, 1), "visual_id": 18},
    {"name": "Culinary Crescendo", "city": "Crescendo Heights", "category": "Symphony of Flavors", "description": "A crescendo of culinary delights", "date_opened": date(2025, 1, 15), "visual_id": 19},
    {"name": "Flavorful Ventures", "city": "Ventureville", "category": "Adventurous Dining", "description": "Venture into flavorful experiences", "date_opened": date(2025, 3, 8), "visual_id": 20},
]


def dummy_setup():
    db = database.SessionLocal()
    visuals = populate_visuals(db)
    if crud.count_restaurants(db) < 20:
        populate_restaurants(db)


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


def drinks_menu_items(db, restaurant_id):
    schema = schemas.MenuItemCreate(

    )
    crud.create_restaurant_menu_item(db, schema, restaurant_id)


def populate_restaurant(db, restaurant):
    schema = schemas.RestaurantCreate(**restaurant)
    return crud.create_restaurant(db, schema)


def populate_restaurants(db):
    return [populate_restaurant(db, restaurant) for restaurant in RESTAURANTS]
