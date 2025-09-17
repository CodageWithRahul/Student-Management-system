from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from app import db
from app.models.sms_models import Student

student_bp = Blueprint('student',__name__)

@student_bp.route("/students")
def students():
    return render_template("students/students.html")
    
@student_bp.route("/students/add",methods= ["POST","GET"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        age = request.form.get("age")
        phone = request.form.get("phone")
        email = request.form.get("email")
        last_qualification = request.form.get("last_qualification")
        new_student = Student(name=name,address=address,age=age,phone=phone,email=email,last_qualification=last_qualification)
        db.session.add(new_student)
        db.session.commit()
        flash(f"Student {name} added successfully" ,"message")
        return redirect(url_for("student.students"))
    else:
        return render_template("students/add_student.html")
    
@student_bp.route("/students/filter",methods=["POST"])
def serachStudent():
    search_term = request.form.get("search")

    if not search_term:
        flash("Please enter a search term", "error")
        return redirect("/students")

    if search_term.isdigit():
        got_student = Student.query.filter_by(id = int(search_term)).all()

    else:
        # Search by name (partial match, case-insensitive)
        got_student = Student.query.filter(Student.name.ilike(f"%{search_term}%")).all()

    if not got_student:
        flash("No students found", "error")
        
    return render_template("students/students.html", students=got_student)