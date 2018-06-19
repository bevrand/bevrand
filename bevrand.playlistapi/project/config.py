import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CONNECTION = os.environ.get('MONGO_URL')


class development(BaseConfig):
    """Development configuration"""
    DEBUG = True


class testing(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    CONNECTION = 'mongodb://0.0.0.0:27017'


class production(BaseConfig):
    """Production configuration"""
    DEBUG = False
