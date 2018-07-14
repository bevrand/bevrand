from os import getenv
from flask import Flask
from flasgger import Swagger
from jaeger_client import Config
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_all_patches
import logging


JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')


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

    config = Config(config={'sampler': {'type': 'const', 'param': 1},
                            'logging': True,
                            'local_agent':
                            # Also, provide a hostname of Jaeger instance to send traces to.
                                {'reporting_host': JAEGER_HOST}},
                    # Service name can be arbitrary string describing this particular web service.
                    service_name="playlist-api")

    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracer(jaeger_tracer)
    global FLASK_TRACER
    FLASK_TRACER = tracer
    install_all_patches()

    # set config
    env = getenv('APP_SETTINGS')
    if env is None:
        env = 'Test'
    app_settings = 'api.config.' + env
    app.config.from_object(app_settings)

    # register blueprints
    from api.controllers.frontpage_controller import users_blueprint
    app.register_blueprint(users_blueprint)


    return app