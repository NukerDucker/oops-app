from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from modules.system import System
from modules.patient import Patient
from modules.treatment import Treatment
from modules.prescription import Prescription

patients_bp = Blueprint('patients', __name__)
system_service = System()

def init_patients_routes(blueprint, system):
    """Initialize patient routes with system dependency"""
    global system_service
    system_service = system
    return blueprint

@patients_bp.route('/api/patients', methods=['GET'])
@jwt_required()
def get_patients():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Simple authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Return all patients from system
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'age': p.age,
        'gender': p.gender,
        'contact': p.contact,
        'history': p.history,
        'medications_count': len(p.get_medications()),
        'current_medications_count': len(p.current_medications),
        'fees_total': p.calculate_total_fees()
    } for p in system_service._patients.values()]), 200

@patients_bp.route('/api/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Simple authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Find patient by ID using system
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Get the patient data
    patient_data = patient.get_report_data()
    
    # Convert Treatment objects to dictionaries before JSON serialization
    if 'treatments' in patient_data and patient_data['treatments']:
        patient_data['treatments'] = [
            treatment.to_dict() for treatment in patient_data['treatments']
        ]
    
    # Also handle current_medications if they exist
    if 'current_medications' in patient_data and patient_data['current_medications']:
        patient_data['current_medications'] = [
            med.to_dict() if hasattr(med, 'to_dict') else med 
            for med in patient_data['current_medications']
        ]
    
    return jsonify(patient_data), 200

@patients_bp.route('/api/patients/add', methods=['POST'])
@jwt_required()
def add_patient():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Simple authorization check
    if not user or user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    try:
        # Create new patient with the provided data
        new_patient = Patient(
            data.get('name'),
            int(data.get('age')),
            data.get('gender'),
            data.get('contact')
        )
        
        # Add to system using system controller
        success, message = system_service.add_patient(new_patient)
        
        if not success:
            return jsonify({'error': message}), 400
        
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
    user = system_service.get_user_from_username(current_username)
    
    # Simple authorization check
    if not user or user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    patient_id = int(data.get('id'))
    
    try:
        # Find the patient using system
        patient = system_service.get_patient_from_id(patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Create updated patient
        updated_patient = Patient(
            data.get('name', patient.name),
            int(data.get('age', patient.age)),
            data.get('gender', patient.gender),
            data.get('contact', patient.contact)
        )
        # Preserve the ID
        updated_patient.id = patient_id
        
        # Update internal lists/properties from the old patient
        updated_patient._history = patient._history.copy()
        updated_patient._prescriptions = patient._prescriptions.copy()
        updated_patient._medications = patient._medications.copy()
        updated_patient._fees = patient._fees.copy()
        updated_patient._treatments = patient._treatments.copy()
        
        # Update in system
        # We need to implement this method in the System class if it doesn't exist
        system_service._patients[patient_id] = updated_patient
        
        return jsonify({
            'message': 'Patient updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/delete/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Simple authorization check - only admin can delete patients
    if not user or user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the patient using system
        patient = system_service.get_patient_from_id(patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Remove from system
        del system_service._patients[patient_id]
        
        return jsonify({
            'message': 'Patient deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/<int:patient_id>/history/add', methods=['POST'])
@jwt_required()
def add_patient_history(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Simple authorization check
    if not user or user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    entry = data.get('entry')
    
    try:
        # Get patient from system
        patient = system_service.get_patient_from_id(patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        result, message = patient.add_history_entry(entry)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@patients_bp.route('/api/patients/<int:patient_id>/history/delete', methods=['DELETE'])
@jwt_required()
def delete_patient_history(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    index = data.get('index')
    
    if index is None:
        return jsonify({'error': 'Index of history entry not provided'}), 400
    
    try:
        # Get patient from system
        patient = system_service.get_patient_from_id(patient_id)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Check if index is valid
        if index < 0 or index >= len(patient.history):
            return jsonify({'error': 'Invalid history entry index'}), 400
        
        # Remove the history entry at specified index
        removed_entry = patient._history.pop(index)
        
        return jsonify({
            'message': 'History entry deleted successfully',
            'deleted_entry': removed_entry
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@patients_bp.route('/api/patients/<int:patient_id>/history', methods=['GET'])
@jwt_required()
def get_patient_history(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient from system
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify({'histories': patient.history}), 200

@patients_bp.route('/api/patients/<int:patient_id>/treatments', methods=['POST'])
@jwt_required()
def add_patient_treatment(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient from system
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    data = request.json
    
    try:
        # Create new treatment
        new_treatment = Treatment(
            symptoms=data.get('symptoms', ''),
            diagnosis=data.get('diagnosis', ''),
            treatment=data.get('treatment', ''),
            treatment_date=datetime.strptime(data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        )
        
        # Add treatment to patient
        result, message = patient.add_treatment(new_treatment)
        
        if not result:
            return jsonify({'error': message}), 400
        
        # Also add to patient history
        patient.add_treatment_to_history(new_treatment)
        
        return jsonify({
            'message': 'Treatment added successfully',
            'treatment_id': new_treatment.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/<int:patient_id>/prescriptions', methods=['POST'])
@jwt_required()
def add_patient_prescription(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient from system
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    data = request.json
    
    try:
        # Create new prescription (assuming Prescription class structure)
        new_prescription = Prescription(
            medication=data.get('medication', ''),
            dosage=data.get('dosage', ''),
            date=datetime.strptime(data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        )
        
        # Add prescription to patient
        result, message = patient.add_prescription(new_prescription)
        
        if not result:
            return jsonify({'error': message}), 400
        
        # Also add to patient history
        patient.add_prescription_to_history(new_prescription)
        
        # Verify prescription using system service
        system_service.verify_prescription(new_prescription)
        
        return jsonify({
            'message': 'Prescription added successfully',
            'prescription_id': new_prescription.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/<int:patient_id>/treatments', methods=['GET'])
@jwt_required()
def get_patient_treatments(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient from system
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    treatments = patient.get_treatments()
    
    return jsonify([t.to_dict() for t in treatments]), 200

@patients_bp.route('/api/patients/<int:patient_id>/prescriptions', methods=['GET'])
@jwt_required()
def get_patient_prescriptions(patient_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient from system
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    prescriptions = patient.get_prescriptions()
    
    return jsonify([p.to_dict() for p in prescriptions]), 200

# Add these new routes for treatment management

@patients_bp.route('/api/patients/<int:patient_id>/treatments/<int:treatment_id>', methods=['PUT'])
@jwt_required()
def update_patient_treatment(patient_id, treatment_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient and treatment
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    treatment = patient.get_treatment(treatment_id)
    if not treatment:
        return jsonify({'error': 'Treatment not found'}), 404
    
    data = request.json
    
    try:
        # Create updated treatment
        from datetime import datetime
        updated_treatment = Treatment(
            symptoms=data.get('symptoms', treatment.symptoms),
            diagnosis=data.get('diagnosis', treatment.diagnosis),
            treatment=data.get('treatment', treatment.treatment),
            treatment_date=datetime.strptime(data.get('date', treatment.date.isoformat()), 
                                            '%Y-%m-%d').date() if 'date' in data else treatment.date,
            finished=data.get('finished', treatment.finished)
        )
        # Preserve the ID
        updated_treatment.id = treatment_id
        
        # Update treatment
        result, message = patient.update_treatment(treatment_id, updated_treatment)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': 'Treatment updated successfully',
            'treatment': updated_treatment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@patients_bp.route('/api/patients/<int:patient_id>/treatments/<int:treatment_id>', methods=['DELETE'])
@jwt_required()
def delete_patient_treatment(patient_id, treatment_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    # Authorization check
    if not user or user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get patient
    patient = system_service.get_patient_from_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Delete treatment
    result, message = patient.remove_treatment(treatment_id)
    
    if not result:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'message': 'Treatment deleted successfully'
    }), 200