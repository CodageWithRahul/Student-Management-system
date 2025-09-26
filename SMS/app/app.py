from app import create_app,db 
from flask import session, redirect, url_for, request



app = create_app()

# @app.after_request
# def add_no_cache_headers(response):
#     response.headers["Cache-Control"] = " must-revalidate"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     return response


@app.before_request
def require_login():
    # Allow access to login & static files
    if request.endpoint in ["auth.login", "auth.signup", "static"]:
        return  

    if "user_id" not in session:
        return redirect(url_for("auth.login"))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)