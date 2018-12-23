from tests import test_setup_fixture
from environment import config
import pytest
import os
import json

url = None

@pytest.fixture(scope="module")
def setup_config():
    env = os.environ.get('PYTHON_ENV')
    if env == 'Local':
        env_setting = config.Local()
    elif env == 'Test':
        env_setting = config.Test()
    else:
        env_setting = config.Local()
    global url
    url = env_setting.randomize_url


@pytest.mark.usefixtures("setup_config")
class RandomizerApiTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        sut = url + '/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    #this test is to check for backwards compatibility
    def test_should_be_able_to_randomize_a_simple_list_old_enpoint(self):
        sut = url + '/randomize'
        body = json.dumps(self.test_randomize_body)
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_randomize_a_simple_list(self):
        sut = url + '/v1/randomize'
        body = json.dumps(self.test_randomize_body)
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)


@pytest.mark.usefixtures("setup_config")
class RandomizerValidationChecks(test_setup_fixture.TestFixture):

    def test_should_not_be_able_to_make_empty_calls(self):
        sut = url + '/v1/randomize'
        body = json.dumps({})
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertEqual(400, response.status_code)
        self.assertTrue(self.validate_string_contains(error_message, self.validation_missing_fields))
        self.assertTrue(self.validate_string_contains(meta_message, "user"))

    def test_should_not_be_able_to_make_call_without_beverages(self):
        sut = url + '/v1/randomize'
        body = json.dumps({ "list": "tgif", "user": "frontpage"})
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertEqual(400, response.status_code)
        self.assertTrue(self.validate_string_contains(error_message, self.validation_missing_fields))
        self.assertTrue(self.validate_string_contains(meta_message, "beverages"))

    def test_should_not_be_able_to_make_call_without_user(self):
        sut = url + '/v1/randomize'
        body = json.dumps({ "beverages": [
                            "beer",
                            "wine",
                            "whiskey"
                          ],"list": "frontpage"})
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertEqual(400, response.status_code)
        self.assertTrue(self.validate_string_contains(error_message, self.validation_missing_fields))
        self.assertTrue(self.validate_string_contains(meta_message, "user"))

    def test_should_not_be_able_to_make_call_without_list(self):
        sut = url + '/v1/randomize'
        body = json.dumps({ "beverages": [
                            "beer",
                            "wine",
                            "whiskey"
                          ],"user": "frontpage"})
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertEqual(400, response.status_code)
        self.assertTrue(self.validate_string_contains(error_message, self.validation_missing_fields))
        self.assertTrue(self.validate_string_contains(meta_message, "list"))

    def test_should_be_able_to_include_extra_json_fields(self):
        sut = url + '/v1/randomize'
        body = json.dumps({
            "beverages": [
                "beer",
                "wine",
                "whiskey"
            ],
            "list": "tgif",
            "user": "frontpage",
            "anextrafield": "just an extra field"
        })
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)