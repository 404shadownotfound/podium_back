from bson import ObjectId
from datetime import datetime
from models.database import get_database

class User:
    """User model"""
    
    @staticmethod
    def get_collection():
        """Get users collection"""
        db = get_database()
        return db['user']
    
    @staticmethod
    def create(name, team_id, score=0):
        """Create a new user"""
        try:
            user = {
                'name': name,
                'team_id': ObjectId(team_id),
                'score': score,
                'created_at': datetime.utcnow()
            }
            result = User.get_collection().insert_one(user)
            user['_id'] = result.inserted_id
            
            print(f"[DEBUG] Created user '{name}' with score {score} for team {team_id}")
            
            # Update team score
            from models.team import Team
            new_score = Team.update_score(team_id)
            print(f"[DEBUG] Updated team {team_id} score to {new_score}")
            
            return user
        except Exception as e:
            print(f"[ERROR] Failed to create user: {e}")
            raise
    
    @staticmethod
    def get_all():
        """Get all users"""
        users = list(User.get_collection().find())
        return users
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            user = User.get_collection().find_one({'_id': ObjectId(user_id)})
            return user
        except Exception:
            return None
    
    @staticmethod
    def get_by_team(team_id):
        """Get all users in a team"""
        try:
            users = list(User.get_collection().find({'team_id': ObjectId(team_id)}))
            return users
        except Exception:
            return []
    
    @staticmethod
    def update(user_id, data):
        """Update user"""
        try:
            # Get current user to check if team changed
            current_user = User.get_by_id(user_id)
            if not current_user:
                return False
            
            old_team_id = current_user.get('team_id')
            
            update_data = {}
            if 'name' in data:
                update_data['name'] = data['name']
            if 'score' in data:
                update_data['score'] = data['score']
            if 'team_id' in data:
                update_data['team_id'] = ObjectId(data['team_id'])
            
            result = User.get_collection().update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            
            # Update team scores
            from models.team import Team
            if result.modified_count > 0:
                # Update old team score
                Team.update_score(str(old_team_id))
                # If team changed, update new team score
                if 'team_id' in data and str(old_team_id) != data['team_id']:
                    Team.update_score(data['team_id'])
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    @staticmethod
    def delete(user_id):
        """Delete user"""
        try:
            # Get user to update team score after deletion
            user = User.get_by_id(user_id)
            if not user:
                return False
            
            team_id = user.get('team_id')
            
            result = User.get_collection().delete_one({'_id': ObjectId(user_id)})
            
            # Update team score
            if result.deleted_count > 0:
                from models.team import Team
                Team.update_score(str(team_id))
            
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    @staticmethod
    def get_leaderboard_by_team(team_id):
        """Get users sorted by score for a specific team"""
        try:
            print(f"[DEBUG] Querying users for team_id: {team_id}")
            users = list(User.get_collection().find(
                {'team_id': ObjectId(team_id)}
            ).sort('score', -1))
            print(f"[DEBUG] Found {len(users)} users")
            return users
        except Exception as e:
            print(f"[ERROR] Error in get_leaderboard_by_team: {e}")
            return []
