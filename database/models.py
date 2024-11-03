# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 03, 2024 16:11:46
# Database: sqlite:////tmp/tmp.hQgNbqrhg3/DogWalkerManagementSystem/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Owner(SAFRSBaseX, Base):
    """
    description: Represents a dog owner.
    """
    __tablename__ = 'owner'
    _s_collection_name = 'Owner'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    created_by = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    DogList : Mapped[List["Dog"]] = relationship(back_populates="owner")
    WalkRequestList : Mapped[List["WalkRequest"]] = relationship(back_populates="owner")



class Walker(SAFRSBaseX, Base):
    """
    description: Represents a person who walks dogs for owners.
    """
    __tablename__ = 'walker'
    _s_collection_name = 'Walker'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    price_for_small = Column(Float, nullable=False)
    price_for_medium = Column(Float, nullable=False)
    price_for_large = Column(Float, nullable=False)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    created_by = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    WalkRequestList : Mapped[List["WalkRequest"]] = relationship(back_populates="walker")



class Dog(SAFRSBaseX, Base):
    """
    description: Represents a dog owned by a dog owner.
    """
    __tablename__ = 'dog'
    _s_collection_name = 'Dog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    size = Column(String, nullable=False)
    notes = Column(String)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    created_by = Column(String)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("DogList"))

    # child relationships (access children)
    WalkRequestList : Mapped[List["WalkRequest"]] = relationship(back_populates="dog")



class WalkRequest(SAFRSBaseX, Base):
    """
    description: Represents a walk request from an owner for their dog(s).
    """
    __tablename__ = 'walk_request'
    _s_collection_name = 'WalkRequest'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    dog_id = Column(ForeignKey('dog.id'), nullable=False)
    walker_id = Column(ForeignKey('walker.id'))
    status = Column(String)
    day_of_week = Column(String, nullable=False)
    time_of_day = Column(String, nullable=False)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)
    created_by = Column(String)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("WalkRequestList"))
    owner : Mapped["Owner"] = relationship(back_populates=("WalkRequestList"))
    walker : Mapped["Walker"] = relationship(back_populates=("WalkRequestList"))

    # child relationships (access children)
