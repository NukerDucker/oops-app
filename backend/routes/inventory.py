from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

inventory_bp = Blueprint('inventory', __name__)

# These will be imported from app.py
supplies = []
users = []

def find_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None

def find_supply_by_id(supply_id):
    for supply in supplies:
        if supply.id == supply_id:
            return supply
    return None

@inventory_bp.route('/api/supplies', methods=['GET'])
@jwt_required()
def get_supplies():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Simple authorization check - only admin can see supplies
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Return all supplies
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'quantity': s.quantity,
        'unit_price': s.unit_price,
        'category': s.category,
        'total_value': s.total_value()
    } for s in supplies]), 200

@inventory_bp.route('/api/inventory/add', methods=['POST'])
@jwt_required()
def add_inventory():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    try:
        # Create new supply with the provided data
        from modules.supply import Supply
        new_supply = Supply(
            data.get('name'),
            int(data.get('quantity')),
            float(data.get('unit_price')),
            data.get('category')
        )
        
        # Add to our supplies list
        supplies.append(new_supply)
        
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
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    item_id = data.get('id')
    
    try:
        # Find the supply item
        supply_item = next((s for s in supplies if s.id == item_id), None)
        
        if not supply_item:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        # Update the supply item properties
        supply_item.name = data.get('name')
        supply_item.quantity = int(data.get('quantity'))
        supply_item.unit_price = float(data.get('unit_price'))
        supply_item.category = data.get('category')
        
        return jsonify({
            'message': 'Inventory item updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# NEW ROUTE: Remove item entirely
@inventory_bp.route('/api/inventory/remove', methods=['DELETE'])
@jwt_required()
def remove_inventory():
    current_username = get_jwt_identity()
    user = find_user_by_username(current_username)
    
    # Authorization check
    if user.user_type != "admin":
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    inventory_id = data.get('inventoryId')
    
    try:
        # Find the supply item index
        supply_index = next((i for i, s in enumerate(supplies) if s.id == inventory_id), None)
        
        if supply_index is None:
            return jsonify({'error': 'Inventory item not found'}), 404
        
        # Remove the item
        removed_item = supplies.pop(supply_index)
        
        return jsonify({
            'message': f'Successfully removed {removed_item.name} from inventory'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400