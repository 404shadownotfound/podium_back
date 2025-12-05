from flask import Blueprint, jsonify
from models.team import Team

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/recalculate-scores', methods=['POST'])
def recalculate_all_scores():
    """Recalculate scores for all teams"""
    try:
        teams = Team.get_all()
        updated = 0
        
        for team in teams:
            team_id = str(team['_id'])
            new_score = Team.update_score(team_id)
            print(f"Updated team {team['name']}: score = {new_score}")
            updated += 1
        
        return jsonify({
            'message': f'Successfully recalculated scores for {updated} teams',
            'teams_updated': updated
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
