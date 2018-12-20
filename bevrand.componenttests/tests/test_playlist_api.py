from tests import test_setup_fixture
from environment import config
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
class PlaylistApiTests(test_setup_fixture.TestFixture):

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
            print(playlist)
            inner_sut = sut + '/' + playlist['list']
            resp = self.get_without_auth_header(inner_sut)
            self.assertEqual(200, resp.status_code)
            self.assertEqual(playlist['user'], resp.json()['result']['user'])
