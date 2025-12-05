"""
Test script for Podium API
Tests user creation and automatic team score updates
"""

import requests
import json

API_BASE = "http://localhost:8003"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_create_team():
    """Test creating a new team"""
    print_section("TEST 1: Create Team")
    
    response = requests.post(
        f"{API_BASE}/api/teams",
        json={"name": f"Test Team Alpha"}
    )
    
    if response.status_code == 201:
        team = response.json()
        print(f"✓ Team created successfully!")
        print(f"  - ID: {team['id']}")
        print(f"  - Name: {team['name']}")
        print(f"  - Initial Score: {team['score']}")
        return team['id']
    else:
        print(f"✗ Failed to create team: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def test_create_user(team_id, name, score):
    """Test creating a user and check if team score updates"""
    print_section(f"TEST 2: Create User '{name}' with {score} points")
    
    response = requests.post(
        f"{API_BASE}/api/users",
        json={
            "name": name,
            "team_id": team_id,
            "score": score
        }
    )
    
    if response.status_code == 201:
        user = response.json()
        print(f"✓ User created successfully!")
        print(f"  - ID: {user['id']}")
        print(f"  - Name: {user['name']}")
        print(f"  - Score: {user['score']}")
        return user['id']
    else:
        print(f"✗ Failed to create user: {response.status_code}")
        print(f"  Response: {response.text}")
        return None

def test_get_team(team_id):
    """Get team details and check score"""
    print_section("TEST 3: Verify Team Score Updated")
    
    response = requests.get(f"{API_BASE}/api/teams/{team_id}")
    
    if response.status_code == 200:
        team = response.json()
        print(f"✓ Team retrieved successfully!")
        print(f"  - Name: {team['name']}")
        print(f"  - Current Score: {team['score']}")
        return team['score']
    else:
        print(f"✗ Failed to get team: {response.status_code}")
        return None

def test_update_user(user_id, new_score):
    """Test updating user score"""
    print_section(f"TEST 4: Update User Score to {new_score}")
    
    response = requests.put(
        f"{API_BASE}/api/users/{user_id}",
        json={"score": new_score}
    )
    
    if response.status_code == 200:
        user = response.json()
        print(f"✓ User updated successfully!")
        print(f"  - Name: {user['name']}")
        print(f"  - New Score: {user['score']}")
        return True
    else:
        print(f"✗ Failed to update user: {response.status_code}")
        return False

def test_leaderboard():
    """Test getting team leaderboard"""
    print_section("TEST 5: Get Team Leaderboard")
    
    response = requests.get(f"{API_BASE}/api/leaderboard")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Leaderboard retrieved successfully!")
        print(f"  - Type: {data['type']}")
        print(f"  - Teams count: {len(data['leaderboard'])}")
        
        for i, team in enumerate(data['leaderboard'][:5], 1):
            print(f"  {i}. {team['name']} - {team['score']} pts")
        
        return True
    else:
        print(f"✗ Failed to get leaderboard: {response.status_code}")
        return False

def main():
    print("\n" + "🚀 PODIUM API TEST SUITE" + "\n")
    print("Testing automatic team score calculation...")
    
    try:
        # Test 1: Create a team
        team_id = test_create_team()
        if not team_id:
            print("\n❌ Test suite failed at team creation")
            return
        
        # Test 2: Create first user
        user1_id = test_create_user(team_id, "Alice", 100)
        if not user1_id:
            print("\n❌ Test suite failed at user creation")
            return
        
        # Test 3: Check team score (should be 100)
        score1 = test_get_team(team_id)
        if score1 == 100:
            print("  ✓ Score is correct: 100")
        else:
            print(f"  ✗ Score is incorrect! Expected 100, got {score1}")
        
        # Test 4: Create second user
        user2_id = test_create_user(team_id, "Bob", 150)
        
        # Test 5: Check team score again (should be 250)
        score2 = test_get_team(team_id)
        if score2 == 250:
            print("  ✓ Score is correct: 250")
        else:
            print(f"  ✗ Score is incorrect! Expected 250, got {score2}")
        
        # Test 6: Update user score
        test_update_user(user1_id, 200)
        
        # Test 7: Check team score after update (should be 350)
        score3 = test_get_team(team_id)
        if score3 == 350:
            print("  ✓ Score is correct: 350")
        else:
            print(f"  ✗ Score is incorrect! Expected 350, got {score3}")
        
        # Test 8: Get leaderboard
        test_leaderboard()
        
        print_section("✅ ALL TESTS COMPLETED")
        print("\nSummary:")
        print(f"  - Team created: {team_id}")
        print(f"  - Users created: 2")
        print(f"  - Final team score: {score3}")
        print(f"  - Test result: {'PASS' if score3 == 350 else 'FAIL'}")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Flask server!")
        print("   Make sure the server is running on http://localhost:8003")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
