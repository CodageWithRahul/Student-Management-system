from flask import Blueprint,render_template,redirect,url_for,flash,session,request,jsonify
from app import db
from app.models.sms_models import Student,Course,Enrollment

enrollment_bp = Blueprint('enrollment',__name__)

@enrollment_bp.route("/enrollments")
def enroll_home():
    if session.get("user_id"):
        enrolls = Enrollment.query.all()
        return render_template("enrollment/enroll_home.html",enrollments = enrolls)
    else:
        return redirect(url_for("auth.login"))

@enrollment_bp.route("/enrollments/add",methods = ["POST","GET"])
def add_enroll():
    if request.method == "POST":
        got_student_id =  request.form.get("student_id")
        got_course_id =  request.form.get("course_id")
        got_semester =  request.form.get("semester_id")
        # got_date =  request.form.get("enroll_date")
        got_status = request.form.get("status")
        new_enrollment = Enrollment(student_id =got_student_id,course_id=got_course_id,semester_id = got_semester,status=got_status)
        db.session.add(new_enrollment)
        db.session.commit()
        return redirect(url_for("enrollment.enroll_home"))
    else:
        got_courses = Course.query.all()
        return render_template("enrollment/add_enrollment.html",courses = got_courses)


@enrollment_bp.route("/students/search")
def search_students():
    query = request.args.get("query", "")
    results = Student.query.filter(Student.name.ilike(f"%{query}%")).limit(10).all()
    return jsonify([{"id": s.id, "name": s.name} for s in results])
