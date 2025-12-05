import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    MONGO_URI = os.getenv('MONGO_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'poduim')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
