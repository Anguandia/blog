from app import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(164))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140), index = True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship('Post', backref=db.backref('question', remote_side=[id]), lazy='dynamic')
    ans_to = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '{}'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))