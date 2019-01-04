from tests import test_setup_fixture
from environment import config
from helpers.random_name_generator import HelperClass
from helpers.models import AuthenticationModel
import pytest
import os
import requests

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
    url = env_setting.authentication_url


@pytest.mark.usefixtures("setup_config")
@pytest.mark.order1
class AuthenticationPostApiTests(test_setup_fixture.TestFixture):

    def test_should_be_able_to_create_a_new_user(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName" : user, "emailAddress": email, "passWord": password }
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    def test_should_not_be_able_to_post_an_empty_body(self):
        sut = url + '/Users'
        body = {}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['ErrorId']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)

    def test_should_not_be_able_to_create_a_new_user_with_missing_username(self):
        sut = url + '/Users'
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"emailAddress": email, "passWord": password }
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['ErrorId']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "You have to provide a user"))

    def test_should_not_be_able_to_create_a_new_user_with_missing_email(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName" : user, "passWord": password }
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['ErrorId']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "You have to provide an email"))

    def test_should_not_be_able_to_create_a_new_user_with_missing_password(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        body = {"userName" : user, "emailAddress": email}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['ErrorId']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "You have to provide a valid password"))

    def test_should_not_be_able_to_create_a_new_user_with_faulty_email(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.random_word_letters_only(10)
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName" : user, "emailAddress": email, "passWord": password }
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['Error']
        meta_message = response.json()['ErrorId']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "was not a valid mailaddress"))

    def test_should_not_be_able_to_post_a_user_twice(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName" : user, "emailAddress": email, "passWord": password }
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        resp = self.post_without_auth_header(sut, body)
        self.assertEqual(400, resp.status_code)


@pytest.mark.usefixtures("setup_config", "post_a_new_user")
@pytest.mark.order2
class AuthenticationGetApiTests(test_setup_fixture.TestFixture):

    scoped_user = None

    @pytest.fixture
    def post_a_new_user(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        self.scoped_user = AuthenticationModel.from_dict(response)
        self.scoped_user.password = password

    def test_should_be_able_to_retrieve_a_list_of_users(self):
        sut = f'{url}/Users'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.json()) >= 1)

    def test_should_be_able_to_retrieve_a_posted_user_by_id(self):
        sut = f'{url}/Users/{self.scoped_user.id}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_retrieve_a_posted_user_by_username(self):
        sut = f'{url}/Users/by-username/{self.scoped_user.username}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_retrieve_a_posted_user_by_email(self):
        sut = f'{url}/Users/by-email/{self.scoped_user.email_address}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_should_not_be_able_to_retrieve_a_non_existent_user_by_id(self):
        local_id = self.unknown_id
        sut = f'{url}/Users/{local_id}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(404, response.status_code)

    def test_should_not_be_able_to_retrieve_a_non_existent_user_by_user(self):
        username = HelperClass.random_word_letters_only(20)
        sut = f'{url}/Users/by-username/{username}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(404, response.status_code)

    def test_should_not_be_able_to_retrieve_a_non_existent_user_by_email(self):
        email = HelperClass.create_random_email()
        sut = f'{url}/Users/by-email/{email}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(404, response.status_code)

@pytest.mark.usefixtures("setup_config", "post_a_new_user")
@pytest.mark.order3
class AuthenticationPutApiTests(test_setup_fixture.TestFixture):

    scoped_user = None

    @pytest.fixture
    def post_a_new_user(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        self.scoped_user = AuthenticationModel.from_dict(response)
        self.scoped_user.password = password

    def test_should_be_able_to_update_a_username(self):
        get_url = f'{url}/Users/{self.scoped_user.id}'
        user_name_before = self.get_without_auth_header(get_url).json()['username']
        body = {
              "username": HelperClass.random_word_letters_only(20),
              }
        sut = f'{url}/Users?id={self.scoped_user.id}'
        resp = self.put_without_auth_header(sut, body)
        self.assertEqual(204, resp.status_code)
        user_name_after = self.get_without_auth_header(get_url).json()['username']
        self.assertNotEqual(user_name_before, user_name_after)

    def test_should_be_able_to_update_an_email(self):
        get_url = f'{url}/Users/{self.scoped_user.id}'
        user_name_before = self.get_without_auth_header(get_url).json()['emailAddress']
        body = {
              "emailAddress": HelperClass.create_random_email(),
              }
        sut = f'{url}/Users?id={self.scoped_user.id}'
        resp = self.put_without_auth_header(sut, body)
        self.assertEqual(204, resp.status_code)
        user_name_after = self.get_without_auth_header(get_url).json()['emailAddress']
        self.assertNotEqual(user_name_before, user_name_after)

    def test__should_not_be_able_to_update_an_email_to_an_invalid_mail(self):
        get_url = f'{url}/Users/{self.scoped_user.id}'
        user_name_before = self.get_without_auth_header(get_url).json()['emailAddress']
        body = {
              "emailAddress": HelperClass.random_word_letters_only(15),
              }
        sut = f'{url}/Users?id={self.scoped_user.id}'
        resp = self.put_without_auth_header(sut, body)
        error_message = resp.json()['Error']
        meta_message = resp.json()['ErrorId']
        self.assertEqual(400, resp.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "was not a valid mailaddress"))
        user_name_after = self.get_without_auth_header(get_url).json()['emailAddress']
        self.assertEqual(user_name_before, user_name_after)

    def test_should_be_able_to_update_deactvice_a_user(self):
        get_url = f'{url}/Users/{self.scoped_user.id}'
        body = {
              "active": False,
              }
        sut = f'{url}/Users?id={self.scoped_user.id}'
        resp = self.put_without_auth_header(sut, body)
        self.assertEqual(204, resp.status_code)
        user_name_after = self.get_without_auth_header(get_url).json()['active']
        self.assertFalse(user_name_after)

    def test_should_be_able_to_update_all_fields_at_once(self):
        get_url = f'{url}/Users/{self.scoped_user.id}'
        body = {
                "username": HelperClass.random_word_letters_only(20),
                "emailAddress": HelperClass.create_random_email(),
                "active": False,
              }
        sut = f'{url}/Users?id={self.scoped_user.id}'
        resp = self.put_without_auth_header(sut, body)
        self.assertEqual(204, resp.status_code)
        response = self.get_without_auth_header(get_url).json()
        updated_user = AuthenticationModel.from_dict(response)
        self.assertFalse(updated_user.valid)
        self.assertNotEqual(updated_user.username, self.scoped_user.username)
        self.assertNotEqual(updated_user.email_address, self.scoped_user.email_address)

    def test_should_not_be_able_to_update_a_password_with_user_endpoints(self):
        new_password = HelperClass.random_word_special_signs_included(25)
        body = {
              "password": new_password,
              }
        sut = f'{url}/Users?id={self.scoped_user.id}'
        resp = self.put_without_auth_header(sut, body)
        self.assertEqual(204, resp.status_code)
        validate_url = f'{url}/Validate'
        body = {
              "userName": self.scoped_user.username,
              "emailAddress": self.scoped_user.username,
              "passWord": new_password
              }
        validation = self.post_without_auth_header(validate_url, body).json()
        self.assertFalse(validation)


@pytest.mark.usefixtures("setup_config", "post_a_new_user")
@pytest.mark.order4
class AuthenticationDeleteApiTests(test_setup_fixture.TestFixture):

    scoped_user = None

    @pytest.fixture
    def post_a_new_user(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        self.scoped_user = AuthenticationModel.from_dict(response)
        self.scoped_user.password = password

    def test_should_be_able_to_delete_a_user(self):
        sut = f'{url}/Users?id={self.scoped_user.id}'
        response = self.delete_without_auth_header(sut)
        self.assertEqual(204, response.status_code)

    def test_should_not_be_able_to_delete_a_user_that_does_not_exist(self):
        local_id = self.unknown_id
        sut = f'{url}/Users?id={local_id}'
        response = self.delete_without_auth_header(sut)
        self.assertEqual(404, response.status_code)

    def test_should_not_be_able_to_delete_a_user_twice(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        local_id = response['id']
        sut = f'{url}/Users?id={local_id}'
        response = self.delete_without_auth_header(sut)
        self.assertEqual(204, response.status_code)
        resp = self.delete_without_auth_header(sut)
        self.assertEqual(404, resp.status_code)


@pytest.mark.usefixtures("setup_config", "post_a_new_user")
@pytest.mark.order5
class AuthenticationValidateApiTests(test_setup_fixture.TestFixture):

    scoped_user = None

    @pytest.fixture
    def post_a_new_user(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        self.scoped_user = AuthenticationModel.from_dict(response)
        self.scoped_user.password = password

    def test_should_be_able_to_validate_a_password(self):
        validate_url = f'{url}/Validate'
        body = {
              "userName": self.scoped_user.username,
              "emailAddress": self.scoped_user.email_address,
              "passWord": self.scoped_user.password
              }
        validation = self.post_without_auth_header(validate_url, body).json()
        self.assertTrue(validation)

    def test_should_be_able_to_validate_a_password_to_false(self):
        validate_url = f'{url}/Validate'
        body = {
              "userName": self.scoped_user.username,
              "emailAddress": self.scoped_user.email_address,
              "passWord": HelperClass.random_word_special_signs_included(10)
              }
        validation = self.post_without_auth_header(validate_url, body).json()
        self.assertFalse(validation)

    def test_should_be_able_to_update_a_password_using_validation_endpooint(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        local_id = response['id']

        sut = f'{url}/Validate?id={local_id}'
        new_password = HelperClass.random_word_special_signs_included(14)
        body = {
                  "oldPassWord": password,
                  "newPassWord": new_password
                }
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)

    def test_should_not_be_able_to_update_password_using_wrong_password(self):
        sut = f'{url}/Validate?id={self.scoped_user.id}'
        new_password = HelperClass.random_word_special_signs_included(14)
        body = {
                  "oldPassWord": HelperClass.random_word_special_signs_included(14),
                  "newPassWord": new_password
                }
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['ErrorId']
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "Password provided is not valid"))

    def test_should_be_able_to_update_a_password_and_validate_with_new_credentials(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        local_id = response['id']

        sut = f'{url}/Validate?id={local_id}'
        new_password = HelperClass.random_word_special_signs_included(14)
        body = {
                  "oldPassWord": password,
                  "newPassWord": new_password
                }
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)

        validate_url = f'{url}/Validate'
        body = {
              "userName": user,
              "emailAddress": email,
              "passWord": new_password
              }
        validation = self.post_without_auth_header(validate_url, body).json()
        self.assertTrue(validation)

    def test_should_not_be_able_to_update_a_password_and_validate_with_old_credentials(self):
        sut = url + '/Users'
        user = HelperClass.random_word_letters_only(25)
        email = HelperClass.create_random_email()
        password = HelperClass.random_word_special_signs_included(25)
        body = {"userName": user, "emailAddress": email, "passWord": password}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url=sut, json=body, headers=headers).json()
        local_id = response['id']

        sut = f'{url}/Validate?id={local_id}'
        new_password = HelperClass.random_word_special_signs_included(14)
        body = {
                  "oldPassWord": password,
                  "newPassWord": new_password
                }
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)

        validate_url = f'{url}/Validate'
        body = {
              "userName": user,
              "emailAddress": email,
              "passWord": password
              }
        validation = self.post_without_auth_header(validate_url, body).json()
        self.assertFalse(validation)
