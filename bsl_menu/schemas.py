from pydantic import BaseModel, Field


class MenuItemCreate(BaseModel):
    name: str
    description: str
    visual_id: int


class MenuItem(MenuItemCreate):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True


class RestaurantCreate(BaseModel):
    name: str
    city: str
    category: str
    description: str
    year_opened: int = Field(gt=0, description="Year must be greater than 0")
    is_active: bool
    visual_id: int | None = None


class Restaurant(RestaurantCreate):
    id: int
    menu_items: list[MenuItem] = []

    class Config:
        from_attributes = True


class VisualCreate(BaseModel):
    name: str
    description: str
    reference_link: str


class Visual(VisualCreate):
    id: int
