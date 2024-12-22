Absence Manager - Face Recognition Based Attendance System

This project is a Python-based application designed to manage student attendance using facial recognition technology. It features an intuitive interface developed with PyQt5 and integrates with a PostgreSQL database for storing and managing user and attendance records.

Table of Contents
Features
Project Structure
Prerequisites
How to Use
Technical Details
Installation Steps
Features
Facial Recognition: Identify and mark attendance using face recognition.
Database Integration: PostgreSQL database for user and attendance records.
Multi-Functional Interfaces:
Manage users
Notify stakeholders
Analyze attendance statistics
Modern Interface: Developed using PyQt5 for a responsive and interactive UI.
Dockerized Deployment: Simplified setup with Docker and Docker Compose.
Project Structure
bash
Copy code
FACE-RECOGNITION-APP/
│
├── app/
│   ├── recorder.py                     
├── mysql/
│   ├── database_students.sql
│   ├── Dockerfile
├── python/
│   ├── AbsenceAnalyticsInterface.py
│   ├── AbsenceManagerHome.py
│   ├── Dockerfile
│   ├── ManageUsersInterface.py
│   ├── Menu.py
│   ├── recorder.py
│   ├── requirements.txt
├── docker-compose.yml                 
└── README.md  # Project documentation
Prerequisites
Install Docker: Download Docker from Docker official website.
Install Docker Compose: Download Docker Compose from Docker Compose official page.
Ensure the following ports are available:
Technical Details
Technologies Used:
Backend: Python (with libraries like face_recognition, psycopg2, PyQt5, etc.)
Database: PostgreSQL
Deployment: Docker and Docker Compose
Database Schema:
Users Table:

id: User ID (Primary Key)
username: Unique username
filiere: Program/field of study
image: Encrypted image data
image_pure: Original image data
accepte: Permission flag
Absence Table:

id_ab: Attendance ID (Primary Key)
id: User ID (Foreign Key)
time: Time of attendance
date: Date of attendance (default: current timestamp)
Installation Steps
xluncher:

Install xluncher
Choose multiple windows display, number 0
Next
Start with no client
Next
Activate "Disable Access Control"
Next
Docker:

Create a custom Docker network:
bash
Copy code
docker network create testg_network
Pull the project Docker image:
bash
Copy code
docker pull jammiosama/face-recognition-app-mysql:latest
docker pull jammiosama/face-recognition-app-pythonapp:latest

docker network create testg_network
docker run --name face-recognition-app-mysql-1 --network testg_network -e MYSQL_ROOT_PASSWORD=root -d jammiosama/face-recognition-app-mysql:latest

Start the Application:

Get the IP address from the terminal of your machine and replace 192.168.0.71 with your actual IP address.
bash
Copy code
docker run --rm --name test-pythonapp --network testg_network -e DISPLAY=192.168.0.71:0 -v /tmp/.X11-unix:/tmp/.X11-unix jammiosama/face-recognition-app-pythonapp:latest
Les corrections apportées incluent :

Correction de l'orthographe de "database_students.sql" dans le répertoire mysql/.
Correction de requitements.txt en requirements.txt.
Clarification des étapes d'installation Docker.
Quelques réorganisations pour la lisibilité, comme l'ajout des liens vers les pages de téléchargement Docker et Docker Compose.