from flask import Blueprint,render_template,redirect,url_for,flash,session,request,jsonify
from app import db
from app.models.sms_models import Student,Course,Enrollment
from sqlalchemy import or_,cast,String
from app.decorator.login_auth import login_required

enrollment_bp = Blueprint('enrollment',__name__)

@enrollment_bp.route("/enrollments")
@login_required
def enroll_home():
    if session.get("user_id"):
        enrolls = Enrollment.query.order_by(Enrollment.enroll_date.desc()).limit(5).all()
        return render_template("enrollment/enroll_home.html",enrollments = enrolls,text = "Last 5 Enrollments!")
    else:
        return redirect(url_for("auth.login"))


@enrollment_bp.route("/enrollments/add",methods = ["POST","GET"])
@login_required
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



@enrollment_bp.route("/enrollments/<int:enroll_id>/edit",methods = ["POST","GET"])
@login_required
def edit_enroll(enroll_id):
    got_enroll = Enrollment.query.get_or_404(enroll_id)    
    if request.method == "POST":
        got_enroll.student_id = request.form.get("student_id")
        got_enroll.course_id = request.form.get("course_id")
        got_enroll.semester_id = request.form.get("semester_id")
        # got_enroll.enroll_date = request.form.get()
        got_enroll.status = request.form.get("status")
        
        try:
            db.session.commit()
            flash("student is updated succesfully","success")
            return redirect(url_for("enrollment.enroll_home"))
        except Exception as e:
            db.session.rollback()
            flash("error in updated ","error")
            return redirect(url_for("enrollment.enroll_home")) 
    else :
        got_courses = Course.query.all()
        return render_template("enrollment/edit_enroll.html",enroll = got_enroll,courses =got_courses)
    
    
    
@enrollment_bp.route("/enrollments/<int:enroll_id>/delete",methods = ["POST","GET"])
@login_required
def deroll_student(enroll_id):
    enrolled_studnet = Enrollment.query.get_or_404(enroll_id)
    
    db.session.delete(enrolled_studnet)
    db.session.commit()
    flash("Student has been de-enrolled successfully.", "success")
    return redirect(url_for("enrollment.enroll_home"))


@enrollment_bp.route("/enrollments/search",methods = ["POST"])
@login_required
def search_enroll():
    search_term= request.form.get("search").strip()
    if not search_term:
        flash("Please enter a search term", "error")
        return render_template("enrollment/enroll_home.html", enrollments=[])

    if search_term.isdigit():
        got_enroll = Enrollment.query.filter(Enrollment.id == int(search_term))
        
    else:
        got_enroll = (Enrollment.query
            .join(Course)
            .join(Student)
            .filter(
                or_(
                    Course.name.ilike(f"%{search_term}%"),
                    Student.name.ilike(f"%{search_term}%"),
                    cast(Enrollment.enroll_date, String).ilike(f"%{search_term}%")
                )
            )
        )

        
        
    results = got_enroll.all()
    if not results:
        flash("No Enrollment Found", "error")
    return render_template("enrollment/enroll_home.html",enrollments= results)
    

@enrollment_bp.route("/students/search")
@login_required
def search_students():
    query = request.args.get("query", "")
    results = Student.query.filter(Student.name.ilike(f"%{query}%")).limit(10).all()
    return jsonify([{"id": s.id, "name": s.name} for s in results])

@enrollment_bp.route("/enroll/students/<int:student_id>/viwe")
@login_required
def viwe_student(student_id):
    got_student = Student.query.get_or_404(student_id)
    return render_template("students/student_view.html", student=got_student,back_url = "enrollments",show_edit = False)
