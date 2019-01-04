import unittest
import requests
from helpers.random_name_generator import HelperClass

class TestFixture(unittest.TestCase):
    """Test fixture used on all apis"""

    reserved_keywords = ['global', 'frontpage', 'bevrand', 'bevragerandomizer']
    headers = {'Content-type': 'application/json'}
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

    def get_without_auth_header(self, url):
        response = requests.get(url)
        return response

    def post_without_auth_header(self, url, body):
        response = requests.post(url=url, json=body, headers=self.headers)
        return response

    def put_without_auth_header(self, url, body):
        headers = {'Content-Type': 'application/json-patch+json'}
        response = requests.put(url=url, json=body, headers=headers)
        return response

    @staticmethod
    def delete_without_auth_header(url):
        response = requests.delete(url=url)
        return response

    @staticmethod
    def validate_string_contains(base_string, assertion_string):
        return assertion_string.lower() in base_string.lower()


