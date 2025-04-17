from flask import Flask, request, jsonify, send_file
from models import db, Student, Course
import pandas as pd
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    courses = Course.query.filter(Course.id.in_(data.get("courses", []))).all()
    student = Student(name=data["name"], email=data["email"], age=data["age"], courses=courses)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added", "id": student.id})

@app.route("/students", methods=["GET"])
def list_students():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    sort_by = request.args.get("sort", "id")
    sort_order = request.args.get("order", "asc")

    query = Student.query.filter_by(deleted=False)

    if sort_order == "desc":
        query = query.order_by(db.desc(getattr(Student, sort_by)))
    else:
        query = query.order_by(getattr(Student, sort_by))

    students = query.paginate(page=page, per_page=limit).items

    result = [{
        "id": s.id,
        "name": s.name,
        "email": s.email,
        "age": s.age,
        "courses": [c.title for c in s.courses]
    } for s in students]

    return jsonify(result)

@app.route("/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    data = request.json
    course_ids = data.get("courses", [])

    student = Student.query.get_or_404(student_id)
    courses = Course.query.filter(Course.id.in_(course_ids)).all()
    student.courses.extend([c for c in courses if c not in student.courses])
    db.session.commit()

    return jsonify({"message": f"Student {student.name} enrolled in courses."})

@app.route("/students/<int:student_id>", methods=["DELETE"])
def soft_delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.deleted = True
    db.session.commit()
    return jsonify({"message": "Student marked as deleted."})

@app.route("/students/export", methods=["GET"])
def export_students():
    students = Student.query.filter_by(deleted=False).all()
    data = [{
        "ID": s.id,
        "Name": s.name,
        "Email": s.email,
        "Age": s.age,
        "Courses": ", ".join([c.title for c in s.courses])
    } for s in students]

    df = pd.DataFrame(data)
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(io.BytesIO(buf.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='students.csv')

@app.route("/courses", methods=["POST"])
def add_course():
    data = request.json
    course = Course(title=data["title"], credits=data["credits"])
    db.session.add(course)
    db.session.commit()
    return jsonify({"message": "Course added", "id": course.id})

if __name__ == "__main__":
    app.run(debug=True)
