from pymongo import MongoClient
import project
import os


def connect_to_mongo():
    app_settings = os.getenv('APP_SETTINGS')
    env = getattr(project.config, app_settings)
    client = MongoClient(env.CONNECTION)
    db = client.bevrand
    return db