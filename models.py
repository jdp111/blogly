from enum import unique
from flask_sqlalchemy import SQLAlchemy
import time
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
    image_url = db.Column(db.Text, default = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-Y5t0_YAP2Kak3u5WA-TFTzY1zOu3C5Bfjw&usqp=CAU')
    
    post = db.relationship('Post', backref="user", cascade = "all,delete-orphan")

class PostTag(db.Model):
    """relates posts and their tags"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'),primary_key=True, unique = True)


class Tag(db.Model):
    """list of tags that can be applied to posts"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable = False)

    


class Post(db.Model):
    """list of posts as related to user"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tag = db.relationship("Tag",secondary='posts_tags',backref='post')


















