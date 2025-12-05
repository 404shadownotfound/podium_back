from bson import ObjectId
from datetime import datetime
from models.database import get_database

class Team:
    """Team model"""
    
    @staticmethod
    def get_collection():
        """Get teams collection"""
        db = get_database()
        return db['teams']
    
    @staticmethod
    def create(name):
        """Create a new team"""
        team = {
            'name': name,
            'score': 0,
            'created_at': datetime.utcnow()
        }
        result = Team.get_collection().insert_one(team)
        team['_id'] = result.inserted_id
        return team
    
    @staticmethod
    def get_all():
        """Get all teams"""
        teams = list(Team.get_collection().find())
        return teams
    
    @staticmethod
    def get_by_id(team_id):
        """Get team by ID"""
        try:
            team = Team.get_collection().find_one({'_id': ObjectId(team_id)})
            return team
        except Exception:
            return None
    
    @staticmethod
    def update(team_id, data):
        """Update team"""
        try:
            update_data = {}
            if 'name' in data:
                update_data['name'] = data['name']
            if 'score' in data:
                update_data['score'] = data['score']
            
            result = Team.get_collection().update_one(
                {'_id': ObjectId(team_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception:
            return False
    
    @staticmethod
    def delete(team_id):
        """Delete team"""
        try:
            result = Team.get_collection().delete_one({'_id': ObjectId(team_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    @staticmethod
    def update_score(team_id):
        """Calculate and update team score from user scores"""
        from models.user import User
        try:
            print(f"[DEBUG] Calculating score for team {team_id}")
            # Get all users for this team
            users = User.get_by_team(team_id)
            print(f"[DEBUG] Found {len(users)} users for team {team_id}")
            
            # Calculate total score
            total_score = sum(user.get('score', 0) for user in users)
            print(f"[DEBUG] Total score calculated: {total_score}")
            
            # Update team score
            result = Team.get_collection().update_one(
                {'_id': ObjectId(team_id)},
                {'$set': {'score': total_score}}
            )
            print(f"[DEBUG] MongoDB update result: modified_count={result.modified_count}")
            
            return total_score
        except Exception as e:
            print(f"[ERROR] Error updating team score: {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    @staticmethod
    def get_leaderboard():
        """Get teams sorted by score (descending)"""
        teams = list(Team.get_collection().find().sort('score', -1))
        return teams
