from flask import Blueprint,session
from app.models.sms_models import User

base_bp = Blueprint("user",__name__)

@base_bp.app_context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        return {"login_user": User.query.get(user_id)}
    return {"login_user": None}