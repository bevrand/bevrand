from flask import jsonify, request, Blueprint
from flask_restplus import inputs
from project.api import REQURL

import requests

from project.service import api_handler
from project.service import redis_connection


randomize_blueprint = Blueprint('randomize', __name__,)


@randomize_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@randomize_blueprint.route('/api/randomize', methods=['GET'])
def randomize():
    """
        This is an api to randomize lists and add data to redis
        ---
        tags:
          - Api to randomize
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
            description: Your call was made with success
    """
    username = request.args.get('user')
    description_list = request.args.get('list')
    if username is None and description_list is None:
        url = REQURL + 'api/frontpage?list=TGIF'
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            user_list = "frontpageTgif"
            random_drink = api_handler.random_list_creator(json_response, user_list)
            return str(random_drink)
        else:
            return "Bad request, no valid status returned"
    if username == 'frontpage':
        url = REQURL + 'api/frontpage?list=' + description_list
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            user_list = "frontpage" + description_list
            random_drink = api_handler.random_list_creator(json_response, user_list)
            return str(random_drink)
        else:
            return "Bad request, no valid status returned"
    else:
        url = REQURL + 'api/users?user=' + username + '&list=' + description_list
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            user_list = username + description_list
            random_drink = api_handler.random_list_creator(json_response, user_list)
            return random_drink
        else:
            return "Bad request, no valid status returned"


@randomize_blueprint.route('/api/redisuser', methods=['GET'])
def show_top_rolled_beverages():
    """
        This is an api to randomize lists and add data to redis
        ---
        tags:
          - Api to randomize
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
          - name: topfive
            type: boolean
            in: query
            required: true
            description: return a top 5 or all
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your call was made with success
    """
    user = request.args.get('user', default=None)
    desc_list = request.args.get('list', default=None)
    topfive = request.args.get('topfive', type=inputs.boolean)
    if user is None:
        return "please supply a user", 400
    if desc_list is None:
        return "please supply a user", 400
    if topfive is None:
        return "please supply the bool topfive", 400
    redis_top_five = redis_connection.get_five_from_list(user, desc_list, topfive)
    return redis_top_five


@randomize_blueprint.route('/api/redis', methods=['POST'])
def clean_current_session():
    command = request.json['command']
    if command == 'clean':
        result = redis_connection.clean_up_redis()
        if result:
            return 'Redis now empty'
        else:
            return 'Could not clean, error in command'
    else:
        return 'No command given please use : { "command" : "clean" } '

