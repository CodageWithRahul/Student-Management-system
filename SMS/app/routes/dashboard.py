from flask import Blueprint,render_template,redirect,url_for,flash,session
from app import db
from app.models.sms_models import Student,Course,Subject,Enrollment,User
from app.decorator.login_auth import login_required


dashboard_bp = Blueprint('dashboard',__name__)
@dashboard_bp.route("/")
@login_required
def home():
    user = User.query.get_or_404(session.get("user_id"))
    totalStudents =  Student.query.count()
    totalCourses =  Course.query.count()
    totalSubjects =  Subject.query.count()
    totalEnrollments =  Enrollment.query.count()
    return render_template("dashboard.html",total_students = totalStudents,total_courses = totalCourses,total_subjects = totalSubjects,total_enrollments = totalEnrollments,login_user = user)

    


