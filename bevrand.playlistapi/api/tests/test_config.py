import os
from flask_testing import TestCase

from api.setup import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):

    check_url = '0.0.0.0'

    def create_app(self):
        app.config.from_object('api.config.Development')
        return app

    def test_app_is_development(self):
        assert app.config['DEBUG']
        connection = 'mongodb://{0}:27017/admin'.format(self.check_url)
        assert app.config['CONNECTION'] == connection


class TestTestingConfig(TestCase):

    check_url = '0.0.0.0'

    def create_app(self):
        app.config.from_object('api.config.Test')
        return app

    def test_app_is_testing(self):
        assert app.config['DEBUG']
        assert app.config['TESTING']
        connection = 'mongodb://{0}:27017/admin'.format(self.check_url)
        os.environ["MONGO_URL"] = connection
        assert app.config['CONNECTION'] == connection


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Production')
        return app

    def test_app_is_production(self):
        assert not app.config['DEBUG']
        assert not app.config['TESTING']
