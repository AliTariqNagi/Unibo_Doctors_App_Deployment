from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import EmailStr
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
DATABASE_URL = "postgresql://admin:admin@localhost/doctor_image_validation"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the Doctor model (SQLAlchemy model) - Ensure this matches your database
class Doctor(Base):
    __tablename__ = "doctors"  # Make sure this matches your actual table name
    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String, nullable=False)
    hospital = Column(String)
    hospital_address = Column(String)
    contact_number = Column(String)
    email = Column(String)  # Changed back to String
    specialization = Column(String)
    registration_id = Column(String, nullable=False, unique=True)


# class DoctorImageValidation(Base):
#     __tablename__ = "doctor_image_validation"

#     id = Column(Integer, primary_key=True, index=True)
#     image_path = Column(String)
#     doctor_name = Column(String, nullable=True)
#     rating = Column(Integer, nullable=True)
#     comments = Column(String, nullable=True)
#     disease_name = Column(String)
#     category = Column(String, nullable=True)  # Ensure this line exists


class DoctorImageValidation(Base):
    __tablename__ = "doctor_image_validation"

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String)
    mask_path = Column(String)
    doctor_name = Column(String)
    rating = Column(Integer)
    comments = Column(String)
    mask_comments = Column(String)
    disease_name = Column(String)
    category = Column(String)
    created_at = Column(DateTime, server_default=func.now())



# Create the database tables
Base.metadata.create_all(bind=engine)


