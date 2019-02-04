from tests import test_setup_fixture
from environment import config
from helpers.models import ProxyModel, Jwtheader
from helpers.random_name_generator import HelperClass
from random import shuffle
import pytest
import os

url = None


@pytest.fixture(scope="module")
def setup_config():
    env = os.environ.get('PYTHON_ENV')
    if env == 'Test':
        env_setting = config.Test()
    else:  # If local or other
        env_setting = config.Local()
    global url
    url = env_setting.proxy_url


@pytest.mark.usefixtures("setup_config")
class ProxyApiTestsPlaylistsPublic(test_setup_fixture.TestFixture):

    def test_should_be_able_to_retrieve_all_playlist(self):
        sut = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_all_playslists_should_be_signed(self):
        sut = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(sut).json()
        for playlist in response:
            self.assertIsNotNone(playlist['jwttoken'])

    def test_all_playslists_token_should_be_different(self):
        sut = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(sut).json()
        tokens = []
        for playlist in response:
            token = playlist['jwttoken']
            self.assertTrue(token not in tokens)
            tokens.append(token)


@pytest.mark.usefixtures("setup_config")
class ProxyApiTestsPlaylistsPublic(test_setup_fixture.TestFixture):

    def test_should_be_able_to_retrieve_a_user_playlist(self):
        sut = f'{url}/playlists?username={self.data_seeded_user}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)


@pytest.mark.usefixtures("setup_config")
class ProxyApiTestsRandomizeValidations(test_setup_fixture.TestFixture):

    def test_should_be_able_to_send_json_body_in_random_order(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for playlist in response:
            unsorted_playlist = playlist.copy()
            del unsorted_playlist['displayName']
            del unsorted_playlist['id']
            del unsorted_playlist['user']
            unsorted_playlist['displayName'] = playlist['displayName']
            unsorted_playlist['user'] = playlist['user']
            unsorted_playlist['id'] = playlist['id']
            response = self.post_without_auth_header(sut, unsorted_playlist)
            self.assertEqual(200, response.status_code)

    def test_should_not_be_able_to_send_beverages_in_random_order(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for playlist in response:
            shuffle(playlist['beverages'])
            response = self.post_without_auth_header(sut, playlist)
            self.assertEqual(400, response.status_code)

    def test_should_not_be_able_to_randomize_lists_with_different_payload_token(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.jwttoken = 'iamannewtoken'
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            json_body = response.json()
            self.assertTrue(self.validate_string_contains(json_body['message'], 'does not validate'))

    def test_should_not_be_able_to_randomize_lists_with_different_payload_beverages(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.beverages = ['beer', 'beer', 'beer']
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            json_body = response.json()
            self.assertTrue(self.validate_string_contains(json_body['message'], 'does not validate'))

    def test_should_not_be_able_to_randomize_lists_with_different_payload_image(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.image_url = HelperClass.random_word_letters_only(20)
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            json_body = response.json()
            self.assertTrue(self.validate_string_contains(json_body['message'], 'does not validate'))

    def test_should_not_be_able_to_randomize_lists_with_different_payload_displayname(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.display_name = HelperClass.random_word_letters_only(20)
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            json_body = response.json()
            self.assertTrue(self.validate_string_contains(json_body['message'], 'does not validate'))

    def test_should_not_be_able_to_randomize_lists_with_different_payload_user(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.username = HelperClass.random_word_letters_only(20)
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            json_body = response.json()
            self.assertTrue(self.validate_string_contains(json_body['message'], 'does not validate'))

    def test_should_not_be_able_to_randomize_lists_with_different_payload_list(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.playlist = HelperClass.random_word_letters_only(20)
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            json_body = response.json()
            self.assertTrue(self.validate_string_contains(json_body['message'], 'does not validate'))

    def test_should_not_be_able_to_randomize_lists_with_different_payload_iat(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            playlist.iat = HelperClass.random_int_generator(10)
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)

    # This should trigger a playload error
    def test_should_not_be_able_to_randomize_lists_with_different_payload_jwtheader(self):
        sut = f'{url}/v2/randomize'
        front_page_url = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(front_page_url).json()
        for pl in response:
            playlist = ProxyModel.from_dict(pl)
            jwtheader = Jwtheader(HelperClass.random_word_letters_only(4))
            playlist.jwtheader = jwtheader
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)


@pytest.mark.usefixtures("setup_config", "get_playlists")
class ProxyApiTestsRandomize(test_setup_fixture.TestFixture):

    playlists = []

    @pytest.fixture
    def get_playlists(self):
        sut = f'{url}/v2/frontpage'
        response = self.get_without_auth_header(sut).json()
        for playlist in response:
            pl = ProxyModel.from_dict(playlist)
            self.playlists.append(pl)

    def test_should_be_able_to_randomize_each_list(self):
        sut = f'{url}/v2/randomize'
        for playlist in self.playlists:
            body = ProxyModel.to_dict(playlist)
            response = self.post_without_auth_header(sut, body)
            print(body)
            self.assertEqual(200, response.status_code)
            self.assertTrue(response.json()['result'] in playlist.beverages)

    def test_should_not_be_able_to_randomize_an_unsigned_list(self):
        sut = f'{url}/v2/randomize'
        body = self.test_randomize_body
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)

    def test_should_not_be_able_to_randomize_an_empty_body(self):
        sut = f'{url}/v2/randomize'
        body = {}
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)

