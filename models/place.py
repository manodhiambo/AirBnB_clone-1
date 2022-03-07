#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Float, Integer, Table, ForeignKey, String, Column
from sqlalchemy.orm import relationship
import models


place_amenity = Table('place_amenity', Base.metadata, Column(
    'place_id', String(60), ForeignKey(
        'places.id'), primary_key=True, nullable=False), Column(
            'amenity_id', String(60), ForeignKey(
                'amenities.id'), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """Return list of reviews"""

            review_list = [value for key, value in models.storage.
                           all(Review).items() if value.place_id == self.id]

            return review_list

        @property
        def amenities(self):
            """ Getter attribute amenities that returns the list of Amenity
            instances based on the attribute amenity_ids that contains all
            Amenity.id linked to the Place """
            amenity_list = [value for key, value in models.storage.
                            all(Amenity).items() if value.place_id == self.id]

            return amenity_list

        @amenities.setter
        def amenities(self, amenity_obj):
            """
            Setter attribute amenities that handles append method for adding an
            Amenity.id o the attribute amenity_ids
            """
            if isinstance(amenity_obj, models.Amenity):
                self.amenities.append(amenity_obj.id)
