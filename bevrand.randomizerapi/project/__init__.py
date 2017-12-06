import os
from flask import Flask, jsonify
from flasgger import Swagger


def create_app():
    # instantiate the app
    app = Flask(__name__)
    Swagger(app)

    # set config
   # app_settings = os.getenv('APP_SETTINGS')
   # print(app_settings)
   # app.config.from_object(app_settings)

    # register blueprints
    from project.api.controller import randomize_blueprint
    app.register_blueprint(randomize_blueprint)


    return app