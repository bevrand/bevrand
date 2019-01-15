from flask import jsonify, request, Blueprint
from api.service import data_validator
from api.service.randomizer import Randomizer
from api.error_handler.error_model import InvalidUsage
from api.jaeger import tracing
from opentracing.ext import tags
from opentracing.propagation import Format


randomize_blueprint = Blueprint('randomize', __name__,)
tracer = tracing.init_tracer("RandomizerApi")


@randomize_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@randomize_blueprint.route('randomize', methods=['POST'])
@randomize_blueprint.route('v1/randomize', methods=['POST'])
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
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    if span_ctx is None:
        span_ctx = tracer.start_active_span(request)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    json_body = request.json
    try:
        beverages = json_body['beverages']
        user_name = json_body['user']
        playlist = json_body['list']
    except KeyError:
        raise InvalidUsage('Required fields are missing', status_code=400, meta="user, playlist or beverages")
    data_validator.validate_beverages(beverages)
    data_validator.validate_user_name(user_name)
    data_validator.validate_play_list(playlist)
    with tracer.start_active_span('randomized-drink', child_of=span_ctx, tags=span_tags) as scope:
        randomizer = Randomizer()
        randomized_drink = randomizer.randomize_drink_from_list(beverages, user_name, playlist, tracer)
        scope.span.log_kv({"status_code": 200, "result": randomized_drink})
        return jsonify({"result": randomized_drink}), 200


@randomize_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    if span_ctx is None:
        return response
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_active_span('ERROR', child_of=span_ctx, tags=span_tags) as scope:
        scope.span.log_kv({"status_code": error.status_code, "error": error.message})
        if error.meta is not None:
            scope.span.log_kv({"meta": error.meta})
    return response
