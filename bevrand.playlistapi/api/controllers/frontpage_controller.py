from flask import Blueprint, jsonify, request
import json
from api.services import data_validator
from api import FLASK_TRACER
from api.error_handler.error_model import InvalidUsage
import opentracing
from api.services import frontpage_service
from api.services import logic_for_users_controller_get, \
    logic_for_users_controller_put, \
    logic_for_users_controller_delete, logic_for_users_controller_post


front_page_blueprint = Blueprint('front_page', __name__,)


@front_page_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@front_page_blueprint.route('/api/frontpage', methods=['GET'])
def front_page():
    """
        Endpoint to get frontpage lists and if needed a list of lists
        ---
        tags:
          - FrontPage Methods
        parameters:
          - name: list
            type: string
            in: query
            required: false
            description: specific list that belong to a user
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """
    parent_span = create_parent_trace()
    list_name = request.args.get('list', default=None)
    with opentracing.tracer.start_span('playlist-frontpage', child_of=parent_span) as span:
        if list_name is not None:
            data_validator.validate_json_for_list(list_name)
        return_object = frontpage_service.worker_for_frontpage_get(list_name)
        if return_object['status_code'] is 200:
            res = json.dumps(return_object['body'], indent=4)
            span.log_kv({"status_code": 200, "result": return_object['body']})
            return res, 200
        else:
            res = json.dumps(return_object['body'].__dict__, indent=4)
            return res, return_object['status_code']


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

