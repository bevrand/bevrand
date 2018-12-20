import unittest
import os
import requests
import environment


class TestFixture(unittest.TestCase):
    """Test fixture used on all apis"""

    def get_without_auth_header(self, url):
        response = requests.get(url)
        return response

    @staticmethod
    def post_without_auth_header(url, body):
        response = requests.post(url, body)
        return response

    @staticmethod
    def put_without_auth_header(url, body):
        response = requests.put(url, body)
        return response

    @staticmethod
    def delete_without_auth_header(url):
        response = requests.delete(url)
        return response
