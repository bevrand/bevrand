import redis
import os
import api

app_settings = os.getenv('APP_SETTINGS')
if app_settings is None:
    app_settings = 'Test'
env = getattr(api.config, app_settings)
connection = env.CONNECTION
print(connection)


r_ = redis.Redis(host=connection, port=6379, db=0, decode_responses=True)