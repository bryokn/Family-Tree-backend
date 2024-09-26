import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/familytree')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://avnadmin:AVNS_w-TMv1YoSerycCaA-71@family_treepg-familytree-family-tree.h.aivencloud.com:28889/defaultdb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    
    # Database connection details
    # DB_USER = os.getenv('DB_USER', 'postgres')  # Default to 'postgres'
    # DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
    # DB_HOST = os.getenv('DB_HOST', 'localhost')
    # DB_PORT = os.getenv('DB_PORT', '5432')
    # DB_NAME = os.getenv('DB_NAME', 'familytree')