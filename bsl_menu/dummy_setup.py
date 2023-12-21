import random

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


def add_dummy_data(no: int = 3):
    db = database.SessionLocal()
    for _ in range(no):
        restaurant = dummy_restaurant(schemas)
        results = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant.name).all()
        if len(results) == 0:
            crud.create_restaurant(db=db, restaurant=restaurant)
    db.close()


def generate_description():
    lorem = LOREM.replace("\n", "").split(". ")
    selected_length = random.randint(0, len(lorem))
    return ". ".join(lorem[:selected_length])


def dummy_restaurant(schemas):
    city = random.choice(CITIES)
    category = random.choice(CUISINES)
    locale = random.choice(LOCALES)
    return schemas.CreateRestaurant(
        name=f"The {city} {category} {locale}",
        city=city,
        category=category,
        description=generate_description(),
        year_opened=random.choice(YEARS_OPENED),
        is_active=True,
        visual_source_id=random.randint(1, 10)
    )
