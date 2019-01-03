from tests import test_setup_fixture
from environment import config
from helpers.random_name_generator import HelperClass
from helpers.models import PlaylistModel
import pytest
import os


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
    url = env_setting.playlist_url


@pytest.mark.usefixtures("setup_config")
class PlaylistApiPublicTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        sut = url + '/public/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_tgif_should_always_exist(self):
        sut = url + '/public/tgif'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['result']['beverages'])

    def test_should_be_able_to_retrieve_public_playlists(self):
        sut = url + '/public'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['result'])

    def test_should_be_able_to_get_more_details_on_all_returned_lists(self):
        sut = url + '/public'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        playlists = response.json()['result']
        for playlist in playlists:
            inner_sut = sut + '/' + playlist['list']
            resp = self.get_without_auth_header(inner_sut)
            self.assertEqual(200, resp.status_code)
            self.assertEqual(playlist['user'], resp.json()['result']['user'])

    def test_should_get_a_404_on_a_playlist_that_does_not_exist(self):
        random_playlist = HelperClass.random_word_letters_only(20)
        sut = f'{url}/public/{random_playlist}'
        response = self.get_without_auth_header(sut)
        error_message = response.json()['Error']
        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertTrue(self.validate_string_contains(error_message, "List could not be found"))


@pytest.mark.usefixtures("setup_config")
class PlayListApiPrivateTests(test_setup_fixture.TestFixture):

    def test_should_be_able_to_create_new_playlist_and_user(self):
        newUser = HelperClass.random_word_letters_only(25)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    def test_should_be_able_to_create_playlist_names_should_be_lowercase(self):
        newUser = HelperClass.random_word_letters_only(25)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

        sut = f'{url}/private/{newUser}'
        resp = self.get_without_auth_header(sut)
        self.assertEqual(200, resp.status_code)
        for x in resp.json()['result']:
            self.assertTrue(x.islower())

    def test_should_be_able_to_create_playlists_for_existing_users(self):
        newUser = HelperClass.random_word_letters_only(25)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    def test_should_not_be_able_to_create_a_playlist_twice(self):
        newUser = HelperClass.random_word_letters_only(25)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        resp = self.post_without_auth_header(sut, body)
        self.assertEqual(400, resp.status_code)
        error_message = resp.json()['Error']
        self.assertIsNotNone(error_message)
        self.assertTrue(self.validate_string_contains(error_message, "already exists"))


    def test_should_not_be_able_to_post_a_playlist_with_one_drink(self):
        newUser = HelperClass.random_word_letters_only(25)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        body['beverages'] = ['beer']
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertIsNotNone(error_message)
        self.assertEqual(meta_message['beverages'][0], "min length is 2")

    def test_should_be_able_to_create_same_playlist_for_two_users(self):
        newUser = HelperClass.random_word_letters_only(25)
        newPlaylist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        newUser = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{url}/private/{newUser}/{newPlaylist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    '''This relies on the dataseeder to seed a standard user'''
    def test_should_be_able_to_retrieve_from_a_standard_private_list(self):
        standard_user = 'marvin'
        sut = f'{url}/private/{standard_user}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())

@pytest.mark.usefixtures("setup_config")
class PlayListApiValidationTests(test_setup_fixture.TestFixture):

    def test_should_not_be_able_to_create_playlists_with_reserved_users(self):
        for keyword in self.reserved_keywords:
            sut = url + f'/private/{keyword}/test'
            body = self.test_playlist_body
            response = self.post_without_auth_header(sut, body)
            error_message = response.json()['Error']
            self.assertEqual(403, response.status_code)
            self.assertTrue(self.validate_string_contains(error_message, self.reserved_user_error))
            self.assertTrue(self.validate_string_contains(error_message, keyword))

    def test_should_not_be_able_to_post_to_an_invalid_username(self):
        newUsers = ['%20', 'o']
        for newUser in newUsers:
            newPlaylist = HelperClass.random_word_letters_only(25)
            body = PlaylistModel.create_random_playlist()
            sut = f'{url}/private/{newUser}/{newPlaylist}'
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_get_an_invalid_username(self):
        newUsers = ['%20', 'o']
        for newUser in newUsers:
            sut = f'{url}/private/{newUser}'
            response = self.get_without_auth_header(sut)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_post_invalid_data_user(self):
        newUsers = ['%20', 'o']
        for newUser in newUsers:
            playlist = 'listname'
            sut = f'{url}/private/{newUser}/{playlist}'
            body = PlaylistModel.create_random_playlist()
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_post_invalid_data_playlist(self):
        playlists = ['%20', 'o']
        for playlist in playlists:
            username = 'listname'
            sut = f'{url}/private/{username}/{playlist}'
            body = PlaylistModel.create_random_playlist()
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['playlist'][0], "min length is 2")