import random
import requests
import os
import json
from api.error_handler.error_model import InvalidUsage


class Randomizer(object):

    url = None

    def __init__(self):
        self.url = os.environ['HIGHSCORE_API']

    def randomize_drink_from_list(self, beverage_list, user_list, playlist):
        randomized_drink = random.choice(beverage_list)
        self.post_drink_to_highscore(randomized_drink, user_list, playlist)
        return randomized_drink

    def post_drink_to_highscore(self, drink, user, playlist):
        body = {'drink': drink}
        json_body = json.dumps(body)
        url = self.url + f'highscore/{user}/{playlist}'
        print(url)
        r = requests.post(url, json_body)
        if r.status_code != 201:
            raise InvalidUsage('Error occured while posting to the highscoreapi', status_code=503)
        return

    def queue_drink_to_highscore(self):
        return