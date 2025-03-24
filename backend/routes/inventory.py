from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modules.system import System
from modules.supply import Supply

inventory_bp = Blueprint('inventory', __name__)
system_service = System()

def init_inventory_routes(blueprint, system):
    """Initialize inventory routes with system dependency"""
    global system_service
    system_service = system
    return blueprint

@inventory_bp.route('/api/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'quantity': s.quantity,
        'unit_price': s.unit_price,
        'category': s.category,
        'total_value': s.total_value()
    } for s in system_service._supplies.values()]), 200

@inventory_bp.route('/api/inventory/add', methods=['POST'])
@jwt_required()
def add_inventory():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        
        new_supply = Supply(
            data.get('name'),
            int(data.get('quantity')),
            float(data.get('unit_price')),
            data.get('category')
        )
        
        
        success, message = system_service.add_supply(new_supply)
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': 'Inventory item added successfully',
            'id': new_supply.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@inventory_bp.route('/api/inventory/update', methods=['PUT'])
@jwt_required()
def update_inventory():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    if not user or user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    item_id = int(data.get('id'))
    
    try:
        supply_item = system_service._supplies.get(item_id)
        
        if not supply_item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        # Update properties of the existing object instead of creating a new one
        supply_item.name = data.get('name')
        supply_item.quantity = int(data.get('quantity'))
        supply_item.unit_price = float(data.get('unit_price'))
        supply_item.category = data.get('category')
        
        # Pass the modified existing object
        success, message = system_service.update_supply(item_id, supply_item)
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': 'Inventory item updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@inventory_bp.route('/api/inventory/remove', methods=['DELETE'])
@jwt_required()
def remove_inventory():
    current_username = get_jwt_identity()
    user = system_service.get_user_from_username(current_username)
    
    
    if not user or user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    inventory_id = int(data.get('inventoryId'))
    
    try:
        
        supply_item = system_service._supplies.get(inventory_id)
        
        if not supply_item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        
        success, message = system_service.delete_supply(inventory_id)
        
        if not success:
            return jsonify({'error': message}), 400
        
        return jsonify({
            'message': f'Successfully removed {supply_item.name} from inventory'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
