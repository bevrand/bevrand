import os
from flask_testing import TestCase

from api.setup import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Development')
        return app

    def test_app_is_development(self):
        assert app.config['DEBUG'] == True
        connection = 'mongodb://0.0.0.0:27017/admin'
        assert app.config['CONNECTION'] == connection

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Test')
        return app

    def test_app_is_testing(self):
        assert app.config['DEBUG'] == True
        assert app.config['TESTING'] == True
        connection = 'mongodb://0.0.0.0:27017/admin'
        os.environ["MONGO_URL"] = connection
        assert app.config['CONNECTION'] == connection


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Production')
        return app

    def test_app_is_production(self):
        assert app.config['DEBUG'] == False
        assert app.config['TESTING'] == False
