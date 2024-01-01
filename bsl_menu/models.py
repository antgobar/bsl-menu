from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

from .database import Base, engine


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    city = Column(String(60))
    category = Column(String(60))
    description = Column(String(120))
    date_opened = Column(Date)
    is_active = Column(Boolean, default=True)

    visual_id = Column(Integer, ForeignKey("visuals.id"), nullable=True)
    visual = relationship("Visual", backref="restaurants")

    # menu_items = relationship("MenuItem", back_populates="restaurant")
    menu_items = relationship("MenuItem", backref="restaurant")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    category = Column(String(20))
    description = Column(String(120))
    price = Column(Float)

    visual_id = Column(Integer, ForeignKey("visuals.id"), nullable=True)
    visual = relationship("Visual", backref="menu_items")

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    # restaurant = relationship("Restaurant", back_populates="menu_items")


class Visual(Base):
    __tablename__ = "visuals"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String(120))
    reference_link = Column(String, unique=True)


Base.metadata.create_all(bind=engine)
