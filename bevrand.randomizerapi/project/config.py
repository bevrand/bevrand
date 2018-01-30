import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CONNECTION = os.environ.get('REDIS_URL')


class development(BaseConfig):
    """Development configuration"""
    DEBUG = True


class testing(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class production(BaseConfig):
    """Production configuration"""
    DEBUG = False

