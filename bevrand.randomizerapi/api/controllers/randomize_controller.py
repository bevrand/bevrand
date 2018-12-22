from flask import jsonify, request, Blueprint
from api import FLASK_TRACER
from api.service import data_validator
from api.service.randomizer import Randomizer
from api.error_handler.error_model import InvalidUsage
import opentracing


randomize_blueprint = Blueprint('randomize', __name__,)


@randomize_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@randomize_blueprint.route('', methods=['POST'])
def randomize_list_of_drinks():
    """
        This is an api to randomize lists and add data to redis
        ---
        tags:
          - Randomizer
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
    parent_span = create_parent_trace()
    json_body = request.json
    data_validator.validate_json_for_randomize(json_body)
    beverages = request.json['beverages']
    user_name = json_body['user']
    playlist = json_body['list']
    with opentracing.tracer.start_span('randomized-drink', child_of=parent_span) as span:
        randomizer = Randomizer()
        randomized_drink = randomizer.randomize_drink_from_list(beverages, user_name, playlist)
        span.log_kv({"status_code": 200, "result": randomized_drink})
        return jsonify({"result": randomized_drink}), 200


@randomize_blueprint.errorhandler(InvalidUsage)
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
