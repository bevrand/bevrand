import redis
import os
import project

app_settings = os.getenv('APP_SETTINGS')
env = getattr(project.config, app_settings)
connection = env.CONNECTION
print(connection)

r_ = redis.Redis(host=connection, port=6379, db=0, decode_responses=True)
