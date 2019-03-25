import unittest
import requests
import os
from helpers.random_name_generator import HelperClass
from environment import config


class TestFixture(unittest.TestCase):
    """Test fixture used for all apis"""

    env = os.environ.get('PYTHON_ENV')
    if env == 'Test':
        env_setting = config.Test()
    else:  # If local or other
        env_setting = config.Local()

    authentication_url = env_setting.authentication_url
    highscore_url = env_setting.highscore_url
    playlist_url = env_setting.playlist_url
    proxy_url = env_setting.proxy_url
    proxy_endpoints = env_setting.proxy_endpoints
    randomizer_url = env_setting.randomize_url
    recommendation_url = env_setting.recommendation_url

    reserved_keywords = ['global', 'frontpage', 'bevrand', 'bevragerandomizer']
    headers = {'Content-type': 'application/json'}
    put_headers = {'Content-Type': 'application/json-patch+json'}
    reserved_user_error = "is a reserved username and cannot be used for creation or deletion"
    attribute_validation_error = "Errors occured when validating"
    unknown_id = HelperClass.random_int_generator(40)
    validation_missing_fields = "Required fields are missing"
    data_seeded_user = 'marvin'

    test_playlist_body = {
                          "beverages": [
                            "beer",
                            "wine"
                          ],
                          "displayName": "I am so depressed",
                          "imageUrl": "http://whatever.com"
                        }
    test_randomize_body = {
                              "beverages": [
                                "beer",
                                "wine",
                                "whiskey"
                              ],
                              "list": "tgif",
                              "user": "frontpage"
                            }

    @staticmethod
    def get_without_auth_header(url):
        response = requests.get(url)
        return response

    def post_without_auth_header(self, url, body):
        response = requests.post(url=url, json=body, headers=self.headers)
        return response

    def put_without_auth_header(self, url, body):
        response = requests.put(url=url, json=body, headers=self.put_headers)
        return response

    @staticmethod
    def delete_without_auth_header(url):
        response = requests.delete(url=url)
        return response

    @staticmethod
    def validate_string_contains(base_string, assertion_string):
        return assertion_string.lower() in base_string.lower()
