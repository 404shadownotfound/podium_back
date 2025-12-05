from flask import Blueprint, request, jsonify
from models.team import Team
from models.user import User
from utils.serializers import serialize_doc

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get leaderboard rankings
    - No parameters: Returns team leaderboard (sorted by score)
    - With team_id parameter: Returns user leaderboard for that team (sorted by score)
    """
    try:
        team_id = request.args.get('team_id')
        
        if team_id:
            # Get user leaderboard for specific team
            users = User.get_leaderboard_by_team(team_id)
            
            if not users:
                team = Team.get_by_id(team_id)
                if not team:
                    return jsonify({'error': 'Team not found'}), 404
            
            return jsonify({
                'type': 'users',
                'team_id': team_id,
                'leaderboard': [serialize_doc(user) for user in users]
            }), 200
        else:
            # Get team leaderboard
            teams = Team.get_leaderboard()
            
            return jsonify({
                'type': 'teams',
                'leaderboard': [serialize_doc(team) for team in teams]
            }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
