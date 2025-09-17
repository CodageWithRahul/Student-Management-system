from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from app import db
from app.models.sms_models import User


auth_bp = Blueprint('auth',__name__)

@auth_bp.route("/signup",methods = ["POST","GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        new_user = User(name = name,email = email ,username = username,password = password)
        db.session.add(new_user)
        db.session.commit()
        flash("you are added successfully" ,"message")
        return redirect(url_for("auth.login"))
    else:
        return render_template("signup.html")

@auth_bp.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session["user"] = user.name
            print(user.id)
            print(user.name)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.home'))
        else:
            flash("invalid credentials", "error")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop('user')
    session.pop('user_id')
    return redirect(url_for("auth.login"))