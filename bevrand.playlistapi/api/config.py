import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CONNECTION = os.environ.get('MONGO_URL')


class Development(BaseConfig):
    """Development configuration"""
    DEBUG = True
    CONNECTION = 'mongodb://0.0.0.0:27017'


class Test(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    CONNECTION = 'mongodb://0.0.0.0:27017'


class Production(BaseConfig):
    """Production configuration"""
    DEBUG = False

