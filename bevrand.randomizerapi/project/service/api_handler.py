from project.db import redis_connection

import random


def randomize_drink_from_list(beverage_list, user_list):
        return_object = random_selection(beverage_list, user_list)
        return return_object


def random_selection(rand_list, redis_col):
    randomized_drink = random.choice(rand_list)
    redis_response = redis_connection.redis_controller(redis_col, randomized_drink)
    if not redis_response.valid:
        error_object = {'status_code': redis_response.status_code, 'body': redis_response.message}
        return error_object
    return_object = {'status_code': 200, 'body': randomized_drink}
    return return_object


def get_all_rolled_drinks_from_redis(user, desc_list, topfive_bool):
    redis_coll = user + desc_list
    redis_result = redis_connection.get_top_list(redis_coll)

    if not redis_result.valid:
        error_object = {'status_code': redis_result.status_code, 'body': redis_result.message}
        return error_object

    redis_list = []
    redis_sorted_list = redis_result.sorted_list
    redis_top_list = user + ":" + desc_list
    if topfive_bool:
        redis_sorted_list = redis_sorted_list[:5]
    for res in redis_sorted_list:
        count = res["rolled"]
        drink = res["drink"]
        tempdrink = ":".join(drink.split(':')[1:2])
        jsonvalue = {'drink': tempdrink, 'rolled': count}
        redis_list.append(jsonvalue)
    body = {redis_top_list: redis_list}
    return_object = {'status_code': 200, 'body': body}
    return return_object