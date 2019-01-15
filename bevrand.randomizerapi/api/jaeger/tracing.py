import logging
import os
from jaeger_client import Config


def init_tracer(service):
    jaeger_host = retrieve_jaeger_host()
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    config = Config(config={'sampler': {'type': 'probabilistic', 'param': 0.2},
                            'logging': True,
                            'local_agent':
                            # Also, provide a hostname of Jaeger instance to send traces to.
                                {'reporting_host': jaeger_host}},
                    # Service name can be arbitrary string describing this particular web service.
                    service_name=service)

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


def retrieve_jaeger_host():
    try:
        jaeger_host = os.environ['JAEGER_AGENT_HOST']
    except KeyError:
        jaeger_host = 'localhost'
    return jaeger_host
