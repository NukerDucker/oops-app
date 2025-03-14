from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

medications_bp = Blueprint('medications', __name__)

# These will be imported from app.py
patients = []
users = []

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

@medications_bp.route('/api/medications', methods=['GET'])
@jwt_required()
def get_medications():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Collect all medications from all patients
    all_medications = []
    for patient in patients:
        medications = patient.get_medications()
        for med in medications:
            all_medications.append({
                'id': med.id,
                'patient_id': med.patient_id,
                'patient_name': next((p.name for p in patients if p.id == med.patient_id), "Unknown"),
                'name': med.name,
                'dosage': med.dosage,
                'start_date': med.start_date.isoformat(),
                'end_date': med.end_date.isoformat(),
                'notes': med.notes,
                'active': med.active,
                'finished': med.finished
            })
    
    return jsonify(all_medications), 200