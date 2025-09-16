from app import create_app,db 


app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main_":
    app.run(debug=True)