from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date

patients_bp = Blueprint('patients', __name__)

# These will be imported from app.py
patients = []
users = []

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

@patients_bp.route('/api/patients', methods=['GET'])
@jwt_required()
def get_patients():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Return all patients
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'age': p.age,
        'gender': p.gender,
        'contact': p.contact,
        'history': p.history,
        'lab_results_count': len(p.get_lab_results()),
        'medications_count': len(p.get_medications()),
        'current_medications_count': len(p.current_medications),
        'fees_total': p.calculate_total_fees()
    } for p in patients]), 200

@patients_bp.route('/api/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Find patient by ID
    patient = next((p for p in patients if p.id == patient_id), None)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(patient.get_report_data()), 200

@patients_bp.route('/api/patients/add', methods=['POST'])
@jwt_required()
def add_patient():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    try:
        # Create new patient with the provided data
        from modules.patient import Patient
        new_patient = Patient(
            data.get('name'),
            int(data.get('age')),
            data.get('gender'),
            data.get('contact')
        )
        
        # Add to our patients list
        patients.append(new_patient)
        
        return jsonify({
            'message': 'Patient added successfully',
            'id': new_patient.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/update', methods=['PUT'])
@jwt_required()
def update_patient():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    patient_id = data.get('id')
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Update only allowed fields based on role
        if user.user_type in ["admin", "receptionist"]:
            # Admin and receptionist can update all patient info
            patient._name = data.get('name')
            patient._age = int(data.get('age'))
            patient._gender = data.get('gender')
            patient._contact = data.get('contact')
        elif user.user_type == "doctor":
            # Doctors can only update medical information, not personal info
            pass
        
        return jsonify({
            'message': 'Patient updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/delete/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check - only admin can delete patients
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the patient
        patient_index = next((i for i, p in enumerate(patients) if p.id == patient_id), None)
        
        if patient_index is None:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Remove the patient
        patients.pop(patient_index)
        
        return jsonify({
            'message': 'Patient deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/<int:patient_id>/history', methods=['POST'])
@jwt_required()
def add_patient_history(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    entry = data.get('entry')
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Add history entry
        result, message = patient.add_history_entry(entry)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400