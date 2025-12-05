from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Database connection manager"""
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish connection to MongoDB"""
        if self._client is None:
            try:
                mongo_uri = os.getenv('MONGO_URI')
                database_name = os.getenv('DATABASE_NAME', 'poduim')
                
                if not mongo_uri:
                    raise ValueError("MONGO_URI not found in environment variables")
                
                self._client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                # Test connection
                self._client.admin.command('ping')
                self._db = self._client[database_name]
                print(f"[OK] Successfully connected to MongoDB database: {database_name}")
                
            except ConnectionFailure as e:
                print(f"[ERROR] Failed to connect to MongoDB: {e}")
                raise
            except Exception as e:
                print(f"[ERROR] Error connecting to database: {e}")
                raise
        
        return self._db
    
    def get_database(self):
        """Get database instance"""
        if self._db is None:
            return self.connect()
        return self._db
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("[OK] Database connection closed")

# Global database instance
db_manager = Database()

def get_database():
    """Helper function to get database instance"""
    return db_manager.get_database()
