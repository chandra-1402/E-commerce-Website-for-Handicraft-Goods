import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tribal-handicraft-super-secret-key-2026'
    
    db_dir = os.path.join(BASE_DIR, 'database')
    os.makedirs(db_dir, exist_ok=True)
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = db_url or ('sqlite:///' + os.path.join(db_dir, 'database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB max upload
