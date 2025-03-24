from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from modules.system import System
from modules.appointment import Appointment

appointments_bp = Blueprint('appointments', __name__)

# Add this initialization function
def init_appointments_routes(blueprint, system):
    """Initialize appointment routes with system dependency"""
    global system_service
    system_service = system
    return blueprint

# Set a default system for direct imports
system_service = System()

@appointments_bp.route('/api/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if user.user_type not in ["admin", "doctor", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if user.user_type == "admin" or user.user_type == "receptionist":
        appointments = list(system_service._appointments.values())
    else:  
        appointments = system_service.get_appointments(user)
    
    return jsonify([{
        'id': a.id,
        'patient_id': a.patient_id,
        'patient_name': system_service.get_patient_from_id(a.patient_id).name if system_service.get_patient_from_id(a.patient_id) else "Unknown",
        'doctor_id': a.doctor_id,
        'doctor_name': system_service.get_user(a.doctor_id).username if system_service.get_user(a.doctor_id) else "Unknown",
        'date': a.date.isoformat(),
        'time': a.time.isoformat(),
        'status': a.status
    } for a in appointments]), 200

# Add these routes to properly support the frontend
@appointments_bp.route('/api/appointments/add', methods=['POST'])
@jwt_required()
def add_appointment():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Get patient and doctor IDs
        patient_id = int(data.get('patient_id'))
        doctor_id = int(data.get('doctor_id'))
        
        # Convert date and time strings to objects
        appointment_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        appointment_time = datetime.strptime(data.get('time'), '%H:%M').time()
        
        # Create appointment
        new_appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=appointment_date,
            time=appointment_time
        )
        
        # Add to system
        result, message = system_service.add_appointment(new_appointment)
        
        if not result:
            return jsonify({'error': message}), 400
            
        return jsonify({'id': new_appointment.id, 'message': 'Appointment added successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/api/appointments/update', methods=['PUT'])
@jwt_required()
def update_appointment():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        appointment_id = int(data.get('id'))
        appointment = system_service._appointments.get(appointment_id)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update fields
        if 'patient_id' in data:
            appointment.update_patient_id(int(data.get('patient_id')))
            
        if 'doctor_id' in data:
            appointment.update_doctor_id(int(data.get('doctor_id')))
            
        if 'date' in data:
            appointment.update_date(datetime.strptime(data.get('date'), '%Y-%m-%d').date())
            
        if 'time' in data:
            appointment.update_time(datetime.strptime(data.get('time'), '%H:%M').time())
            
        if 'status' in data:
            appointment.update_status(data.get('status'))
            
        return jsonify({'message': 'Appointment updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/api/appointments/status/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        appointment = system_service._appointments.get(appointment_id)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
            
        result, message = appointment.update_status(data.get('status'))
        
        if not result:
            return jsonify({'error': message}), 400
            
        return jsonify({'message': 'Appointment status updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/api/appointments/delete/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        result, message = system_service.delete_appointment(appointment_id)
        
        if not result:
            return jsonify({'error': message}), 400
            
        return jsonify({'message': 'Appointment deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
