from flask import jsonify, request, Blueprint
from flask_restplus import inputs

from api import FLASK_TRACER
from api.service import redis_service, data_validator
from api.error_handler.error_model import InvalidUsage
import json
import opentracing


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
    parent_span = create_parent_trace()

    desc_list = request.args.get('list')
    data_validator.validate_json_for_list(desc_list)

    user_name = request.args.get('user')
    data_validator.validate_json_for_user(user_name)

    with opentracing.tracer.start_span('topfive-list', child_of=parent_span) as span:
        top_five = request.args.get('topfive', type=inputs.boolean, default=True)
        result = redis_service.get_all_rolled_drinks_from_redis(user_name, desc_list, top_five)
        span.log_kv({"status_code": 200, "result": result['body']})
        res = json.dumps(result['body'], indent=4)
        return res, 200


@redis_blueprint.errorhandler(InvalidUsage)
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