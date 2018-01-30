from flask import Blueprint, jsonify, request
from project.api.models import ReturnModel, ReturnModelPost, ReturnModelPut
import json

from project.db import db_frontpage, db_users


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
        This is an api to see lists and beverages
        ---
        tags:
          - Api to show lists&beverages
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
    list_name = request.args.get('list', default=None)
    if list_name is None:
        front_page_list = db_frontpage.get_all_frontpage_lists()
        return front_page_list, 200
    else:
        list_is_correct = db_frontpage.check_if_frontpage_list_exists(list_name)
        if list_is_correct:
            front_page_mongo = db_frontpage.get_frontpage_beverages(list_name)
            front_page_model = json.dumps(front_page_mongo.__dict__, indent=4)
            return front_page_model, 200
        else:
            error = ReturnModel('frontpage', list_name, 'The frontpagelist you queried does not exist')
            error_message = json.dumps(error.__dict__, indent=4)
            return error_message, 404


@users_blueprint.route('/api/users', methods=['GET'])
def users():
    """
        This is an api to see lists and beverages
        ---
        tags:
          - Api to show lists&beverages
        parameters:
          - name: user
            type: string
            in: query
            required: false
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
            description: Your list is correct see response
    """

    user_name = request.args.get('user', default=None)
    user_list = request.args.get('list', default=None)

    # These methods check if the data is correct, if not they will return a not found
    if user_name is not None:
        user_exists = db_users.check_if_user_exists(user_name)
        if not user_exists:
            error = ReturnModel(user_name, user_list, 'The user you queried does not exist')
            error_message = json.dumps(error.__dict__, indent=4)
            return error_message, 404
    if user_list is not None:
        list_exists = db_users.check_if_userlist_exists(user_name, user_list)
        if not list_exists:
            error = ReturnModel(user_name, user_list, 'The user you queried does not exist')
            error_message = json.dumps(error.__dict__, indent=4)
            return error_message, 404

    if user_name is None and user_list is None:
        all_users = db_users.get_all_users()
        return jsonify({'users': all_users}), 200
    elif user_name is not None and user_list is None:
        description_lists = db_users.get_all_descriptions(user_name)
        return jsonify({'descriptions': description_lists}), 200
    elif user_name is not None and user_list is not None:
        beverage_list = db_users.get_specific_drinklist(user_name, user_list)
        return jsonify({'beverages': beverage_list}), 200
    else:
        error = ReturnModel(user_name, user_list, 'Not a correct call')
        error_message = json.dumps(error.__dict__, indent=4)
        return error_message, 400


@users_blueprint.route('/api/users', methods=['POST'])
def post_user():
    """
        This is an api to see lists and beverages
        ---
        tags:
          - Api to show lists&beverages
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: user
              required:
                - user
                - list
                - beverages
              properties:
                user:
                    type: string
                    description: The user to insert
                list:
                  type: string
                  description: The list to insert
                imageUrl:
                  type: string
                  description: The image to upload
                beverages:
                  type: array
                  items:
                    schema:
                        type: string
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list has been inserted
    """
    user_name = request.json['user'].lower()
    list_name = request.json['list'].lower()
    if user_name is 'frontpage':
        front_page_object = ReturnModel(user_name, list_name, 'frontpage is an invalid user - reserved')
        res = json.dumps(front_page_object.__dict__, indent=4)
        return res, 403
    list_exists = db_users.check_if_userlist_exists(user_name, list_name)
    if not list_exists:
        data_to_insert = request.json
        insert_list_res = db_users.insert_new_list(data_to_insert, user_name, list_name)
        temp_object = ReturnModelPost(user_name, list_name, insert_list_res, data_to_insert)
        response = json.dumps(temp_object.__dict__, indent=4)
        return response, 200
    else:
        return_object = ReturnModel(user_name, list_name, 'Unable to insert list already exists')
        res = json.dumps(return_object.__dict__, indent=4)
        return res, 400


@users_blueprint.route('/api/users', methods=['DELETE'])
def remove_user_list():
    """
        Call to remove a list from a user
        ---
        tags:
          - Api to show lists&beverages
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
            description: Your list was deleted
    """

    to_remove_user = request.args.get('user').lower()
    to_remove_list = request.args.get('list').lower()
    user_exists = db_users.check_if_user_exists(to_remove_user)
    if user_exists:
        list_exists = db_users.check_if_userlist_exists(to_remove_user, to_remove_list)
        if list_exists:
            deleted_list = db_users.delete_specific_list(to_remove_user, to_remove_list)
            temp_object = ReturnModel(to_remove_user, to_remove_list, deleted_list)
            response = json.dumps(temp_object.__dict__, indent=4)
            return response, 200
        else:
            return_object = ReturnModel(to_remove_user, to_remove_list,
                                             'Unable to delete list list does not exist')
            res = json.dumps(return_object.__dict__, indent=4)
            return res, 400
    else:
        return_object = ReturnModel(to_remove_user, to_remove_list,
                                         'Unable to delete user, user does not exist')
        res = json.dumps(return_object.__dict__, indent=4)
        return res, 400


@users_blueprint.route('/api/users', methods=['PUT'])
def update_user_list():
    """
         Call to update a list from a user
        ---
        tags:
          - Api to show lists&beverages
        parameters:
          - name: user
            type: string
            in: query
            required: true
            description: user where the list belongs to
          - name: list
            type: string
            in: query
            required: true
            description: specific list that belong to a user
          - name: body
            in: body
            required: true
            schema:
              id: user
              required:
                - user
                - list
                - beverages
              properties:
                user:
                    type: string
                    description: The user to insert
                list:
                  type: string
                  description: The list to insert
                imageUrl:
                  type: string
                  description: The image to upload
                beverages:
                  type: array
                  items:
                    schema:
                        type: string
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your list was deleted
    """

    old_user = request.args.get('user').lower()
    old_list = request.args.get('list').lower()

    # check to see if user exists if it does user is updated
    user_exists = db_users.check_if_user_exists(old_user)
    if user_exists:
        list_exists = db_users.check_if_userlist_exists(old_user, old_list)
        if list_exists:
            list_to_update = request.json
            updated_list = db_users.update_specific_list(list_to_update, old_user, old_list)
            temp_object = ReturnModelPut(old_user, old_list, updated_list, list_to_update)
            response = json.dumps(temp_object.__dict__, indent=4)
            return response, 200
        else:
            return_object = ReturnModel(old_user, old_list,
                                        'Unable to update list, list does not exist')
            res = json.dumps(return_object.__dict__, indent=4)
            return res, 400

    # if user does not exist no update is made
    else:
        return_object = ReturnModel(old_user, old_list,
                                    'Unable to update user, user does not exist')
        res = json.dumps(return_object.__dict__, indent=4)
        return res, 400
