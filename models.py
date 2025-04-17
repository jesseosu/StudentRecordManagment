from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

student_course = db.Table('student_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, default=False)  # Soft delete flag
    courses = db.relationship('Course', secondary=student_course, backref='students')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
