from pydantic import BaseModel, Field


class CreateMenuItem(BaseModel):
    name: str
    description: str
    visual_id: int


class MenuItem(CreateMenuItem):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True


class CreateRestaurant(BaseModel):
    name: str
    city: str
    category: str
    description: str
    year_opened: int = Field(gt=0, description="Year must be greater than 0")
    is_active: bool
    visual_id: int | None


class Restaurant(CreateRestaurant):
    id: int
    menu_items: list[MenuItem] = []

    class Config:
        orm_mode = True


class CreateVisual(BaseModel):
    name: str
    description: str
    reference_link: str


class Visual(CreateVisual):
    id: int
