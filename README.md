Absence Manager - Face Recognition Based Attendance System
This project is a Python-based application designed to manage student attendance using facial recognition technology. It features an intuitive interface developed with PyQt5 and integrates with a PostgreSQL database for storing and managing user and attendance records.



Table of Contents
Features
Project Structure
Prerequisites
Installation Steps
How to Use
Technical Details




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
project/
│
├── classe/
│   ├── Menu.py                     # Main entry point for the application
│   ├── AbsenceAnalyticsInterface.py # Interface for attendance analytics
│   ├── AbsenceManagerHome.py        # Home interface
│   ├── ManageUsersInterface.py      # User management interface
│   ├── NotifiInterface.py           # Notification management interface
│   ├── recorder.py                  # Script for face recognition and attendance marking
│
├── .env                             # Environment variables for PostgreSQL configuration
├── Dockerfile                       # Instructions to build the application image
├── docker-compose.yml               # Docker Compose configuration
├── requirements.txt                 # requirement.tx
└── README.md                        # Project documentation






Prerequisites
Install Docker: Download Docker
Install Docker Compose: Download Docker Compose
Ensure the following ports are available:
8000: For the application.
5432: For PostgreSQL.
8080: For Adminer (optional database UI).




Installation Steps
cd absence-manager
1. Configure Environment Variables
Create a .env file in the root directory with the following content:

POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
POSTGRES_DB=miniproject
DATABASE_URL=postgresql://docker:docker@database:5432/miniproject
2. Build Docker Containers
Build the application and database containers:

docker-compose build
3. Start the Application
Run all services using Docker Compose:

docker-compose up



How to Use
Access the Application:

Open the application UI by launching the Menu.py script. This will initialize the main interface for attendance management.
Adminer Database Management (Optional):

Adminer (if included) can be accessed at http://localhost:8080 for database management. Use:
System: PostgreSQL
Server: database
Username: docker
Password: docker
Database: miniproject
Record Attendance:

From the home interface, navigate to the Attendance Recording feature, which uses the recorder.py script.
View Analytics:

Analyze attendance statistics using the Analytics Interface.
User Management:

Manage users and their information through the Manage Users Interface.




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