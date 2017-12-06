from project.service import error_handler, r_

from operator import itemgetter
from flask import jsonify


def rediscontroller(redis_col, drink_to_incr):
    col = redis_col
    drink = drink_to_incr
    key = col + ":" + drink
    temp = r_.get(key)
    if temp is None:
        r_.set(key, 0)
    try:
        r_.incr(key)
    except:
        raise error_handler.InvalidUsage('An error has occured when incrementing drinks', status_code=410)
    return


def get_top_list(redis_col):
    pattern = redis_col + "*"
    output = r_.keys(pattern)
    drinks = []
    for out in output:
        try:
            count = r_.get(out)
            jsonvalue = {'drink': out, 'rolled': int(count)}
            drinks.append(jsonvalue)
        except:
            raise error_handler.InvalidUsage('Invalid input', status_code=410)
    sorted_list = sorted(drinks, key=itemgetter('rolled'), reverse=True)
    return sorted_list


def get_five_from_list(user, desc_list, topfive_bool):
    redis_coll = user + desc_list
    redis_result = get_top_list(redis_coll)
    redis_list = []
    redis_top_list = user + ":" + desc_list
    if topfive_bool:
        redis_result = redis_result[:5]
    for res in redis_result:
        count = res["rolled"]
        drink = res["drink"]
        tempdrink = ":".join(drink.split(':')[1:2])
        jsonvalue = {'drink': tempdrink, 'rolled': count}
        redis_list.append(jsonvalue)
    return jsonify({redis_top_list: redis_list})


def clean_up_redis(redis_col):
    pattern = redis_col + "*"
    keys = r_.keys(pattern)
    for key in keys:
        r_.delete(key)
    return
