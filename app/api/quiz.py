from flask import Blueprint, jsonify

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

@quiz_bp.route('/submit', methods=['POST'])
def submit():
    return jsonify({'status': 'Awaiting active recall metrics tracking hooks.'})