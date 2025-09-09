# 🎓 Student Course Management System
A simple *web-based Student Course Management System* built with *Python (Flask), SQLite, HTML, and CSS*.
This project allows easy management of students, courses, and enrollments with a clean UI.

##  Features
 *Student Management*

  * Add new students with name and email
  * View all registered students

   *Course Management*

  * Add new courses with course name & duration
  * View all available courses

   *Enrollments*

  * Enroll students into courses
  * View students in a selected course
  * See how many students are enrolled in each course
  * Find students enrolled in multiple courses

   *Extra Features (Bonus)*

  * Search student by name or email
  * Export reports to CSV
  * Navigation with Home button across all pages

## Database Design

Three main tables:

1. *Students* → (student_id, name, email)
2. *Courses* → (course_id, course_name, duration)
3. *Enrollments* → (enrollment_id, student_id, course_id)

## Tech Stack

* *Backend:* Python (Flask)
* *Frontend:* HTML, CSS (custom styling)
* *Database:* SQLite

## How to Run

1. Clone the repository

   bash
   git clone https://github.com/your-username/student-course-management-system.git
   cd student-course-management-system
   

2. Install dependencies

   bash
   pip install flask
   

3. Setup the database

   bash
   sqlite3 scms.db < schema.sql
   

4. Run the app

   bash
   python app.py


## Project Purpose

This project is made as a *beginner-friendly assignment* to learn:

* Database design (SQL + relationships)
* Flask routing & templates
* Building a mini web application
