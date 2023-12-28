from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field


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
    visual_id: Optional[int] = None


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
    year_opened: int = Field(gt=0, description="Year must be greater than 0", default=1)
    visual_id: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        city: str = Form(...),
        category: str = Form(...),
        description: str = Form(...),
        year_opened: int = Form(...),
        visual_id: int = Form(...),
    ):
        return cls(
            name=name,
            city=city,
            category=category,
            description=description,
            year_opened=year_opened,
            visual_id=visual_id
        )


class Restaurant(RestaurantCreate):
    id: int
    is_active: bool
    menu_items: Optional[list[MenuItem]] = []
    visual: Optional[Visual] = {}

    class Config:
        from_attributes = True
