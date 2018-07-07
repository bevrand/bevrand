from flask import jsonify, request, Blueprint
from flask_restplus import inputs

from api import FLASK_TRACER
from api.service import redis_service, data_validator
from api.error_handler.error_model import InvalidUsage
import json


redis_blueprint = Blueprint('redis', __name__,)


@redis_blueprint.route('', methods=['GET'])
#@FLASK_TRACER.trace()
def redis_top_five():
    """
        This is an api to show top rolled drinks from redis
        ---
        tags:
          - Redis
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

    return_object = redis_service.get_all_rolled_drinks_from_redis(user_name, desc_list, top_five)
    if return_object['status_code'] is 200:
        res = json.dumps(return_object['body'], indent=4)
        return res, 200
    else:
        res = json.dumps(return_object['body'], indent=4)
        return res, return_object['status_code']


@redis_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response