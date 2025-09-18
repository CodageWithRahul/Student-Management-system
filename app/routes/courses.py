from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from app import db
from app.models.sms_models import Course ,Subject,SemesterSubject,Semester

course_bp = Blueprint("course",__name__)

@course_bp.route("/courses")
def course_home():
    if session.get("user_id"):
        got_courses = Course.query.all()
        return render_template("courses/courses.html",courses =got_courses)
    else:
        return redirect(url_for("auth.login"))

@course_bp.route("/courses/add",methods = ["POST","GET"])
def add_course():
    if request.method == "POST":
        course_name = request.form.get("name")
        course_duration = request.form.get("duration")
        new_course = Course(name = course_name,duration = course_duration)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("course.course_home"))
    else:
        return render_template("courses/add_course.html")

@course_bp.route("/courses/search",methods = ["POST"])
def search_course():
    search_term = request.form.get("search")

    if not search_term:
        flash("Please enter a search term", "error")
        return redirect("/courses")
    if search_term.isdigit():
        got_course = Course.query.filter_by(id=int(search_term))
    else:
        got_course = Course.query.filter(Course.name.ilike(f"%{search_term}%")).all()

    if not got_course:
        flash("No Course found", "error")

    return render_template("courses/courses.html",courses = got_course)
        

@course_bp.route("/courses/add/subject",methods = ["POST","GET"])
def add_subject():
    if request.method == ("POST"):
        sub_code = request.form.get("sub_code")
        sub_name = request.form.get("sub_name")
        new_sub = Subject(code = sub_code,name = sub_name)
        db.session.add(new_sub)
        db.session.commit()
        flash("Subject is added","success")
        return redirect(url_for("course.add_subject"))
    else:
        return render_template("courses/add_subject.html")
    

@course_bp.route("/courses/<int:course_id>/semesters") 
def semester_manage(course_id):
    got_course = Course.query.get_or_404(course_id)
    return render_template("courses/semester_manage.html",course = got_course)


@course_bp.route("/courses/<int:course_id>/semesters/add/form",methods = ["POST","GET"])
def add_semester(course_id):
    if request.method ==  "POST":
        c_id = request.form.get("course_id")
        sem_num = request.form.get("number")
        selected_subjects = request.form.getlist("subjects")
        print(c_id)
        print(sem_num)
        print(selected_subjects)
        new_sem = Semester(number= sem_num,course_id = c_id)
        db.session.add(new_sem)
        db.session.flush()
        for sub in selected_subjects:
            new_sub = SemesterSubject(semester_id = new_sem.id,subject_id = sub)
            db.session.add(new_sub)
        
        db.session.commit()
        
        got_course = Course.query.filter_by(id = course_id).first()
        return render_template("courses/add_semester.html",course = got_course,subjects = Subject.query.all())
    else:
        got_course = Course.query.filter_by(id = course_id).first()
        return render_template("courses/add_semester.html",course = got_course,subjects = Subject.query.all())
