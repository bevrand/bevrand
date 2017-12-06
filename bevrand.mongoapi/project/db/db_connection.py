from pymongo import MongoClient
import os


#app_settings = os.getenv('APP_SETTINGS')
#CONNECTION = 'mongodb://0.0.0.0:27017'


def connect_to_mongo():
    connection = os.getenv('CONNECTION')
    print(connection)
    client = MongoClient(connection)
    db = client.bevrand
    return db