from flask import Blueprint, render_template, session, redirect

# This variable definition MUST match exactly what __init__.py is trying to import
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    # Force access restriction if the security session is missing
    if 'user_id' not in session:
        return redirect('/auth')
    return render_template('interface.html')

@views_bp.route('/auth')
def auth_portal():
    # If already logged in, skip the gate and head straight to dashboard
    if 'user_id' in session:
        return redirect('/')
    return render_template('auth_portal.html')