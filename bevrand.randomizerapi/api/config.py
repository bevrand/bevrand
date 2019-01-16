class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False


class Development(BaseConfig):
    """Development configuration"""
    DEBUG = True


class Test(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


class Coverage(BaseConfig):
    DEBUG = False


class Production(BaseConfig):
    """Production configuration"""
    DEBUG = False



