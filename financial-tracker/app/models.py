from datetime import datetime
from . import db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import pytz

utc_zone = pytz.utc
local_tz = pytz.timezone('US/Central')  # Ensure it's imported here as well
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)  # Budget amount
    period = db.Column(db.String(10), nullable=False, default="monthly")  # monthly, weekly, biweekly
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(utc_zone))
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Budget ({self.period}): {self.amount}>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category: {self.name}>"

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(utc_zone).astimezone(local_tz))

    category = db.relationship('Category', backref='expenses')

    def __repr__(self):
        return f"<Expense ({self.category.name}): {self.amount}>"
