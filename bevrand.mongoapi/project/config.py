import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CONNECTION = 'mongodb://localhost:27017'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    CONNECTION = 'mongodb://0.0.0.0:27017'


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    CONNECTION = 'mongodb://0.0.0.0:27017'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    CONNECTION = 'mongodb://dockermongo:27017'