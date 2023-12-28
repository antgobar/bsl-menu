from typing import Optional

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


class Restaurant(RestaurantCreate):
    id: int
    is_active: bool
    menu_items: Optional[list[MenuItem]] = []
    visual: Optional[Visual] = {}

    class Config:
        from_attributes = True
