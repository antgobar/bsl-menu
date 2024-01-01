from typing import Optional
from datetime import date

from fastapi import Form
from pydantic import BaseModel


class VisualCreate(BaseModel):
    name: str
    description: str
    reference_link: str


class Visual(VisualCreate):
    id: int


class MenuItemCreate(BaseModel):
    name: str
    category: str
    description: str
    price: float
    visual_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        category: str = Form(...),
        description: str = Form(...),
        visual_id: int = Form(...),
        price: float = Form(...)
    ):
        return cls(
            name=name,
            category=category,
            description=description,
            price=price,
            visual_id=visual_id
        )


class MenuItem(MenuItemCreate):
    id: int
    visual: Visual = {}
    restaurant_id: int

    class Config:
        from_attributes = True


class RestaurantCreate(BaseModel):
    name: str
    city: str
    category: str
    description: str
    date_opened: date
    visual_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        city: str = Form(...),
        category: str = Form(...),
        description: str = Form(...),
        date_opened: date = Form(...),
        visual_id: int = Form(...),
    ):
        return cls(
            name=name,
            city=city,
            category=category,
            description=description,
            date_opened=date_opened,
            visual_id=visual_id
        )


class Restaurant(RestaurantCreate):
    id: int
    is_active: bool
    menu_items: Optional[list[MenuItem]] = []
    visual: Optional[Visual] = {}

    class Config:
        from_attributes = True
