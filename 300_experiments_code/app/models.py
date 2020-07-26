from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    submissions = db.relationship('Submission', backref = 'author', lazy = 'dynamic')
    student_id = db.Column(db.String(64), index = True, unique = True)

    def __repr__(self) :
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Float())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    regulation = db.Column(db.String(120))
    balance_sheet = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Submission {}'.format(self.answerfor)
