from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university_events.db'
app.config['SECRET_KEY'] = 'gizli-kalit-soz'
db = SQLAlchemy(app)

# --- VERİLƏNLƏR BAZASI MODELLƏRİ ---


class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  events = db.relationship('Event', backref='category', lazy=True)


class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(150), nullable=False)
  description = db.Column(db.Text, nullable=False)
  date = db.Column(db.String(50), nullable=False)
  time = db.Column(db.String(50), nullable=False)
  location = db.Column(db.String(150), nullable=False)
  max_participants = db.Column(db.Integer, nullable=False)
  category_id = db.Column(
      db.Integer, db.ForeignKey('category.id'), nullable=False
  )
  registrations = db.relationship(
      'Registration', backref='event', cascade='all, delete-orphan', lazy=True
  )


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(150), nullable=False)
  email = db.Column(db.String(150), unique=True, nullable=False)
  registrations = db.relationship('Registration', backref='user', lazy=True)


class Registration(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
  __table_args__ = (
      db.UniqueConstraint('user_id', 'event_id', name='unique_user_event'),
  )


# --- ROUTLAR ---


@app.route('/')
def index():
  return render_template('index.html')


# Verilənlər bazasını yaratmaq üçün
with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run(debug=True)