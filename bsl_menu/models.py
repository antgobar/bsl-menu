from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    city = Column(String(60))
    category = Column(String(60))
    description = Column(String(120))
    year_opened = Column(Integer)
    is_active = Column(Boolean, default=True)
    visual_id = Column(Integer, ForeignKey("visuals.id"))
    menu_items = relationship("MenuItem", back_populates="restaurant")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String(120))
    visual_id = Column(Integer, ForeignKey("visuals.id"))

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="menu_items")


class Visual(Base):
    __tablename__ = "visuals"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String(120))
    reference_link = Column(String)
