from flask import Blueprint,render_template,redirect,url_for,flash,session,request,jsonify
from app import db
from app.models.sms_models import Student,Course,Enrollment

student_bp = Blueprint('student',__name__)

@student_bp.route("/students")
def students():
    if session.get("user_id"):
        got_course =  Course.query.all()
        return render_template("students/students.html",courses=got_course)
    else:
        return redirect(url_for("auth.login"))
    

@student_bp.route("/api/courses/<int:course_id>/semesters")
def api_get_semesters(course_id):
    course = Course.query.get_or_404(course_id)
    semesters = [{"id": sem.id, "number": sem.number} for sem in course.semesters]
    return jsonify({"semesters": semesters})

    
@student_bp.route("/students/add",methods= ["POST","GET"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        age = request.form.get("age")
        phone = request.form.get("phone")
        email = request.form.get("email")
        last_qualification = request.form.get("last_qualification")
        try:
            new_student = Student(name=name,address=address,age=age,phone=phone,email=email,last_qualification=last_qualification)
            db.session.add(new_student)
            db.session.commit()
            flash(f"Student {name} added successfully" ,"message")
            return redirect(url_for("student.students"))
        except Exception as e:
            flash(f"error same email found" ,"message")
            return redirect(url_for("student.add_student"))
            
    else:
        return render_template("students/add_student.html")
    
@student_bp.route("/students/filter",methods=["POST"])
def serachStudent():
    search_term = (request.form.get("search") or "").strip()
    search_course = (request.form.get("course") or "").strip()
    search_sem = (request.form.get("semester") or "").strip()
    
    if not search_term and not search_course and not search_sem:
        flash("Please enter a search term", "error")
        return redirect("/students")

    # Start query joining Student and Enrollment
    query = Student.query.outerjoin(Enrollment)

    # Apply search by term (id or name)
    if search_term:
        if search_term.isdigit():
            query = query.filter(Student.id == int(search_term))
        else:
            query = query.filter(Student.name.ilike(f"%{search_term}%"))
    print(query)

    # Apply course filter
    if search_course:
        query = query.filter(Enrollment.course_id == int(search_course))

    # Apply semester filter
    if search_sem :
        query = query.filter(Enrollment.semester_id == int(search_sem))

    got_students = query.all()

    if not got_students:
        flash("No students found", "error")
    got_course =  Course.query.all()
    return render_template("students/students.html", courses = got_course,students=got_students)



@student_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    got_student = Student.query.get_or_404(student_id)
    

    if request.method == "POST":
        # Update student details from form
        got_student.name = request.form.get("name")
        got_student.address = request.form.get("address")
        got_student.age = request.form.get("age")
        got_student.phone = request.form.get("phone")
        got_student.email = request.form.get("email")
        got_student.last_qualification = request.form.get("last_qualification")

        try:
            db.session.commit()
            flash("Student updated successfully!", "success")
            return redirect(url_for("student.students"))  # go back to student list
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating student", "error")

    # GET request → render form with current data
    return render_template("students/edit_student.html", student=got_student)


@student_bp.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    if student.enrollments:  # assuming you have relationship Student.enrollments
        course_names = [enrollment.course.name for enrollment in student.enrollments]
        flash(f"Cannot delete student. They are enrolled in: {', '.join(course_names)}", "error")
        return redirect(url_for("student.students"))

    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting student: {e}", "error")

    return redirect(url_for("student.students"))

@student_bp.route("/students/<int:student_id>/viwe")
def viwe_student(student_id):
    got_student = Student.query.get_or_404(student_id)
    return render_template("students/student_viwe.html", student=got_student,back_url = "students",show_edit = True)


    