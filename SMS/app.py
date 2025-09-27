from app import create_app,db 
from flask import session, redirect, url_for, request



app = create_app()

# @app.after_request
# def add_no_cache_headers(response):
#     response.headers["Cache-Control"] = " must-revalidate"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     return response

# @app.before_request
# def require_login():
#     # Paths that do NOT require login
#     exempt_paths = [
#         "/login",
#         "/signup",
#         "/static",
#         "/captcha/generate",
#         "/captcha/validate"
#     ]

#     # Only redirect if the current path is NOT exempt
#     if not any(request.path == p or request.path.startswith(p + "/") for p in exempt_paths):
#         # Check if user is logged in
#         if "user_id" not in session:
#             return redirect("/login")



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)                                                                       