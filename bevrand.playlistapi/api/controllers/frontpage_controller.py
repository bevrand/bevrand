from flask import Blueprint, jsonify, request
import json
from api.services import data_validator
from api import flask_tracer
from api.setup import  FLASK_TRACER
from api.error_handler.error_model import InvalidUsage
import opentracing
from api.services.frontpage_service import FrontPageService


front_page_blueprint = Blueprint('front_page', __name__,)


@front_page_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@front_page_blueprint.route('/api/frontpages', methods=['GET'])
def front_page_all_lists():
    """
        Endpoint to get frontpage lists and if needed a list of lists
        ---
        tags:
          - FrontPage Methods
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_frontpage', child_of=parent_span) as span:
        service = FrontPageService()
        front_page_lists = service.retrieve_all_front_page_lists()
        return jsonify({"result": front_page_lists}), 200


@front_page_blueprint.route('/api/frontpages/<listname>', methods=['GET'])
def front_page_list(listname):
    """
        Endpoint to get frontpage lists and if needed a list of lists
        ---
        tags:
          - FrontPage Methods
        parameters:
          - name: list
            in: path
            type: string
            required: true
            description: specific frontpage list
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_frontpage', child_of=parent_span) as span:
        data_validator.validate_json_for_list(listname)
        service = FrontPageService()
        front_page_lists = service.retrieve_front_page_list(listname)
        return jsonify({"result": front_page_lists.__dict__}), 200


@front_page_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('error', child_of=parent_span) as span:
        span.log_kv({"status_code": error.status_code, "error": error.message})
        if error.meta is not None:
            span.log_kv({"meta": error.meta})
    return response


@FLASK_TRACER.trace()
def create_parent_trace():
    parent_span = FLASK_TRACER.get_span(request)
    parent_span.set_tag('http.url', request.base_url)
    parent_span.set_tag('http.method', request.method)
    parent_span.set_tag('body', request.json)
    return parent_span

