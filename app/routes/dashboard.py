from flask import Blueprint,render_template,redirect,url_for,flash,session
from app import db

dashboard_bp = Blueprint('dashboard',__name__)

@dashboard_bp.route("/")
def home():
    return render_template("dashboard.html")

@dashboard_bp.route("/students")
def students():
    pass