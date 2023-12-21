from sqlalchemy.orm import Session

from . import models, schemas


def read_entity(db: Session, model, entity_id: int):
    return db.query(model).filter(model.id == entity_id).first()


def read_entities(db: Session, model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def search_entities_by_key_value(db: Session, model, key: str, value: str, skip: int = 0, limit: int = 100):
    return db.query(model).filter(model[key].like(f"%{value}%")).offset(skip).limit(limit).all()


def create_entity(db: Session, model, schema):
    db_entity = model(**schema.model_dump())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def update_entity(db: Session, model, entity_id: int, **field_values):
    db_entity = db.query(model).filter(model.id == entity_id).first()
    if db_entity:
        for field, value in field_values.items():
            db_entity[field] = value
        db.commit()
        db.refresh(db_entity)
    return db_entity


def delete_entity(db: Session, model, entity_id: int):
    db_entity = db.query(model).filter(model.id == entity_id).first()
    if db_entity is not None:
        db.delete(db_entity)
        db.commit()
    return db_entity


######################################
def create_restaurant(db: Session, restaurant: schemas.CreateRestaurant):
    db_restaurant = models.Restaurant(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def read_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()


def read_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit).all()


def search_restaurants_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).filter(models.Restaurant.name.like(f"%{name}%")).offset(skip).limit(limit).all()


def update_restaurant(db: Session, restaurant_id: int, **field_values):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if db_restaurant:
        for field, value in field_values.items():
            if field in schemas.Restaurant.model_fields:
                db_restaurant[field] = value
        db.commit()
        db.refresh(db_restaurant)
    return db_restaurant


def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if db_restaurant is not None:
        db.delete(db_restaurant)
        db.commit()
    return db_restaurant


def create_restaurant_menu_item(db: Session, menu_item: schemas.CreateMenuItem, restaurant_id: int):
    db_menu_item = models.MenuItem(**menu_item.model_dump(), restaurant_id=restaurant_id)
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def read_menu_item(db: Session, menu_item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id).first()


def read_restaurant_menu_item(db: Session, restaurant_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()


def update_restaurant_menu_item(db: Session, restaurant_id: int, menu_item_id: int, **field_values):
    db_menu_item = db.query(
        models.MenuItem
    ).filter(
        models.MenuItem.restaurant_id == restaurant_id, models.MenuItem.id == menu_item_id
    ).first()

    if db_menu_item:
        for field, value in field_values.items():
            if field in schemas.MenuItem.model_fields:
                db_menu_item[field] = value
        db.commit()
        db.refresh(db_menu_item)
    return db_menu_item


def create_visual(db: Session, schema):
    return create_entity(db, models.Visual, schema)


def read_visual(db: Session, visual_id: int):
    return read_entity(db, models.Visual, visual_id)


def read_visuals(db: Session, skip, limit):
    return read_entities(db, models.Visual, skip=skip, limit=limit)
