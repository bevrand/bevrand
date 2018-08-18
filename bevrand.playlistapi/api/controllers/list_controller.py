from flask import Blueprint, jsonify, request
import json
from api.services import data_validator
from api import flask_tracer
from api.setup import FLASK_TRACER
from api.error_handler.error_model import InvalidUsage
import opentracing
from api.services.lists_service import ListsService


list_blueprint = Blueprint('lists', __name__,)


@list_blueprint.route('/api/lists', methods=['POST'])
def create_new_list():
    """
        Endpoint to insert new lists into Mongo
        ---
        tags:
          - List Methods
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                user:
                  type: string
                  description: The user to insert
                list:
                  type: string
                  description: The list to insert
                displayName:
                  type: string
                  description: The name you want people to see
                imageUrl:
                  type: string
                  description: The image to upload
                beverages:
                  type: array
                  items:
                    schema:
                        type: string
              example:
                user: Marvin
                list: Paranoid
                displayName: I am so depressed
                imageUrl: http://whatever.com
                beverages: [beer, wine]
        responses:
          200:
            description: Your list has been inserted
          400:
            description: Invalid Mongo operation
          503:
            description: No mongo connection
    """
    parent_span = create_parent_trace()
    json_body = request.json
    with opentracing.tracer.start_span('playlist_list_post', child_of=parent_span) as span:
        data_validator.validate_json_for_post(json_body)
        service = ListsService()
        service.post_new_list(json_body)
        span.log_kv({"status_code": 201, "result": result})
        return 201


@list_blueprint.route('/api/lists/<user_name>', methods=['DELETE'])
def remove_user_list(user_name):
    """
        Endpoint to remove a specific list or a complete user
        ---
        tags:
          - List Methods
        parameters:
          - name: user_name
            type: string
            in: path
            required: true
            description: user you want to query
          - name: list
            type: string
            in: query
            required: false
            description: specific list that belong to a user
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list was deleted
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_delete', child_of=parent_span) as span:
        validation = data_validator.validate_json_for_user(user_name)
        to_remove_list = request.args.get('list', default=None)
        if to_remove_list is not None:
            data_validator.validate_json_for_list(to_remove_list)
        service = ListsService()
        service.delete_user_list(user_name, to_remove_list)
        span.log_kv({"status_code": 204, "result": ""})
        return 204



@list_blueprint.route('/api/lists/<user_name>/<list_name>', methods=['PUT'])
def update_user_list(user_name, list_name):
    """
         Endpoint to update a user or a list
        ---
        tags:
          - List Methods
        parameters:
          - name: user_name
            type: string
            in: path
            required: true
            description: user you want to update
          - name: list_name
            type: string
            in: path
            required: true
            description: list you want to update
          - name: body
            in: body
            required: true
            schema:
              properties:
                user:
                  type: string
                  description: The user to insert
                list:
                  type: string
                  description: The list to insert
                displayName:
                  type: string
                  description: The name you want people to see
                imageUrl:
                  type: string
                  description: The image to upload
                beverages:
                  type: array
                  items:
                    schema:
                        type: string
              example:
                user: Marvin
                list: Paranoid
                displayName: I am so depressed
                imageUrl: http://whatever.com
                beverages: [beer, wine]
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list was deleted
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_update', child_of=parent_span) as span:
        json_body = request.json
        data_validator.validate_json_for_post(json_body)
        data_validator.validate_json_for_user(user_name)
        data_validator.validate_json_for_list(list_name)
        service = ListsService()
        service.worker_for_update(user_name, list_name, json_body)
        span.log_kv({"status_code": 204, "result": ""})
        return 204


@list_blueprint.route('/api/lists/<user_name>/<list_name>', methods=['GET'])
def specific_list_for_specific_user(user_name, list_name):
    """
        Endpoint to get a specific list for a specific user
        ---
        tags:
          - List Methods
        parameters:
          - name: user_name
            type: string
            in: path
            required: true
            description: user you want to query
          - name: list_name
            type: string
            in: path
            required: true
            description: specific list that belong to a user
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """
    parent_span = create_parent_trace()
    with opentracing.tracer.start_span('playlist_list_get', child_of=parent_span) as span:
        data_validator.validate_json_for_user(user_name)
        data_validator.validate_json_for_list(list_name)
        service = ListsService()
        result = service.get_specific_user_list(user_name, list_name)
        return jsonify(result.__dict__), 200


@list_blueprint.errorhandler(InvalidUsage)
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