from flask import Blueprint,render_template,redirect,url_for,flash,session,request
from app import db
from app.models.sms_models import Course ,Subject,SemesterSubject,Semester

course_bp = Blueprint("course",__name__)

@course_bp.route("/courses")
def course_home():
    if session.get("user_id"):
        return render_template("courses/courses.html")
    else:
        return redirect(url_for("auth.login"))

@course_bp.route("/courses/add",methods = ["POST","GET"])
def add_course():
    if request.method == "POST":
        course_name = request.form.get("name")
        course_duration = request.form.get("duration")
        new_course = Course(name = course_name,duration = course_duration)
        try:
            db.session.add(new_course)
            db.session.commit()
            flash(f"{course_name} added Successfully","success")
            return redirect(url_for("course.course_home"))
        
        except Exception :
            flash("Course is already added","success")
            return redirect(url_for("course.add_course"))
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

@course_bp.route("/courses/subject")
def subject_manage():
    return render_template("courses/subjects_manage.html")

@course_bp.route("/courses/search/subject",methods = ["POST"])
def search_subject():
    search_term = request.form.get("search")
    got_subject = Subject.query.filter(Subject.code.ilike(f"%{search_term}%" ) | Subject.name.ilike(f"%{search_term}%")).all()
    return render_template("courses/subjects_manage.html",subjects = got_subject)

@course_bp.route("/subject/edit/<string:subject_code>",methods = ["POST","GET"])
def edit_subject(subject_code):
    got_sub = Subject.query.get(subject_code)
    if request.method ==  "POST":
        got_sub.name = request.form.get("sub_name")
        got_sub.code = request.form.get("sub_code")
        try:
            db.session.commit()
            flash("Subject updated Successfully","success")
            return redirect(url_for("course.subject_manage"))
        except Exception:
            db.session.rollback()
            flash("Subject code is already exists","error")
            return redirect(url_for("course.edit_subject",subject_code = got_sub.code))
    else:
        return render_template("courses/edit_subject.html",subject = got_sub)
    
        

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

@course_bp.route("/courses/edit/<int:course_id>",methods = ["POST","GET"])
def edit_course(course_id):
    fetched_course = Course.query.get_or_404(course_id)
    if request.method == "POST":
        try:
            fetched_course.name = request.form.get("name")
            fetched_course.duration = request.form.get("duration")
            db.session.commit()
            flash("Update Successfully","error")
            return redirect(url_for("course.course_home"))
        except Exception:
            flash("error in updating course","error")
            return redirect(url_for("course.course_home"))
    else:
        return render_template("courses/edit_course.html",course = fetched_course)
    
@course_bp.route("/subject/delete/<string:subject_code>",methods = ["POST","GET"])
def delete_sub(subject_code):
    sub_for_delete = Subject.query.get(subject_code)
    try:
        db.session.delete(sub_for_delete)
        flash(f"{sub_for_delete.name} is deleted Successfully","success")
        db.session.commit()
        return redirect(url_for("course.course_home"))
    except Exception:
        flash("This subject is linked with Semester","error")
        return redirect(url_for("course.course_home"))
        
    
    
@course_bp.route("/courses/delete/<int:course_id>", methods=["POST","GET"])
def delete_course(course_id):
    course_delete = Course.query.get_or_404(course_id)
    
    if course_delete.semesters:
        semseter = [semester.number for semester in course_delete.semesters]
        flash(f"Cannot delete {course_delete.name} Course. This Course have : Active Semester {semseter}", "error")
        return redirect(url_for("course.course_home"))
    
    try:
        db.session.delete(course_delete)
        db.session.commit()
        flash("Course Deleted Successfully","success")
        return redirect(url_for("course.course_home"))
    except Exception :
        db.session.rollback()
        flash("Error in deleting course","error")
        
    return redirect(url_for("course.course_home"))


@course_bp.route("/courses/edit/semester/<int:semester_id>", methods=["POST", "GET"])
def edit_sem(semester_id):
    got_sem = Semester.query.get_or_404(semester_id)

    if request.method == "POST":
        got_sem.number = request.form.get("number")

        # Get selected subject codes Subject.code is PK
        new_selected_sub = request.form.getlist("subjects")

        # Update subjects for this semester
        got_sem.subjects = Subject.query.filter(Subject.code.in_(new_selected_sub)).all()

        db.session.commit()
        return redirect(url_for("course.semester_manage", course_id=got_sem.course.id))

    return render_template(
        "courses/edit_semester.html",
        course=got_sem.course,
        semester=got_sem,
        subjects=Subject.query.all()  # send ALL subjects
    )
@course_bp.route("/courses/delete/semester/<int:semester_id>",methods = {"POST","GET"})
def delete_sem(semester_id):
    sem_for_delete = Semester.query.get_or_404(semester_id)
    save_course_id = sem_for_delete.course.id
    if sem_for_delete.enrollments:
        sem = [enrollment.student for enrollment in sem_for_delete.enrollments]
        flash(f"Cannot delete this semester. {len(sem)} student(s) enrolled.", "error")
        return redirect(url_for("course.semester_manage",course_id =save_course_id))
    try:
        db.session.delete(sem_for_delete)
        db.session.commit()
        return redirect(url_for("course.semester_manage",course_id =save_course_id))
    except Exception:
        db.session.rollback()
        flash("not delete","error")
        return redirect(url_for("course.semester_manage",course_id =save_course_id))