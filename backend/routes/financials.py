from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, timedelta

financials_bp = Blueprint('financials', __name__)

# These will be imported from app.py
patients = []
users = []
system = None

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

@financials_bp.route('/api/patients/<int:patient_id>/fees', methods=['POST'])
@jwt_required()
def add_patient_fee(patient_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Create new fee
        from modules.fee import Fee
        from datetime import datetime
        new_fee = Fee(
            patient_id,
            float(data.get('amount')),
            data.get('description'),
            datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else date.today()
        )
        
        # Add fee to patient
        result, message = patient.add_fee(new_fee)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message,
            'fee_id': new_fee.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@financials_bp.route('/api/patients/<int:patient_id>/fees/<int:fee_id>', methods=['PUT'])
@jwt_required()
def update_patient_fee(patient_id, fee_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Get the existing fee
        existing_fee = patient.get_fee(fee_id)
        if not existing_fee:
            return jsonify({'error': 'Fee not found'}), 404
        
        # Create updated fee
        from modules.fee import Fee
        from datetime import datetime
        updated_fee = Fee(
            patient_id,
            float(data.get('amount')),
            data.get('description'),
            datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else existing_fee.date
        )
        updated_fee.id = fee_id  # Keep the same ID
        
        # Update fee
        result, message = patient.update_fee(fee_id, updated_fee)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@financials_bp.route('/api/patients/<int:patient_id>/fees/<int:fee_id>', methods=['DELETE'])
@jwt_required()
def delete_patient_fee(patient_id, fee_id):
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Find the patient
        patient = next((p for p in patients if p.id == patient_id), None)
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Delete fee
        result, message = patient.remove_fee(fee_id)
        
        if not result:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': message
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@financials_bp.route('/api/financial-report', methods=['GET'])
@jwt_required()
def get_financial_report():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check
    if user.user_type not in ["admin", "receptionist"]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    start_date = request.args.get('start_date', (date.today() - timedelta(days=30)).isoformat())
    end_date = request.args.get('end_date', date.today().isoformat())
    
    try:
        # For demonstration, we'll use the system's generate_financial_report method
        success, report = system.generate_financial_report(start_date, end_date)
        
        if not success:
            return jsonify({'error': 'Failed to generate report'}), 400
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400