from flask import Blueprint, jsonify, request
from api.services import logic_for_users_controller_get, \
    logic_for_users_controller_put, logic_for_frontpage_controller_get, \
    logic_for_users_controller_delete, logic_for_users_controller_post
from api.services import data_validator
import json
from api import FLASK_TRACER
from api.error_handler.error_model import InvalidUsage
import opentracing

users_blueprint = Blueprint('users', __name__,)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/api/frontpage', methods=['GET'])
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
        return_object = logic_for_frontpage_controller_get.worker_for_frontpage_get(list_name)
        if return_object['status_code'] is 200:
            res = json.dumps(return_object['body'], indent=4)
            span.log_kv({"status_code": 200, "result": return_object['body']})
            return res, 200
        else:
            res = json.dumps(return_object['body'].__dict__, indent=4)
            return res, return_object['status_code']


@users_blueprint.route('/api/users', methods=['GET'])
def list_of_all_users():
    """
        Endpoint to get all users
        ---
        tags:
          - Users Methods
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """

    return_object = logic_for_users_controller_get.worker_for_all_users()
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, return_object['status_code']
    return 200


@users_blueprint.route('/api/list', methods=['GET'])
def specific_list_for_specific_user():
    """
        Endpoint to get a specific list for a specific user
        ---
        tags:
          - List Methods
        parameters:
          - name: user
            type: string
            in: query
            required: true
            description: user you want to query
          - name: list
            type: string
            in: query
            required: true
            description: specific list that belong to a user
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """
    user_name = request.args.get('user', default=None)
    if user_name is not None:
        data_validator.validate_json_for_user(user_name)
    user_list = request.args.get('list', default=None)
    if user_list is not None:
        data_validator.validate_json_for_list(user_list)
    return_object = logic_for_users_controller_get.worker_for_users_get(user_name, user_list)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, return_object['status_code']


@users_blueprint.route('/api/user', methods=['GET'])
def lists_for_specific_user():
    """
        Endpoint to get all lists for a user
        ---
        tags:
          - User Methods
        parameters:
          - name: user
            type: string
            in: query
            required: true
            description: user you want to query
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list is correct see response
    """
    user_name = request.args.get('user', default=None)
    if user_name is not None:
        data_validator.validate_json_for_user(user_name)
    return_object = logic_for_users_controller_get.worker_for_all_lists_of_a_specific_user(user_name)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, return_object['status_code']


@users_blueprint.route('/api/user', methods=['POST'])
def post_user():
    """
        Endpoint to insert new lists into Mongo
        ---
        tags:
          - User Methods
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
          400:
            description: Incorrect dbs used
          200:
            description: Your list has been inserted
    """
    json_body = request.json
    data_validator.validate_json_for_post(json_body)
    return_object = logic_for_users_controller_post.worker_for_post(json_body)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, return_object['status_code']


@users_blueprint.route('/api/user', methods=['DELETE'])
def remove_user_list():
    """
        Endpoint to remove a specific list or a complete user
        ---
        tags:
          - User Methods
        parameters:
          - name: user
            type: string
            in: query
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

    to_remove_user = request.args.get('user')
    if to_remove_user is not None:
        validation = data_validator.validate_json_for_user(to_remove_user)

    to_remove_list = request.args.get('list', default=None)
    if to_remove_list is not None:
        data_validator.validate_json_for_list(to_remove_list)

    return_object = logic_for_users_controller_delete.worker_for_delete(to_remove_user, to_remove_list)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, return_object['status_code']



@users_blueprint.route('/api/user', methods=['PUT'])
def update_user_list():
    """
         Endpoint to update a user or a list
        ---
        tags:
          - User Methods
        parameters:
          - name: user
            type: string
            in: query
            required: true
            description: user you want to update
          - name: list
            type: string
            in: query
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
    old_user = request.args.get('user')
    old_list = request.args.get('list')

    json_body = request.json
    data_validator.validate_json_for_post(json_body)

    if old_user is not None:
        data_validator.validate_json_for_user(old_user)

    if old_list is not None:
        data_validator.validate_json_for_list(old_list)

    return_object = logic_for_users_controller_put.worker_for_update(old_user, old_list, json_body)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'].__dict__, indent=4)
        return res, return_object['status_code']


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

