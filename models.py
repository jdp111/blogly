from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """creates user info"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-Y5t0_YAP2Kak3u5WA-TFTzY1zOu3C5Bfjw&usqp=CAU')


















