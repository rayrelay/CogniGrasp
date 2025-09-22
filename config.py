import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cognigrasp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False