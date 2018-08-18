from pymongo import MongoClient
import api
import os


def connect_to_mongo():
    app_settings = os.getenv('APP_SETTINGS')
    env = getattr(api.config, app_settings)
    print(env.CONNECTION)
    client = MongoClient(env.CONNECTION)
    db = client.bevrand
    return db