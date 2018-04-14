import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['CONNECTION'] ==
            'mongodb://0.0.0.0:27017'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['CONNECTION'] ==
            'mongodb://0.0.0.0:27017'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(
            app.config['CONNECTION'] ==
            'mongodb://dockermongo:27017'
        )


if __name__ == '__main__':
    unittest.main()