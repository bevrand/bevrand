import redis
import os

connection = os.getenv('CONNECTION')
print(connection)

r_ = redis.Redis(host=connection, port=6379, db=0, decode_responses=True)