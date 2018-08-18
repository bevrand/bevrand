from flask import Blueprint, jsonify, request
from api.services import data_validator
from api.setup import FLASK_TRACER
from api.error_handler.error_model import InvalidUsage
import opentracing
from api.services.users_service import UsersService


users_blueprint = Blueprint('users', __name__,)


@users_blueprint.route('/api/users', methods=['GET'])
def list_of_all_users():
    """
        Endpoint to get all users
        ---
        tags:
          - Users Methods
        responses:
          200:
            description: All users currently known
          400:
            description: Invalid Mongo operation
          503:
            description: No mongo connection
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_get_all_users', child_of=parent_span) as span:
      service = UsersService()
      all_users = service.retrieve_all_users()
      span.log_kv({"status_code": 200, "result": all_users})
      return jsonify(all_users), 200


@users_blueprint.route('/api/users/<user_name>', methods=['GET'])
def lists_for_specific_user(user_name):
    """
        Endpoint to get all lists for a user
        ---
        tags:
          - Users Methods
        parameters:
          - name: user
            type: string
            in: path
            required: true
            description: user you want to see the lists of
        responses:
          200:
            description: Your list is correct see response
          400:
            description: Invalid Mongo operation
          503:
            description: No mongo connection
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_get_all_user_lists', child_of=parent_span) as span:
      data_validator.validate_json_for_user(user_name)
      service = UsersService()
      result = service.retrieve_all_lists_for_user(user_name)
      span.log_kv({"status_code": 200, "result": result})
      return jsonify(result), 200


@users_blueprint.errorhandler(InvalidUsage)
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

