from flask import Blueprint, jsonify, request
from project.api.models import ReturnModel
import json

from project.db import db_frontpage_filler, db_worker


users_blueprint = Blueprint('users', __name__,)


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/api/frontpage/', methods=['GET'])
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
            description: Your stuff has been moved bro
    """
    listname = request.args.get('list', default=None)
    if listname is None:
        front_page_list = db_frontpage_filler.get_all_frontpage_lists()
        return front_page_list
    else:
        front_page_beverages = db_frontpage_filler.get_frontpage_beverages(listname)
        return front_page_beverages
    #jsonify in the view, return a list from the repo


@users_blueprint.route('/api/users/', methods=['GET'])
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
            description: Your stuff has been moved bro
    """
    username = request.args.get('user', default=None)
    descriptionlist = request.args.get('list', default=None)
    if username is None and descriptionlist is None:
        all_users = db_worker.get_all_users()
        return all_users
    elif username is not None and descriptionlist is None:
        description_lists = db_worker.get_all_descriptions(username)
        return description_lists
    elif username is not None and descriptionlist is not None:
        beverage_list = db_worker.get_specific_drinklist(username, descriptionlist)
        return beverage_list
    else:
        return "not a correct call", 400


@users_blueprint.route('/api/users/', methods=['POST'])
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
                beverages:
                  type: array
                  items:
                    schema:
                        type: string
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your stuff has been moved bro
    """

    user = request.json['user']
    list = request.json['list']
    list_exists = db_worker.check_if_userlist_already_exists(user, list)
    if not list_exists:
        data_to_insert = request.json
        insert_list_res = db_worker.insert_new_list(data_to_insert, user, list)
        temp_object = ReturnModel(user, list, insert_list_res, data_to_insert)
        response = json.dumps(temp_object.__dict__)
        return response, 200
    else:
        return "List already exists unable to insert", 400


@users_blueprint.route('/api/users/', methods=['DELETE'])
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
            description: Your stuff has been moved bro
    """

    to_remove_user = request.args.get('user')
    to_remove_list = request.args.get('list')
    user_exists = db_worker.check_if_user_exists(to_remove_user)
    if user_exists:
        list_exists = db_worker.check_if_userlist_already_exists(to_remove_user, to_remove_list)
        if list_exists:
            deleted_list = db_worker.delete_specific_list(to_remove_user, to_remove_list)
            temp_object = ReturnModel(to_remove_user, to_remove_list, deleted_list, "No more data")
            response = json.dumps(temp_object.__dict__)
            return response, 200
        else:
            return "Unable to delete list, list does not exist", 400
    else:
        return "Unable to delete user, user does not exist", 400


@users_blueprint.route('/api/users/', methods=['PUT'])
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
              id: Product
              required:
                - name
              properties:
                name:
                  type: string
                  description: The product's name.
                  default: "Guarana"
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your stuff has been moved bro
    """

    old_user = request.args.get('user')
    old_list = request.args.get('list')
    user_exists = db_worker.check_if_user_exists(old_user)
    if user_exists:
        list_exists = db_worker.check_if_userlist_already_exists(old_user, old_list)
        if list_exists:
            list_to_update = request.json
            updated_list = db_worker.update_specific_list(list_to_update, old_user, old_list)
            temp_object = ReturnModel(old_user, old_list, updated_list, list_to_update)
            response = json.dumps(temp_object.__dict__)
            return response, 200
        else:
            return "Could not update list, list does not exist", 400
    else:
        return "Could not update user, user does not exist", 400
