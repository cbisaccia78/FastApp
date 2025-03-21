import os

class Config:
    def __init__(self):
        self.testing = False

        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()