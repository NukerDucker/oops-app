from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

# These will be imported from app.py
appointments = []
patients = []
users = []

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

@appointments_bp.route('/api/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # For doctors, only return their appointments
    filtered_appointments = appointments
    if user.user_type == "doctor":
        filtered_appointments = [a for a in appointments if a.doctor_id == user.id]
    
    # Return appointments
    return jsonify([{
        'id': a.id,
        'patient_id': a.patient_id,
        'patient_name': next((p.name for p in patients if p.id == a.patient_id), "Unknown"),
        'doctor_id': a.doctor_id,
        'doctor_name': next((u.username for u in users if u.id == a.doctor_id), "Unknown"),
        'date': a.date.isoformat(),
        'time': a.time.isoformat(),
        'status': a.status
    } for a in filtered_appointments]), 200

@appointments_bp.route('/api/appointments/add', methods=['POST'])
@jwt_required()
def add_appointment():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Create new appointment
        from modules.appointment import Appointment
        new_appointment = Appointment(
            int(data.get('patient_id')),
            int(data.get('doctor_id')),
            datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            datetime.strptime(data.get('time'), '%H:%M').time()
        )
        
        # Add to appointments list
        appointments.append(new_appointment)
        
        return jsonify({
            'message': 'Appointment added successfully',
            'id': new_appointment.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/api/appointments/update', methods=['PUT'])
@jwt_required()
def update_appointment():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    appointment_id = data.get('id')
    
    try:
        # Find the appointment
        appointment = next((a for a in appointments if a.id == appointment_id), None)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update appointment fields
        appointment.patient_id = int(data.get('patient_id'))
        appointment.doctor_id = int(data.get('doctor_id'))
        appointment.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        appointment.time = datetime.strptime(data.get('time'), '%H:%M').time()
        
        if data.get('status'):
            appointment.update_status(data.get('status'))
        
        return jsonify({
            'message': 'Appointment updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/api/appointments/delete/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the appointment
        appointment_index = next((i for i, a in enumerate(appointments) if a.id == appointment_id), None)
        
        if appointment_index is None:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Remove the appointment
        appointments.pop(appointment_index)
        
        return jsonify({
            'message': 'Appointment deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@appointments_bp.route('/api/appointments/status/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment_status(appointment_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist", "doctor"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    status = data.get('status')
    
    try:
        # Find the appointment
        appointment = next((a for a in appointments if a.id == appointment_id), None)
        
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Update status
        appointment.update_status(status)
        
        return jsonify({
            'message': 'Appointment status updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400