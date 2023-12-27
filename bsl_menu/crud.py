from . import models, schemas
from .database import DbSession


def create_entity(db: DbSession, model, schema):
    db_entity = model(**schema.model_dump())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def read_entity(db: DbSession, model, entity_id: int):
    return db.query(model).filter(model.id == entity_id).first()


def read_entities(db: DbSession, model, skip: int, limit: int):
    return db.query(model).offset(skip).limit(limit).all()


def search_entities_by_key_value(db: DbSession, model, column, value: str, skip: int, limit: int):
    return db.query(model).filter(column.like(f"%{value}%")).offset(skip).limit(limit).all()


def update_entity(db: DbSession, model, entity_id: int, **field_values):
    db_entity = db.query(model).filter(model.id == entity_id).first()
    if db_entity:
        for field, value in field_values.items():
            db_entity.__dict__[field] = value
        db.commit()
        db.refresh(db_entity)
    return db_entity


def delete_entity(db: DbSession, model, entity_id: int):
    db_entity = db.query(model).filter(model.id == entity_id).first()
    if db_entity:
        db.delete(db_entity)
        db.commit()
    return db_entity


def create_restaurant(db: DbSession, restaurant: schemas.RestaurantCreate):
    return create_entity(db, models.Restaurant, restaurant)


def read_restaurant(db: DbSession, restaurant_id: int):
    return read_entity(db, models.Restaurant, restaurant_id)


def read_restaurants(db: DbSession, skip: int = 0, limit: int = 100):
    return read_entities(db, models.Restaurant, skip, limit)


def search_restaurants_by_name(db: DbSession, name: str, skip: int = 0, limit: int = 100):
    if not name.strip() or not name:
        return []
    return db.query(
        models.Restaurant
    ).filter(models.Restaurant.name.like(f"%{name}%")).offset(skip).limit(limit).all()


def remove_restaurant(db: DbSession, restaurant_id: int):
    return delete_entity(db, models.Restaurant, restaurant_id)


def create_restaurant_menu_item(db: DbSession, menu_item: schemas.MenuItemCreate, restaurant_id: int):
    db_menu_item = models.MenuItem(**menu_item.model_dump(), restaurant_id=restaurant_id)
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def read_menu_item(db: DbSession, menu_item_id: int):
    return read_entity(db, models.MenuItem, menu_item_id)


def read_restaurant_menu(db: DbSession, restaurant_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()


def create_visual(db: DbSession, schema):
    return create_entity(db, models.Visual, schema)


def read_visual(db: DbSession, visual_id: int):
    return read_entity(db, models.Visual, visual_id)


def read_visuals(db: DbSession, skip, limit):
    return read_entities(db, models.Visual, skip=skip, limit=limit)


def update_visual_reference_link(db: DbSession, visual_id: int, reference_link: str):
    visual = read_visual(db, visual_id)
    visual.reference_link = reference_link
    db.commit()
    db.refresh(visual)
    return visual


def remove_visual(db: DbSession, visual_id: int):
    return delete_entity(db, models.Visual, visual_id)
