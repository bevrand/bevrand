import os
from flask import Flask, jsonify
from flasgger import Swagger


def create_app():
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
        'title': 'Flask RandomizeApi',
        'uiversion': 3
    }
    Swagger(app, config=swagger_config)
    # instantiate the app
    # set config
   # app_settings = os.getenv('APP_SETTINGS')
   # print(app_settings)
   # app.config.from_object(app_settings)

    # register blueprints
    from project.api.controller import randomize_blueprint
    app.register_blueprint(randomize_blueprint)


    return app