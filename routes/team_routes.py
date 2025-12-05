from flask import Blueprint, request, jsonify
from models.team import Team
from utils.serializers import serialize_doc

team_bp = Blueprint('teams', __name__)

@team_bp.route('/api/teams', methods=['POST'])
def create_team():
    """Create a new team"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Team name is required'}), 400
        
        team = Team.create(data['name'])
        return jsonify(serialize_doc(team)), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams"""
    try:
        teams = Team.get_all()
        return jsonify([serialize_doc(team) for team in teams]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/api/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """Get a specific team"""
    try:
        team = Team.get_by_id(team_id)
        
        if not team:
            return jsonify({'error': 'Team not found'}), 404
        
        return jsonify(serialize_doc(team)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/api/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    """Update a team"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        success = Team.update(team_id, data)
        
        if not success:
            return jsonify({'error': 'Team not found or update failed'}), 404
        
        team = Team.get_by_id(team_id)
        return jsonify(serialize_doc(team)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@team_bp.route('/api/teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Delete a team"""
    try:
        success = Team.delete(team_id)
        
        if not success:
            return jsonify({'error': 'Team not found'}), 404
        
        return jsonify({'message': 'Team deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
