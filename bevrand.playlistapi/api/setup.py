import api
from os import getenv
from flask import Flask
from flasgger import Swagger
from jaeger_client import Config
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_all_patches
import logging
from flask_pymongo import PyMongo
import os

try:
    JAEGER_HOST = os.environ['JAEGER_AGENT_HOST']
except:
    JAEGER_HOST = "localhost"
print(JAEGER_HOST)
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
                "title": "BevRand Playlist Api",
                "version": "1.0"

            }
    }
    Swagger(app, config=swagger_config)

    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


    # set config
    env = getenv('APP_SETTINGS')
    if env is None:
        env = 'Test'
    app_settings = 'api.config.' + env
    app.config.from_object(app_settings)

    config = Config(config={'sampler': {'type': 'const', 'param': 1},
                            'logging': True,
                            'local_agent':
                            # Also, provide a hostname of Jaeger instance to send traces to.
                                {'reporting_host': JAEGER_HOST}},
                    # Service name can be arbitrary string describing this particular web service.
                    service_name="PlaylistApi")

    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracer(jaeger_tracer)
    global FLASK_TRACER
    FLASK_TRACER = tracer
    install_all_patches()

    # register blueprints
    from api.controllers.private_controller import private_blueprint
    app.register_blueprint(private_blueprint, url_prefix='/api/v1/private')

    from api.controllers.public_controller import public_blueprint
    app.register_blueprint(public_blueprint, url_prefix='/api/v1/public')

    return app


def create_mongo(app):
    mongo_url = app.config["CONNECTION"] + "/bevrand"
    return PyMongo(app, uri=mongo_url)


app = create_app()

# bind to application package
api.app = app
api.mongo = create_mongo(app)
