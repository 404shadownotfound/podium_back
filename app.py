from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from config import config
from models.database import get_database

# Import routes
from routes.team_routes import team_bp
from routes.user_routes import user_bp
from routes.leaderboard_routes import leaderboard_bp
from routes.admin_routes import admin_bp

# Global SocketIO instance
socketio = None

def create_app(config_name='development'):
    """Application factory"""
    global socketio
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize SocketIO with auto-detected async mode
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Initialize database connection
    try:
        db = get_database()
        print(f"[OK] Flask app connected to database: {app.config['DATABASE_NAME']}")
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
    
    # Register blueprints
    app.register_blueprint(team_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(admin_bp)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to Podium API',
            'endpoints': {
                'teams': '/api/teams',
                'users': '/api/users',
                'leaderboard': '/api/leaderboard'
            },
            'websocket': 'Socket.IO enabled for real-time updates'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # WebSocket event handlers
    @socketio.on('connect')
    def handle_connect():
        print('[WebSocket] Client connected')
        emit('connection_response', {'status': 'connected'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('[WebSocket] Client disconnected')
    
    @socketio.on('request_leaderboard')
    def handle_leaderboard_request(data):
        """Handle leaderboard data request via WebSocket"""
        from models.team import Team
        from models.user import User
        from utils.serializers import serialize_doc
        
        team_id = data.get('team_id')
        
        if team_id:
            # Send user leaderboard
            users = User.get_leaderboard_by_team(team_id)
            emit('leaderboard_update', {
                'type': 'users',
                'team_id': team_id,
                'leaderboard': [serialize_doc(user) for user in users]
            })
        else:
            # Send team leaderboard
            teams = Team.get_leaderboard()
            emit('leaderboard_update', {
                'type': 'teams',
                'leaderboard': [serialize_doc(team) for team in teams]
            })
    
    return app

def broadcast_leaderboard_update():
    """Broadcast leaderboard update to all connected clients"""
    if socketio:
        from models.team import Team
        from utils.serializers import serialize_doc
        
        teams = Team.get_leaderboard()
        socketio.emit('leaderboard_update', {
            'type': 'teams',
            'leaderboard': [serialize_doc(team) for team in teams]
        }, broadcast=True)

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print(">>> Podium API Server Starting...")
    print("="*50)
    print("\n[Available Endpoints]")
    print("  - GET  /                     - API information")
    print("  - GET  /api/teams            - Get all teams")
    print("  - POST /api/teams            - Create team")
    print("  - GET  /api/teams/<id>       - Get team by ID")
    print("  - PUT  /api/teams/<id>       - Update team")
    print("  - DELETE /api/teams/<id>     - Delete team")
    print("  - GET  /api/users            - Get all users")
    print("  - POST /api/users            - Create user")
    print("  - GET  /api/users/<id>       - Get user by ID")
    print("  - PUT  /api/users/<id>       - Update user")
    print("  - DELETE /api/users/<id>     - Delete user")
    print("  - GET  /api/leaderboard      - Get team rankings")
    print("  - GET  /api/leaderboard?team_id=<id> - Get user rankings for team")
    print("\n[WebSocket Support]")
    print("  - Real-time leaderboard updates enabled")
    print("  - Socket.IO endpoint: ws://localhost:8003")
    print("\n" + "="*50 + "\n")
    
    socketio.run(app, host='0.0.0.0', port=8003, debug=True, allow_unsafe_werkzeug=True)
