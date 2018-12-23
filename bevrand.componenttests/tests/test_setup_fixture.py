import unittest
import requests


class TestFixture(unittest.TestCase):
    """Test fixture used on all apis"""

    reserved_keywords = ['global', 'frontpage', 'bevrand', 'bevragerandomizer']
    headers = {'Content-type': 'application/json'}
    reserved_user_error = "is a reserved username and cannot be used for creation or deletion"
    attribute_validation_error = "Errors occured when validating"
    validation_missing_fields = "Required fields are missing"
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
        response = requests.post(url, body, headers=self.headers)
        return response

    def put_without_auth_header(self, url, body):
        response = requests.put(url, body, headers=self.headers)
        return response

    @staticmethod
    def delete_without_auth_header(url):
        response = requests.delete(url)
        return response

    @staticmethod
    def validate_string_contains(base_string, assertion_string):
        return assertion_string.lower() in base_string.lower()


