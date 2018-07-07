import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CONNECTION = os.environ.get('REDIS_URL')

class Development(BaseConfig):
    """Development configuration"""
    DEBUG = True


class Testing(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class Production(BaseConfig):
    """Production configuration"""
    DEBUG = False


