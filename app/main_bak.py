from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models import DoctorImageValidation, SessionLocal, engine, Base
from app.schemas import DoctorImageValidationResponse
from typing import Optional
import os
import shutil
import pandas as pd
from typing import List
from fastapi import Query
from fastapi.responses import FileResponse
from fastapi import FastAPI, Form, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models import Doctor  # Import your Doctor model
from app.schemas import DoctorSchema  # Import your Doctor schema if you have one
from app.models import SessionLocal  # Import SessionLocal
from sqlalchemy import inspect, text  # Import inspect and text
from app.models import Doctor, SessionLocal
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
import logging
# No need to recreate tables here, model.py does it
# Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

Ipp = [
    "http://localhost:8080",  # The origin where your frontend might be served
    "http://localhost:8000",  # Add the origin where your frontend is actually making requests from
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development, specify origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.mount("/images", StaticFiles(directory="images"), name="images")

# @app.get("/categorize_image/", response_model=DoctorImageValidationResponse)
# async def categorize_image(db: Session = Depends(get_db)):
#     """
#     Retrieves the first uncategorized image from the database.
#     """
#     db_entry = db.query(DoctorImageValidation).filter(DoctorImageValidation.doctor_name == None).order_by(DoctorImageValidation.id).first()
#     if db_entry is None:
#         raise HTTPException(status_code=404, detail="No new images to categorize")
#     return db_entry

# @app.get("/categorize_image/", response_model=Optional[DoctorImageValidationResponse])
# async def get_first_uncategorized_image():
#     """
#     Retrieves the first image from the 'images' directory. No database entry is created yet.
#     """
#     images_dir = "images"
#     image_files = sorted([f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))])
#     if image_files:
#         global current_image_filename
#         current_image_filename = image_files[0]
#         return DoctorImageValidationResponse(id=None, image_path=os.path.join("images", current_image_filename), doctor_name=None, rating=None, comments=None, disease_name=None, category=None)
#     else:
#         raise HTTPException(status_code=404, detail="No images to categorize found.")

# @app.get("/categorize_image/{current_displayed_filename}", response_model=Optional[DoctorImageValidationResponse])
# async def get_next_uncategorized_image(current_displayed_filename: str):
#     """
#     Retrieves the next image from the 'images' directory. No database entry is created yet.
#     """
#     images_dir = "images"
#     image_files = sorted([f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))])

#     try:
#         current_index = image_files.index(current_displayed_filename)
#         if current_index < len(image_files) - 1:
#             global current_image_filename
#             current_image_filename = image_files[current_index + 1]
#             return DoctorImageValidationResponse(id=None, image_path=os.path.join("images", current_image_filename), doctor_name=None, rating=None, comments=None, disease_name=None, category=None)
#         else:
#             return None  # No more images
#     except ValueError:
#         return None # Current image file not found in directory



# @app.get("/categorize_image/{current_displayed_filename}", response_model=Optional[DoctorImageValidationResponse])
# async def get_next_uncategorized_image(current_displayed_filename: str):
#     """
#     Retrieves the next uncategorized image from the 'images' directory.
#     """
#     images_dir = "images"
#     uncategorized_files = sorted([
#         f for f in os.listdir(images_dir)
#         if os.path.isfile(os.path.join(images_dir, f))
#         and f not in ["disease", "non-disease"]  # Exclude subdirectory names
#     ])

#     try:
#         if current_displayed_filename in uncategorized_files:
#             current_index = uncategorized_files.index(current_displayed_filename)
#             if current_index < len(uncategorized_files) - 1:
#                 next_image_filename = uncategorized_files[current_index + 1]
#                 return DoctorImageValidationResponse(
#                     id=None,
#                     image_path=os.path.join("images", next_image_filename),
#                     doctor_name=None,
#                     rating=None,
#                     comments=None,
#                     disease_name=None,
#                     category=None
#                 )
#             else:
#                 return None  # No more uncategorized images
#         else:
#             # If the current file is not found in the uncategorized list (already moved)
#             # Return the first uncategorized image if available
#             if uncategorized_files:
#                 first_image_filename = uncategorized_files[0]
#                 return DoctorImageValidationResponse(
#                     id=None,
#                     image_path=os.path.join("images", first_image_filename),
#                     doctor_name=None,
#                     rating=None,
#                     comments=None,
#                     disease_name=None,
#                     category=None
#                 )
#             else:
#                 return None
#     except ValueError:
#         # Should not happen now with the 'in' check, but as a fallback
#         if uncategorized_files:
#             first_image_filename = uncategorized_files[0]
#             return DoctorImageValidationResponse(
#                 id=None,
#                 image_path=os.path.join("images", first_image_filename),
#                 doctor_name=None,
#                 rating=None,
#                 comments=None,
#                 disease_name=None,
#                 category=None
#             )
#         else:
#             return None

# @app.get("/categorize_image/", response_model=Optional[DoctorImageValidationResponse])
# async def get_first_uncategorized_image():
#     """
#     Retrieves the first uncategorized image from the 'images' directory.
#     """
#     images_dir = "images"
#     uncategorized_files = sorted([
#         f for f in os.listdir(images_dir)
#         if os.path.isfile(os.path.join(images_dir, f))
#         and f not in ["disease", "non-disease"]  # Exclude subdirectory names
#     ])
#     if uncategorized_files:
#         first_image_filename = uncategorized_files[0]
#         return DoctorImageValidationResponse(
#             id=None,
#             image_path=os.path.join("images", first_image_filename),
#             doctor_name=None,
#             rating=None,
#             comments=None,
#             disease_name=None,
#             category=None
#         )
#     else:
#         raise HTTPException(status_code=404, detail="No images to categorize found.")
    
def find_image_pair(directory="images"):
    all_files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f not in ["disease", "non-disease"]])
    processed = set()
    for filename in all_files:
        if filename in processed:
            continue
        name, ext = os.path.splitext(filename)
        mask_filename = f"{name}_mask{ext}"
        if mask_filename in all_files:
            processed.add(filename)
            processed.add(mask_filename)
            yield filename, mask_filename

@app.get("/categorize_image/{current_displayed_filename}", response_model=Optional[DoctorImageValidationResponse])
async def get_next_uncategorized_image(current_displayed_filename: str):
    image_pairs = list(find_image_pair())
    current_base_filename, _ = os.path.splitext(current_displayed_filename)
    current_pair = None
    for base, mask in image_pairs:
        if os.path.splitext(base)[0] == current_base_filename:
            current_pair = (base, mask)
            break

    if current_pair:
        current_index = image_pairs.index(current_pair)
        if current_index < len(image_pairs) - 1:
            next_base, next_mask = image_pairs[current_index + 1]
            return DoctorImageValidationResponse(
                id=None,
                image_path=os.path.join("images", next_base),
                mask_path=os.path.join("images", next_mask),
                doctor_name=None,
                rating=None,
                comments=None,
                mask_comments=None,
                disease_name=None,
                category=None
            )
    elif image_pairs:
        first_base, first_mask = image_pairs[0]
        return DoctorImageValidationResponse(
            id=None,
            image_path=os.path.join("images", first_base),
            mask_path=os.path.join("images", first_mask),
            doctor_name=None,
            rating=None,
            comments=None,
            mask_comments=None,
            disease_name=None,
            category=None
        )
    return None

@app.get("/categorize_image/", response_model=Optional[DoctorImageValidationResponse])
async def get_first_uncategorized_image():
    image_pairs = list(find_image_pair())
    if image_pairs:
        first_base, first_mask = image_pairs[0]
        return DoctorImageValidationResponse(
            id=None,
            image_path=os.path.join("images", first_base),
            mask_path=os.path.join("images", first_mask),
            doctor_name=None,
            rating=None,
            comments=None,
            mask_comments=None,
            disease_name=None,
            category=None
        )
    raise HTTPException(status_code=404, detail="No image pairs to categorize found.")
# @app.post("/categorize_image/")
# async def submit_categorization(
# current_filename: str = Form(...), # Receive the filename
# doctor_name: str = Form(...),
# rating: int = Form(...),
# comments: Optional[str] = Form(None),
# disease_name: str = Form(...),
# category: str = Form(...),
# db: Session = Depends(get_db)
# ):
# """
# Saves the categorization details to the database and moves the image file,
# handling potential filename collisions.
# """
# db_image = DoctorImageValidation(
# image_path=os.path.join("images", current_filename), # Use the submitted filename
# doctor_name=doctor_name,
# rating=rating,
# comments=comments,
# disease_name=disease_name,
# category=category
# )
# db.add(db_image)
# db.commit()
# db.refresh(db_image)
# image_id = db_image.id

# source_path = os.path.join("images", current_filename) # Use the submitted filename
# destination_dir = os.path.join("images", category)
# os.makedirs(destination_dir, exist_ok=True)
# destination_path = os.path.join(destination_dir, current_filename)

# # Check if the destination file already exists
# if os.path.exists(destination_path):
# name, ext = os.path.splitext(current_filename)
# counter = 1
# while True:
# new_filename = f"{name}_{counter}{ext}"
# new_destination_path = os.path.join(destination_dir, new_filename)
# if not os.path.exists(new_destination_path):
# destination_path = new_destination_path
# current_filename = new_filename
# break
# counter += 1

# try:
# shutil.move(source_path, destination_path)
# db_image.image_path = os.path.join("images", category, current_filename)
# db.commit()
# return {"message": f"Image categorized as {category} and moved to {current_filename}.", "image_id": image_id}
# except FileNotFoundError:
# db.rollback()
# raise HTTPException(status_code=404, detail=f"Source file not found: {source_path}")
# except Exception as e:
# db.rollback()
# print(f"Error moving file: {e}")
# raise HTTPException(status_code=500, detail="Failed to move image")
@app.post("/categorize_image/")
async def submit_categorization(
    current_filename: str = Form(...), # Base filename (without _mask)
    doctor_name: str = Form(...),
    rating: int = Form(...),
    comments: Optional[str] = Form(None),
    mask_comments: Optional[str] = Form(None),
    disease_name: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    base_name, ext = os.path.splitext(current_filename)
    original_filename = f"{base_name}{ext}"
    mask_filename = f"{base_name}_mask{ext}"

    db_image = DoctorImageValidation(
        image_path=os.path.join("images", original_filename),
        mask_path=os.path.join("images", mask_filename),
        doctor_name=doctor_name,
        rating=rating,
        comments=comments,
        mask_comments=mask_comments,
        disease_name=disease_name,
        category=category
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    image_id = db_image.id

    source_original_path = os.path.join("images", original_filename)
    source_mask_path = os.path.join("images", mask_filename)
    destination_dir = os.path.join("images", category)
    os.makedirs(destination_dir, exist_ok=True)
    destination_original_path = os.path.join(destination_dir, original_filename)
    destination_mask_path = os.path.join(destination_dir, mask_filename)

    def move_file_with_collision_handling(source, destination):
        if os.path.exists(destination):
            name, ext = os.path.splitext(os.path.basename(source))
            counter = 1
            while True:
                new_filename = f"{name}_{counter}{ext}"
                new_destination = os.path.join(os.path.dirname(destination), new_filename)
                if not os.path.exists(new_destination):
                    destination = new_destination
                    return destination, new_filename #changed to return destination, new_filename
                counter += 1
        return destination, os.path.basename(source) #added return os.path.basename(source)

    try:
        new_original_path, new_original_filename = move_file_with_collision_handling(source_original_path, destination_original_path)
        new_mask_path, new_mask_filename = move_file_with_collision_handling(source_mask_path, destination_mask_path)

        os.rename(source_original_path, new_original_path) # Added os.rename
        os.rename(source_mask_path, new_mask_path)     # Added os.rename

        db_image.image_path = os.path.join("images", category, new_original_filename)
        db_image.mask_path = os.path.join("images", category, new_mask_filename)
        db.commit()

        return {"message": f"Images categorized as {category} and moved.", "image_id": image_id}
    except FileNotFoundError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Source file not found: {e.filename}")
    except Exception as e:
        db.rollback()
        print(f"Error moving files: {e}")
        raise HTTPException(status_code=500, detail="Failed to move images")

@app.get("/disease_images/{disease_name}", response_model=List[DoctorImageValidationResponse])
async def get_disease_images(disease_name: str, db: Session = Depends(get_db)):
    """
    Retrieves images for a specific disease.  This will return both original
    and mask images, and all the details stored in the database.
    """
    # Query the database for entries matching the disease_name
    images = db.query(DoctorImageValidation).filter(DoctorImageValidation.disease_name == disease_name).all()
    return images  # Return the raw database objects, Pydantic will format them

@app.post("/update_image_details/{image_id}")
async def update_image_details(
    image_id: int,
    doctor_name: str = Form(...),
    rating: int = Form(...),
    comments: Optional[str] = Form(None),
    mask_comments: Optional[str] = Form(None),
    disease_name: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Updates the details of an image in the database and moves the image files
    if the category has changed.
    """
    db_image = db.query(DoctorImageValidation).filter(DoctorImageValidation.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    old_category = db_image.category  # Store the old category
    old_image_path = db_image.image_path
    old_mask_path = db_image.mask_path

    # Update the database record
    db_image.doctor_name = doctor_name
    db_image.rating = rating
    db_image.comments = comments
    db_image.mask_comments = mask_comments
    db_image.disease_name = disease_name
    db_image.category = category
    db.commit()  # Commit the changes *before* moving files

    # Move files if the category has changed
    if old_category != category:
        try:
            # Define source and destination directories
            source_original_path = os.path.join(old_image_path)
            source_mask_path = os.path.join(old_mask_path)
            destination_dir = os.path.join("images", category)  # Correct destination
            os.makedirs(destination_dir, exist_ok=True)
            destination_original_path = os.path.join(destination_dir, os.path.basename(old_image_path))
            destination_mask_path = os.path.join(destination_dir, os.path.basename(old_mask_path))

            def move_file_with_collision_handling(source, destination):
                if os.path.exists(destination):
                    name, ext = os.path.splitext(os.path.basename(source))
                    counter = 1
                    while True:
                        new_filename = f"{name}_{counter}{ext}"
                        new_destination = os.path.join(os.path.dirname(destination), new_filename)
                        if not os.path.exists(new_destination):
                            destination = new_destination
                            return destination, os.path.basename(new_filename)
                        counter += 1
                return destination, os.path.basename(source)

            new_original_path, new_original_filename = move_file_with_collision_handling(source_original_path, destination_original_path)
            new_mask_path, new_mask_filename = move_file_with_collision_handling(source_mask_path, destination_mask_path)
           
            os.rename(source_original_path, new_original_path)
            os.rename(source_mask_path, new_mask_path)

            # Update the database with the new paths
            db_image.image_path = os.path.join("images", category, new_original_filename)
            db_image.mask_path = os.path.join("images", category, new_mask_filename)
            db.commit()

        except FileNotFoundError as e:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Source file not found: {e.filename}")
        except Exception as e:
            db.rollback()
            logging.error(f"Error moving files: {e}")
            raise HTTPException(status_code=500, detail="Failed to move images")

    db.refresh(db_image)
    return {"message": "Image details updated successfully", "image_id": image_id}




@app.get("/download_excel/")
async def download_categorizations_excel(db: Session = Depends(get_db)):
    """
    Downloads all categorization entries from the database as an Excel file.
    """
    categorizations = db.query(DoctorImageValidation).all()
    if not categorizations:
        raise HTTPException(status_code=404, detail="No categorizations found in the database.")

    # Convert the database entries to a list of dictionaries
    data = [entry.__dict__ for entry in categorizations]
    # Remove the SQLAlchemy internal attributes
    for row in data:
        row.pop('_sa_instance_state', None)

    df = pd.DataFrame(data)
    excel_file_path = "categorization_data.xlsx"
    df.to_excel(excel_file_path, index=False)

    return FileResponse(excel_file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="categorization_data.xlsx")


# @app.get("/filter_entries/", response_model=List[DoctorImageValidationResponse])
# async def filter_categorizations(category: str = Query(...), disease_name: Optional[str] = Query(None), db: Session = Depends(get_db)):
#     """
#     Filters categorization entries by category and optionally by disease name.
#     """
#     query = db.query(DoctorImageValidation).filter(DoctorImageValidation.category == category)
#     if disease_name:
#         query = query.filter(DoctorImageValidation.disease_name == disease_name)
#     results = query.all()
#     return results

@app.get("/filter_entries/", response_model=List[DoctorImageValidationResponse])
async def filter_categorizations(
    category: str = Query(...),
    disease_name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Filters categorization entries by category and optionally by disease name.
    Returns a list of DoctorImageValidationResponse objects, which should include
    image_path, mask_path, and all the fields needed for the HTML.
    """
    query = db.query(DoctorImageValidation).filter(DoctorImageValidation.category == category)
    if disease_name:
        query = query.filter(DoctorImageValidation.disease_name == disease_name)
    results = query.all()

    # Ensure the results are correctly formatted as DoctorImageValidationResponse
    formatted_results = []
    for result in results:
        formatted_results.append(DoctorImageValidationResponse(
            id=result.id,
            image_path=result.image_path,
            mask_path=result.mask_path,
            doctor_name=result.doctor_name,
            rating=result.rating,
            comments=result.comments,
            mask_comments=result.mask_comments,
            disease_name=result.disease_name,
            category=result.category,
            created_at=result.created_at,
        ))
    return formatted_results



@app.get("/all_categorizations/", response_model=List[DoctorImageValidationResponse])
async def get_all_categorizations(db: Session = Depends(get_db)):
    """
    Retrieves all categorization entries from the database.
    """
    return db.query(DoctorImageValidation).all()

@app.get("/disease_names/", response_model=List[str])
async def get_disease_names(db: Session = Depends(get_db)):
    """
    Retrieves all distinct disease names from the database.
    """
    # Use distinct() on the disease_name column and extract the values
    disease_names = db.query(DoctorImageValidation.disease_name).distinct().all()
    # Convert the result (list of tuples) to a list of strings
    return [row[0] for row in disease_names]


@app.post("/register_doctor/")
async def register_doctor(
    doctorName: str = Form(...),
    hospital: Optional[str] = Form(None),
    hospitalAddress: Optional[str] = Form(None),
    contactNumber: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    specialization: Optional[str] = Form(None),
    registrationId: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Registers a new doctor in the database.
    """
    # Check if the registration ID already exists
    if db.query(Doctor).filter(Doctor.registration_id == registrationId).first():
        raise HTTPException(status_code=400, detail="Registration ID already exists")

    # Create a new Doctor instance
    db_doctor = Doctor(
        doctor_name=doctorName,
        hospital=hospital,
        hospital_address=hospitalAddress,
        contact_number=contactNumber,
        email=email,
        specialization=specialization,
        registration_id=registrationId,
    )

    # Add the doctor to the database
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)  # Get the newly created doctor instance with the ID

    return {"message": "Doctor registered successfully", "doctor_id": db_doctor.id}
    #except Exception as e:
    #    db.rollback()
    #    raise HTTPException(status_code=500, detail=f"Failed to register doctor: {e}")

@app.get("/doctors/", response_model=List[DoctorSchema])
async def get_doctors(db: Session = Depends(get_db)):
    """
    Retrieves all doctors from the database.
    """
    doctors = db.query(Doctor).all()
    return doctors


@app.delete("/doctors/")
async def delete_doctors_table(db: Session = Depends(get_db)):
    """
    Deletes the doctors table from the database.
    """
    inspector = inspect(db.bind)
    if not inspector.has_table("doctors"):
        raise HTTPException(status_code=404, detail="Doctors table not found")

    # Use a raw SQL query to delete the table
    try:
        db.execute(text("DROP TABLE doctors"))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete table: {e}")

    return {"message": "Doctors table deleted successfully"}


def drop_table(db: Session, table_name: str):
    """
    Drops the specified table from the database.

    Args:
        db: The database session.
        table_name: The name of the table to drop.
    """
    try:
        if table_name == 'doctor_image_validation':
            DoctorImageValidation.__table__.drop(bind=engine)
        elif table_name == 'doctors':
            Doctor.__table__.drop(bind=engine)
        else:
            raise HTTPException(status_code=400, detail=f"Table '{table_name}' not found.")
        db.commit()  # Commit the changes after dropping the table
        logging.info(f"Table '{table_name}' dropped successfully.")
    except OperationalError as e:
        logging.error(f"Error dropping table '{table_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to drop table '{table_name}': {e}")
    except Exception as e:
        logging.error(f"Unexpected error dropping table '{table_name}': {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.delete("/delete_table/{table_name}")
def delete_table_route(table_name: str, db: Session = Depends(get_db)):
    """
    Deletes the specified table.

    Args:
        table_name: The name of the table to delete ('doctor_image_validation' or 'doctors').
        db: The database session.

    Returns:
        A dictionary indicating the result of the operation.
    """
    if table_name not in ('doctor_image_validation', 'doctors'):
        raise HTTPException(status_code=400, detail="Invalid table name.  Must be 'doctor_image_validation' or 'doctors'.")

    drop_table(db, table_name)
    return {"message": f"Table '{table_name}' has been deleted."}

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)  # Configure logging
    uvicorn.run(app, host="0.0.0.0", port=8000)


