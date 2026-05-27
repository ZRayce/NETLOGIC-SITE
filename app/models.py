import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AccountRole(enum.Enum):
    Admin = 'Admin'
    Student = 'Student'
    Professional = 'Professional'

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    account_role = db.Column(db.Enum(AccountRole), default=AccountRole.Student, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Retention Engine Metrics
    streak_days = db.Column(db.Integer, default=0, nullable=False)
    last_active_date = db.Column(db.Date, nullable=True)
    total_xp = db.Column(db.Integer, default=0, nullable=False)
    
    calculations = db.relationship('SavedCalculation', backref='user', lazy=True, cascade="all, delete-orphan")
    quiz_scores = db.relationship('QuizScore', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class SavedCalculation(db.Model):
    __tablename__ = 'saved_calculations'
    
    calc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    base_ip = db.Column(db.String(45), nullable=False)
    cidr_prefix = db.Column(db.Integer, nullable=False)
    ip_version = db.Column(db.Integer, nullable=False) # 4 or 6
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    subnet_results = db.relationship('SubnetResult', backref='calculation', lazy=True, cascade="all, delete-orphan")

class SubnetResult(db.Model):
    __tablename__ = 'subnet_results'
    
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    calc_id = db.Column(db.Integer, db.ForeignKey('saved_calculations.calc_id', ondelete='CASCADE'), nullable=False)
    subnet_name = db.Column(db.String(128), nullable=False)
    allocated_ip = db.Column(db.String(45), nullable=False)
    cidr_prefix = db.Column(db.Integer, nullable=False)
    usable_range = db.Column(db.String(96), nullable=False)
    broadcast_address = db.Column(db.String(45), nullable=False)

class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'
    
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    module_step = db.Column(db.Integer, nullable=False) # Tracks which Duolingo step (1, 2, 3...)
    score_achieved = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    date_attempted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)