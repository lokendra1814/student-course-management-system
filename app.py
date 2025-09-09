from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import csv

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect("scms.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- ROUTES ----------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        with get_db_connection() as conn:
            existing = conn.execute("SELECT * FROM Students WHERE email = ?", (email,)).fetchone()
            if existing:
                flash("⚠️ Email already exists!", "danger")
                return redirect(url_for('add_student'))
            conn.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
        flash("✅ Student added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_student.html')



# View All Students
@app.route('/view_students')
def view_students():
    with get_db_connection() as conn:
        students = conn.execute("SELECT * FROM Students").fetchall()
    return render_template('view_students.html', students=students)


# Add Course
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        duration = request.form['duration']
        with get_db_connection() as conn:
            conn.execute("INSERT INTO Courses (course_name, duration) VALUES (?, ?)", (course_name, duration))
            conn.commit()
        flash("📘 Course added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_course.html')


# View All Courses
@app.route('/view_courses')
def view_courses():
    with get_db_connection() as conn:
        courses = conn.execute("SELECT * FROM Courses").fetchall()
    return render_template('view_courses.html', courses=courses)


# Enroll Student
@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    with get_db_connection() as conn:
        students = conn.execute("SELECT * FROM Students").fetchall()
        courses = conn.execute("SELECT * FROM Courses").fetchall()
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        with get_db_connection() as conn:
            conn.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
            conn.commit()
        flash("🎯 Student enrolled successfully!", "success")
        return redirect(url_for('home'))
    return render_template('enroll_student.html', students=students, courses=courses)


# Students in a Course
@app.route('/students_in_course/<int:course_id>')
def students_in_course(course_id):
    with get_db_connection() as conn:
        course = conn.execute("SELECT * FROM Courses WHERE course_id = ?", (course_id,)).fetchone()
        students = conn.execute(
            "SELECT s.* FROM Students s "
            "JOIN Enrollments e ON s.student_id = e.student_id "
            "WHERE e.course_id = ?", (course_id,)
        ).fetchall()
    return render_template('students_in_course.html', students=students, course=course)


# Select Course Page (for homepage link)
@app.route('/select_course', methods=['GET', 'POST'])
def select_course():
    with get_db_connection() as conn:
        courses = conn.execute("SELECT * FROM Courses").fetchall()
    if request.method == 'POST':
        course_id = request.form['course_id']
        return redirect(url_for('students_in_course', course_id=course_id))
    return render_template('select_course.html', courses=courses)


# Course Enrollments Report
@app.route('/course_enrollments')
def course_enrollments():
    with get_db_connection() as conn:
        courses = conn.execute(
            "SELECT c.course_id, c.course_name, COUNT(e.student_id) as total_students "
            "FROM Courses c LEFT JOIN Enrollments e ON c.course_id = e.course_id "
            "GROUP BY c.course_id"
        ).fetchall()
    return render_template('course_enrollments.html', courses=courses)


# Students in Multiple Courses
@app.route('/students_multiple_courses')
def students_multiple_courses():
    with get_db_connection() as conn:
        students = conn.execute(
            "SELECT s.name, s.email, COUNT(e.course_id) as num_courses "
            "FROM Students s JOIN Enrollments e ON s.student_id = e.student_id "
            "GROUP BY s.student_id HAVING num_courses > 1"
        ).fetchall()
    return render_template('students_multiple_courses.html', students=students)


# Search Student
@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        with get_db_connection() as conn:
            results = conn.execute(
                "SELECT * FROM Students WHERE name LIKE ? OR email LIKE ?",
                (f'%{keyword}%', f'%{keyword}%')
            ).fetchall()
    return render_template('search_student.html', results=results)


# Export Report (CSV)
@app.route('/export_report')
def export_report():
    with get_db_connection() as conn:
        data = conn.execute(
            "SELECT c.course_name, s.name as student_name, s.email "
            "FROM Courses c "
            "LEFT JOIN Enrollments e ON c.course_id = e.course_id "
            "LEFT JOIN Students s ON e.student_id = s.student_id"
        ).fetchall()

    filename = "student_course_report.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Course Name", "Student Name", "Student Email"])
        for row in data:
            writer.writerow([row["course_name"], row["student_name"], row["email"]])
    return send_file(filename, as_attachment=True)


# ---------- MAIN ----------
if __name__ == '__main__':
    if _name_ == "_main_":
    app.run(debug=False, host="0.0.0.0", port=5000)
