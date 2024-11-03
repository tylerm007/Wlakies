# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime

logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


class Walker(Base):
    """description: Represents a person who walks dogs for owners."""
    __tablename__ = 'walker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    price_for_small = Column(Float, nullable=False)
    price_for_medium = Column(Float, nullable=False)
    price_for_large = Column(Float, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String, nullable=True)


class Owner(Base):
    """description: Represents a dog owner."""
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String, nullable=True)


class Dog(Base):
    """description: Represents a dog owned by a dog owner."""
    __tablename__ = 'dog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    size = Column(String, nullable=False)  # Values: small, medium, large
    notes = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String, nullable=True)


class WalkRequest(Base):
    """description: Represents a walk request from an owner for their dog(s)."""
    __tablename__ = 'walk_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    dog_id = Column(Integer, ForeignKey('dog.id'), nullable=False)
    walker_id = Column(Integer, ForeignKey('walker.id'), nullable=True)  # Initially null until assigned
    status = Column(String, default="Pending")
    day_of_week = Column(String, nullable=False)  # Values: Mon, Tues, Wed, Thurs, Fri, Sat, Sun
    time_of_day = Column(String, nullable=False)  # Values: morning, afternoon
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String, nullable=True)


# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

walker1 = Walker(
    first_name="John",
    last_name="Doe",
    postal_code="12345",
    phone="123-456-7890",
    email="john.doe@example.com",
    max_dogs_per_walk=3,
    price_for_small=15.0,
    price_for_medium=20.0,
    price_for_large=25.0,
    created_by="system_admin"
)

walker2 = Walker(
    first_name="Jane",
    last_name="Smith",
    postal_code="54321",
    phone="987-654-3210",
    email="jane.smith@example.com",
    max_dogs_per_walk=2,
    price_for_small=12.0,
    price_for_medium=18.0,
    price_for_large=24.0,
    created_by="system_admin"
)

owner1 = Owner(
    name="Alice Johnson",
    address="789 Oak Street",
    phone="555-123-4567",
    email="alice.johnson@example.com",
    created_by="system_admin"
)

owner2 = Owner(
    name="Bob Williams",
    address="456 Pine Avenue",
    phone="555-987-6543",
    email="bob.williams@example.com",
    created_by="system_admin"
)

dog1 = Dog(
    owner_id=1,
    name="Buddy",
    breed="Golden Retriever",
    size="large",
    notes="Loves to play fetch",
    created_by="system_admin"
)

dog2 = Dog(
    owner_id=1,
    name="Charlie",
    breed="Beagle",
    size="medium",
    notes="Very friendly",
    created_by="system_admin"
)

walk_request1 = WalkRequest(
    owner_id=1,
    dog_id=1,
    day_of_week="Mon",
    time_of_day="morning",
    created_by="alice.johnson"
)

walk_request2 = WalkRequest(
    owner_id=2,
    dog_id=2,
    day_of_week="Wed",
    time_of_day="afternoon",
    created_by="bob.williams"
)


session.add_all([walker1, walker2, owner1, owner2, dog1, dog2, walk_request1, walk_request2])
session.commit()
