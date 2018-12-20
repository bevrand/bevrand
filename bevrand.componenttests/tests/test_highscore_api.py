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
    url = env_setting.highscore_url


@pytest.mark.usefixtures("setup_config")
class HighScoreApiTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        sut = url + '/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(404, response.status_code)