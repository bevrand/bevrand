from project.service import redis_connection, error_handler

import random


def random_list_creator(responsejson, user_list):
    try:
        response_list = responsejson['beverages']
        random_drink = random_selection(response_list, user_list)
        return random_drink
    except:
        error_handler.InvalidUsage('Invalid Json - url not correct', status_code=410)


def random_list_creator_from_post(beveragelist, user_list):
    try:
        random_drink = random_selection(beveragelist, user_list)
        return random_drink
    except:
        error_handler.InvalidUsage('Invalid Json - url not correct', status_code=410)


def random_selection(rand_list, redis_col):
    listed_drink = random.choice(rand_list)
    redis_connection.rediscontroller(redis_col, listed_drink)
    return listed_drink
