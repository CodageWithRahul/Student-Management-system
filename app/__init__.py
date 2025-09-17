"""App factory setup"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # if flask_sqlalchemy not found for any reason just install it using this command {{pip install flask-sqlalchemy}}


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SMS.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.students import student_bp
    from app.routes.courses import course_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    return app