from api.db import redis_connection
import random


def randomize_drink_from_list(beverage_list, user_list):
    return random_selection(beverage_list, user_list)


def random_selection(rand_list, redis_col):
    randomized_drink = random.choice(rand_list)
    redis_connection.count_rolled_drinks(redis_col, randomized_drink)
    return randomized_drink



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