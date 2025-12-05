from flask import Blueprint, request, jsonify
from models.user import User
from utils.serializers import serialize_doc

user_bp = Blueprint('users', __name__)

def broadcast_update():
    """Broadcast leaderboard update via WebSocket"""
    try:
        from app import broadcast_leaderboard_update
        broadcast_leaderboard_update()
    except Exception as e:
        print(f"[WebSocket] Broadcast failed: {e}")

@user_bp.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'team_id' not in data:
            return jsonify({'error': 'User name and team_id are required'}), 400
        
        score = data.get('score', 0)
        user = User.create(data['name'], data['team_id'], score)
        
        # Broadcast update via WebSocket
        broadcast_update()
        
        return jsonify(serialize_doc(user)), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.get_all()
        return jsonify([serialize_doc(user) for user in users]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user"""
    try:
        user = User.get_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(serialize_doc(user)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        success = User.update(user_id, data)
        
        if not success:
            return jsonify({'error': 'User not found or update failed'}), 404
        
        # Broadcast update via WebSocket
        broadcast_update()
        
        user = User.get_by_id(user_id)
        return jsonify(serialize_doc(user)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        success = User.delete(user_id)
        
        if not success:
            return jsonify({'error': 'User not found'}), 404
        
        # Broadcast update via WebSocket
        broadcast_update()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
