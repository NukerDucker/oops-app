from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from modules.system import System
from modules.medication import Medication

medications_bp = Blueprint('medications', __name__)
system_service = System()

def init_medications_routes(blueprint, system):
    """Initialize medication routes with system dependency"""
    global system_service
    system_service = system
    return blueprint

@medications_bp.route('/api/medications', methods=['GET'])
@jwt_required()
def get_medications():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    
    all_medications = []
    for patient in system_service._patients.values():
        medications = patient.get_medications()
        for med in medications:
            patient_name = patient.name if patient else "Unknown"
            all_medications.append({
                'id': med.id,
                'patient_id': med.patient_id,
                'patient_name': patient_name,
                'name': med.name,
                'quantity': med.quantity,
                'start_date': med.start_date.isoformat() if hasattr(med, 'start_date') and med.start_date else None,
                'end_date': med.end_date.isoformat() if hasattr(med, 'end_date') and med.end_date else None,
                'notes': med.notes,
                'active': med.active,
                'finished': med.finished if hasattr(med, 'finished') else False
            })
    
    return jsonify(all_medications), 200

@medications_bp.route('/api/patients/<int:patient_id>/medications', methods=['POST'])
@jwt_required()
def add_medication(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    data = request.json
    
    try:
        
        new_medication = Medication(
            patient_id=patient_id,
            name=data.get('name'),
            quantity=data.get('quantity'),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date(),
            notes=data.get('notes', '')
        )
        
        
        success, message = patient.add_medication(new_medication)
        
        if not success:
            return jsonify({'error': message}), 400
            
        
        return jsonify({
            'message': 'Medication added successfully',
            'id': new_medication.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medications_bp.route('/api/patients/<int:patient_id>/medications/<int:medication_id>', methods=['PUT'])
@jwt_required()
def update_medication(patient_id, medication_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    
    medication = patient.get_medication(medication_id)
    if not medication:
        return jsonify({'error': 'Medication not found'}), 404
    
    data = request.json
    
    try:
        
        updated_medication = Medication(
            patient_id=patient_id,
            name=data.get('name', medication.name),
            quantity=data.get('quantity', medication.quantity),
            start_date=datetime.strptime(data.get('start_date', medication.start_date.isoformat()), '%Y-%m-%d').date(),
            end_date=datetime.strptime(data.get('end_date', medication.end_date.isoformat()), '%Y-%m-%d').date(),
            notes=data.get('notes', medication.notes)
        )
        updated_medication.id = medication_id
        
        if data.get('active') is False:
            updated_medication.stop_medication()
        
        
        success, message = patient.update_medication(medication_id, updated_medication)
        
        if not success:
            return jsonify({'error': message}), 400
            
        return jsonify({
            'message': 'Medication updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@medications_bp.route('/api/patients/<int:patient_id>/medications/<int:medication_id>', methods=['DELETE'])
@jwt_required()
def delete_medication(patient_id, medication_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    
    success, message = patient.remove_medication(medication_id)
    
    if not success:
        return jsonify({'error': message}), 400
        
    return jsonify({
        'message': 'Medication deleted successfully'
    }), 200

@medications_bp.route('/api/patients/<int:patient_id>/medications/<int:medication_id>/stop', methods=['PUT'])
@jwt_required()
def stop_medication(patient_id, medication_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    
    medication = patient.get_medication(medication_id)
    if not medication:
        return jsonify({'error': 'Medication not found'}), 404
    
    
    success, message = medication.stop_medication()
    
    if not success:
        return jsonify({'error': message}), 400
        
    return jsonify({
        'message': 'Medication stopped successfully'
    }), 200
