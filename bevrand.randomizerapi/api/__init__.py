from os import getenv
from flask import Flask
from flasgger import Swagger


FLASK_TRACER = None


def create_app():
    # instantiate the app
    swagger_config = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'swagger',
                "route": '/swagger.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "specs_route": "/swagger/"
    }

    app = Flask(__name__)
    app.config['SWAGGER'] = {
            "swagger": "3.0",
            'uiversion': "3",
            "info": {
                "title": "BevRand Randomizer Api",
                "version": "1.0"

            }
    }
    Swagger(app, config=swagger_config)

    # set config
    env = getenv('APP_SETTINGS')
    if env is None:
        env = 'Test'
    app_settings = 'api.config.' + env
    app.config.from_object(app_settings)

    # register blueprints
    from api.controllers.randomize_controller import randomize_blueprint
    app.register_blueprint(randomize_blueprint, url_prefix='/api/')


    return app
