from flask import Blueprint, jsonify, request
from flasgger import swag_from
from api.services import data_validator
from api.setup import FLASK_TRACER
from api.error_handler.error_model import InvalidUsage
import opentracing
from api.services.users_service import UsersService
from api.services.lists_service import ListsService


users_blueprint = Blueprint('users', __name__,)


@users_blueprint.route('/<user_name>', methods=['GET'])
@swag_from('../swagger/private_users_get.yml')
def lists_for_specific_user(user_name):
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_get_all_user_lists', child_of=parent_span) as span:
        data_validator.validate_user_name(user_name)
        service = UsersService()
        result = service.retrieve_all_lists_for_user(user_name)
        span.log_kv({"status_code": 200, "result": result})
        return jsonify(result), 200


@users_blueprint.route('/<user_name>/<play_list_name>', methods=['GET'])
@swag_from('../swagger/private_users_get_playlist.yml')
def specific_list_for_specific_user(user_name, play_list_name):
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_get', child_of=parent_span) as span:
        data_validator.validate_user_name(user_name)
        data_validator.validate_play_list(play_list_name)
        service = ListsService()
        result = service.get_specific_user_list(user_name, play_list_name)
        return jsonify({"result": result.__dict__}), 200


@users_blueprint.route('/<user_name>', methods=['POST'])
@swag_from('../swagger/private_users_post.yml')
def create_new_list(user_name):
    parent_span = create_parent_trace()
    json_body = request.json
    with opentracing.tracer.start_span('playlist_list_post', child_of=parent_span) as span:
        data_validator.validate_user_name(user_name)
        service = ListsService()
        service.post_new_list(json_body, user_name)
        span.log_kv({"status_code": 201, "result": ""})
        return '', 201


@users_blueprint.route('/<user_name>', methods=['DELETE'])
@swag_from('../swagger/private_users_delete.yml')
def remove_all_user_lists(user_name):
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_delete', child_of=parent_span) as span:
        data_validator.validate_user_name(user_name)
        service = ListsService()
        service.delete_all_lists_for_a_user(user_name)
        span.log_kv({"status_code": 204, "result": ""})
        return '', 204


@users_blueprint.route('/<user_name>/<play_list_name>', methods=['DELETE'])
@swag_from('../swagger/private_users_delete_playlist.yml')
def remove_user_list(user_name, play_list_name):
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_delete', child_of=parent_span) as span:
        data_validator.validate_user_name(user_name)
        data_validator.validate_play_list(play_list_name)
        service = ListsService()
        service.delete_user_list(user_name, play_list_name)
        span.log_kv({"status_code": 204, "result": ""})
        return '', 204


@users_blueprint.route('/<user_name>/<play_list_name>', methods=['PUT'])
@swag_from('../swagger/private_users_update.yml')
def update_user_list(user_name, play_list_name):
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_update', child_of=parent_span) as span:
        json_body = request.json
        data_validator.validate_user_name(user_name)
        data_validator.validate_play_list(play_list_name)
        service = ListsService()
        service.update_list(user_name, play_list_name, json_body)
        span.log_kv({"status_code": 204, "result": ""})
        return '', 204





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

