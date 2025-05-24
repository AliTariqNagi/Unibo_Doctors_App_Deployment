# Unibo_Doctors_Application

# Setting Up the DB
sudo apt update   
sudo apt install postgresql postgresql-contrib  
sudo systemctl status postgresql  
sudo -i -u postgres  
psql  
CREATE DATABASE doctor_image_validation;  
CREATE USER admin WITH PASSWORD 'admin';  
GRANT ALL PRIVILEGES ON DATABASE doctor_image_validation TO admin;  
\q  

# Running the project
Running the frontend server  
cd frontend  
python3 -m http.server 8080  
  
Running the Backend server  
uvicorn app.main:app --reload  


# Running the Project for the first time
Move images from the Unibo_Doctors_Application/images/disease and Unibo_Doctors_Application/images/non-disease folders to Unibo_Doctors_Application/images


# Application
From the browser please enter the address
http://localhost:8080/main.html  
Username: admin  
Password: password  
