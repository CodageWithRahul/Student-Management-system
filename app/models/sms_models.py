from app import db
import datetime

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    duration = db.Column(db.String(20), nullable=False)

    # Relationship: one course has many semesters
    semesters = db.relationship("Semester", backref="course", lazy=True)


class Subject(db.Model):
    __tablename__ = "subjects"
    code = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Semester(db.Model):
    __tablename__ = "semesters"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)  # e.g., 1, 2, 3...
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)

    # Relationship: a semester has many subjects (via link table)
    subjects = db.relationship("Subject", secondary="semester_subjects", backref="semesters")


# Link table for Semester <-> Subject (many-to-many)
class SemesterSubject(db.Model):
    __tablename__ = "semester_subjects"
    id = db.Column(db.Integer, primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.code"), nullable=False)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    last_qualification = db.Column(db.String(30))

    enrollments = db.relationship("Enrollment", backref="student", lazy=True)


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    f_date = datetime.date.today()
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey("semesters.id"), nullable=False)
    enroll_date = db.Column(db.Date, default=f_date, nullable=False)
    status = db.Column(db.String(20), default="active", nullable=False)

    course = db.relationship("Course", backref="enrollments")
    semester = db.relationship("Semester", backref="enrollments") 



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(100),nullable =False)
    email = db.Column(db.String(80),nullable = False)
    username = db.Column(db.String(80),unique = True,nullable = False)
    password = db.Column(db.String(80),nullable = False)