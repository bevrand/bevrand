import os
from flask import Flask, jsonify
from flasgger import Swagger

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
        'title': 'Flask MongoApi',
        'uiversion': 3
    }
    Swagger(app, config=swagger_config)

    # set config
    app_settings = 'project.config.' + os.getenv('APP_SETTINGS')
    print(app_settings)
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.controller import users_blueprint
    app.register_blueprint(users_blueprint)


    return app