from flask import jsonify, request, Blueprint
from flask_restplus import inputs

from project.service import api_handler, data_validator
from project.db import redis_connection
import json

randomize_blueprint = Blueprint('randomize', __name__,)


@randomize_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@randomize_blueprint.route('/api/randomize', methods=['POST'])
def post_list():
    """
        This is an api to randomize lists and add data to redis
        ---
        tags:
          - Api to randomize
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                user:
                  type: string
                list:
                  type: string
                beverages:
                  type: array
                  items:
                    type: string
              example:
                user: "frontpage"
                list: "tgif"
                beverages: ["beer", "wine", "whiskey"]
        responses:
          400:
            description: Incorrect user, list or beverages
          200:
            description: Your list has been randomized
    """
    json_body = request.json
    validation = data_validator.validate_json_for_randomize(json_body)
    valid = validation['valid']
    if not valid:
        return str(validation['errors']), 400

    beverages = request.json['beverages']
    user_list = json_body['user'] + json_body['list']
    return_object = api_handler.randomize_drink_from_list(beverages, user_list)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'], indent=4)
        return res, return_object['status_code']


@randomize_blueprint.route('/api/redis', methods=['GET'])
def redis_top_five():
    """
        This is an api to Randomize drinks
        ---
        tags:
          - Show top rolled drinks
        parameters:
          - name: user
            type: string
            in: query
            required: true
            description: user you want to query
            example: frontpage
          - name: list
            type: string
            in: query
            required: true
            description: specific list that belong to a user
            example: tgif
          - name: topfive
            type: boolean
            in: query
            required: false
            description: return a top 5 or all
        responses:
          400:
            description: Incorrect dbs used
          200:
            description: Your call was made with success
    """
    desc_list = request.args.get('list')
    validation = data_validator.validate_json_for_list(desc_list)
    valid = validation['valid']
    if not valid:
        return str(validation['errors']), 400

    user_name = request.args.get('user')
    validation = data_validator.validate_json_for_user(user_name)
    valid = validation['valid']
    if not valid:
        return str(validation['errors']), 400

    top_five = request.args.get('topfive', type=inputs.boolean, default=True)

    return_object = api_handler.get_all_rolled_drinks_from_redis(user_name, desc_list, top_five)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'], indent=4)
        return res, return_object['status_code']


'''
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

'''