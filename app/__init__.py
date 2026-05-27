import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.models import db

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Global System Constraints Configuration Configuration Array
    app.config['SECRET_KEY'] = '0ef8347fcd61c045b67a14e912bc0c5719bcbc01a4e58b1c'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netlogic_local.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = False  
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

    db.init_app(app)
    csrf.init_app(app)

    # Isolated scope imports to prevent sequence crashes on startup
    with app.app_context():
        from app.api.auth import auth_bp
        from app.api.network import network_bp
        from app.api.quiz import quiz_bp
        from app.api.views import views_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(network_bp)
        app.register_blueprint(quiz_bp)
        app.register_blueprint(views_bp)

    return app