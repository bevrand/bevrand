from api.db.redis_connection import RedisConnection
import random


def randomize_drink_from_list(beverage_list, user_list):
    return random_selection(beverage_list, user_list)


def random_selection(rand_list, redis_col):
    randomized_drink = random.choice(rand_list)
    Redis = RedisConnection()
    Redis.count_rolled_drinks(redis_col, randomized_drink)
    return randomized_drink


def get_all_rolled_drinks_from_redis(user, desc_list, topfive_bool):
    redis_coll = user + desc_list
    Redis = RedisConnection()
    redis_result = Redis.get_top_list(redis_coll)
    redis_sorted_list = redis_result.sorted_list
    redis_top_list = user + ":" + desc_list
    if topfive_bool:
        redis_sorted_list = redis_sorted_list[:5]
    redis_list = sort_list(redis_sorted_list)
    return_object = {'body': {redis_top_list: redis_list}}
    return return_object


def sort_list(list_to_sort):
    sorted_list = []
    for res in list_to_sort:
        count = res["rolled"]
        drink = res["drink"]
        tempdrink = ":".join(drink.split(':')[1:2])
        jsonvalue = {'drink': tempdrink, 'rolled': count}
        sorted_list.append(jsonvalue)
    return sorted_list