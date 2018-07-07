from ..db.data_models import ErrorModel, SuccessModel, SuccessModelRedis
from ..db import r_
import redis
from operator import itemgetter
from api.error_handler.error_model import InvalidUsage


def count_rolled_drinks(redis_col, drink_to_incr):
    try:
        col = redis_col
        drink = drink_to_incr
        key = col + ":" + drink
        temp = r_.get(key)
        if temp is None:
            r_.set(key, 0)
        r_.incr(key)
        return
    except redis.exceptions.ConnectionError:
        raise InvalidUsage('An error has occurred with the Redis connection', status_code=503)
    except redis.exceptions.RedisError:
        raise InvalidUsage('An error has occurred when incrementing drinks', status_code=503)


def get_top_list(redis_col):
    try:
        pattern = redis_col + "*"
        output = r_.keys(pattern)
        drinks = []
        for out in output:
            count = r_.get(out)
            jsonvalue = {'drink': out, 'rolled': int(count)}
            drinks.append(jsonvalue)
        sorted_list = sorted(drinks, key=itemgetter('rolled'), reverse=True)
        success_model = SuccessModelRedis(True, sorted_list)
        return success_model
    except redis.exceptions.ConnectionError:
        raise InvalidUsage('An error has occurred with the Redis connection', status_code=503)
    except redis.exceptions.RedisError:
        raise InvalidUsage('An error has occurred when incrementing drinks', status_code=503)


def clean_up_redis(redis_col):
    pattern = redis_col + "*"
    keys = r_.keys(pattern)
    for key in keys:
        r_.delete(key)
    return
