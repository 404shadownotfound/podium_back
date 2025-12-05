# Podium - Real-time Leaderboard Platform

A modern full-stack leaderboard application with Flask backend, React frontend, and real-time WebSocket updates for live score tracking.

## ✨ Features

### Backend (Flask + MongoDB + WebSockets)
- ✅ **REST API** - Full CRUD operations with JSON responses
- ✅ **Real-time Updates** - WebSocket support with Flask-SocketIO
- ✅ **MongoDB Integration** - Cloud-based database with MongoDB Atlas
- ✅ **Automatic Score Calculation** - Team scores auto-update when user scores change
- ✅ **Dynamic Leaderboards** - Ranking system for teams and users
- ✅ **CORS Enabled** - Ready for frontend integration

### Frontend (React + Socket.IO)
- ✅ **Modern UI** - Glassmorphism design with gradient effects
- ✅ **Real-time WebSocket** - Instant leaderboard updates
- ✅ **Live Status Indicator** - Shows WebSocket connection status
- ✅ **View Toggle** - Switch between team and user leaderboards
- ✅ **Responsive Design** - Works on all screen sizes
- ✅ **Smooth Animations** - Professional transitions and effects

## 📁 Project Structure

```
podium/
├── models/
│   ├── database.py       # MongoDB connection
│   ├── team.py          # Team model
│   └── user.py          # User model  
├── routes/
│   ├── team_routes.py   # Team endpoints
│   ├── user_routes.py   # User endpoints
│   ├── leaderboard_routes.py  # Rankings
│   └── admin_routes.py  # Admin utilities
├── utils/
│   └── serializers.py   # JSON helpers
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/    # API client
│   └── package.json
├── app.py               # Flask + WebSocket
├── test_api.py          # Test suite
└── requirements.txt
```

## 🚀 Quick Start

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env file
# MONGO_URI=mongodb+srv://...
# DATABASE_NAME=poduim

# Start server
python app.py
# Runs on http://localhost:8003
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

## 📡 API Endpoints

### Teams
- `GET/POST /api/teams` - List/Create teams
- `GET/PUT/DELETE /api/teams/<id>` - Get/Update/Delete team

### Users
- `GET/POST /api/users` - List/Create users (auto-updates team score)
- `GET/PUT/DELETE /api/users/<id>` - Get/Update/Delete user

### Leaderboard
- `GET /api/leaderboard` - Team rankings
- `GET /api/leaderboard?team_id=<id>` - User rankings for a team

### Admin
- `POST /api/admin/recalculate-scores` - Recalculate all team scores

### WebSocket Events
- **Server → Client:** `leaderboard_update` (broadcast on score changes)
- **Client → Server:** `request_leaderboard` (get current data)

## 💡 Usage Examples

### Create Team
```bash
curl -X POST http://localhost:8003/api/teams \
  -H "Content-Type: application/json" \
  -d '{"name": "Team Alpha"}'
```

### Create User (Auto-updates Team Score)
```bash
curl -X POST http://localhost:8003/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "team_id": "xxx", "score": 150}'
```

### Recalculate Team Scores
```bash
curl -X POST http://localhost:8003/api/admin/recalculate-scores
```

## 🧪 Testing

Run the automated test suite:

```bash
python test_api.py
```

Tests team creation, user creation, score updates, and leaderboard retrieval.

## 🔄 Automatic Score Calculation

Team scores automatically update when:
1. User created → Team score increases
2. User updated → Team score recalculated
3. User deleted → Team score decreases  
4. User changes team → Both teams updated

All WebSocket clients receive instant updates!

## 💾 Database Schema

### Teams Collection (`teams`)
```javascript
{
  _id: ObjectId,
  name: String,
  score: Number,        // Auto-calculated
  created_at: DateTime
}
```

### Users Collection (`user`)
```javascript
{
  _id: ObjectId,
  name: String,
  team_id: ObjectId,
  score: Number,
  created_at: DateTime
}
```

> **Note:** Collection is named `user` (singular) in MongoDB.

## 🎨 Frontend Features

- Real-time WebSocket updates
- Team/User view toggle
- Live connection status
- Medal icons for top 3 (🥇🥈🥉)
- Glassmorphism + gradient design
- Smooth animations

**Tech Stack:** React 18, Vite, Socket.IO Client, Axios

## 🐛 Troubleshooting

### Port 8003 Already in Use
```bash
# Windows
netstat -ano | findstr :8003
taskkill /PID <PID> /F
```

### MongoDB Connection Issues
- Verify `MONGO_URI` in `.env`
- Check IP whitelist in MongoDB Atlas
- Confirm database user permissions

### Collection Name Mismatch
- User collection: `user` (singular)
- Team collection: `teams` (plural)
- Check `models/user.py` and `models/team.py`

### Team Scores Not Updating
1. Check Flask terminal for debug messages
2. Manually recalculate: `curl -X POST http://localhost:8003/api/admin/recalculate-scores`
3. Verify debug logging in models

### WebSocket Not Connecting
- Ensure Flask running on port 8003
- Check browser console for errors
- Verify CORS settings in `app.py`

## 🛠️ Dependencies

**Backend:**
- Flask 3.0.0
- PyMongo 4.6.1
- Flask-CORS 4.0.0
- Flask-SocketIO 5.3.6
- python-dotenv 1.0.0

**Frontend:**
- React 18.2.0
- Socket.IO Client 4.7.2
- Axios 1.6.2
- Vite 5.0.8

## 📝 License

Open source - Educational and commercial use

## 🤝 Resources

- [Flask Docs](https://flask.palletsprojects.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Socket.IO Docs](https://socket.io/docs/)
- [React Docs](https://react.dev/)
