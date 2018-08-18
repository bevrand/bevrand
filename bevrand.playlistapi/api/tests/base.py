from flask_testing import TestCase

from api.setup import create_app


app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('api.config.Test')
        return app