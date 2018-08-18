import unittest

from flask import current_app
from flask_testing import TestCase

from api.setup import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Development')
        return app

    def test_app_is_development(self):
        assert app.config['DEBUG'] == True
        assert app.config['CONNECTION'] == 'mongodb://0.0.0.0:27017'



class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Test')
        return app

    def test_app_is_testing(self):
        assert app.config['DEBUG'] == True
        assert app.config['TESTING'] == True
        assert app.config['CONNECTION'] == 'mongodb://0.0.0.0:27017'


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Production')
        return app

    def test_app_is_production(self):
        assert app.config['DEBUG'] == False
        assert app.config['TESTING'] == False
