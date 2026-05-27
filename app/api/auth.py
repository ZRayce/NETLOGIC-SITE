import re
from flask import Blueprint, request, jsonify, session
from app.models import db, User, AccountRole

# This exact line MUST exist at the top level for the import factory to build!
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not USERNAME_REGEX.match(username) or not EMAIL_REGEX.match(email) or len(password) < 8:
        return jsonify({'error': 'Malformed parameters.'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Identity conflict.'}), 409

    new_user = User(username=username, email=email, account_role=AccountRole.Student)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': 'User node committed.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Access denied.'}), 401

    session['user_id'] = user.user_id
    session['username'] = user.username
    session['role'] = user.account_role.value
    
    return jsonify({'success': 'Identity verified.'}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': 'Session terminated.'}), 200