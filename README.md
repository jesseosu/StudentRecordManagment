# Student Records Management System

This project is a Flask-based Student Records Management System (SRMS) that includes features such as:

- Adding, listing, and deleting students and courses
- Enrolling students in courses
- Pagination and sorting for student listings
- Soft delete for student records
- CSV export of student data

## Setup

1. Clone the repository: 
git clone https://github.com/jesseosu/StudentRecordManagment.git

markdown
Copy

2. Install dependencies:
pip install -r requirements.txt

markdown
Copy

3. Run the app:
python app.py

markdown
Copy

## Endpoints

- `POST /students`: Add a student
- `GET /students`: List students (with pagination)
- `POST /students/<id>/enroll`: Enroll a student in courses
- `DELETE /students/<id>`: Soft delete a student
- `GET /students/export`: Export students to CSV
- `POST /courses`: Add a course
