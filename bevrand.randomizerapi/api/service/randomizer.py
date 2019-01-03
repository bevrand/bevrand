import random
import requests
import os
import json
from api.error_handler.error_model import InvalidUsage
from opentracing.ext import tags
from opentracing.propagation import Format


class Randomizer(object):

    url = None

    def __init__(self):
        self.url = os.environ['HIGHSCORE_API']

    def randomize_drink_from_list(self, beverage_list, user_list, playlist, tracer):
        randomized_drink = random.choice(beverage_list)
        self.post_drink_to_highscore(randomized_drink, user_list, playlist, tracer)
        return randomized_drink

    def post_drink_to_highscore(self, drink, user, playlist, tracer):
        body = {'drink': drink}
        json_body = json.dumps(body)
        url = self.url + f'highscores/{user}/{playlist}'

        span = tracer.active_span
        span.set_tag(tags.HTTP_METHOD, 'GET')
        span.set_tag(tags.HTTP_URL, url)
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        headers = {}
        tracer.inject(span, Format.HTTP_HEADERS, headers)

        r = requests.post(url, json_body, headers=headers)
        if r.status_code != 201:
            raise InvalidUsage('Error occured while posting to the highscoreapi', status_code=503)
        return

    def queue_drink_to_highscore(self):
        return
