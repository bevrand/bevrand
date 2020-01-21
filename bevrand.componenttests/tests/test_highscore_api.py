from helpers.random_name_generator import HelperClass
from tests import test_setup_fixture


class HighScoreApiTests(test_setup_fixture.TestFixture):
    def test_ping_returns_200(self):
        split_url = "/".join(self.highscore_url.split("/", 3)[:3])
        sut = split_url + "/ping"
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_should_get_a_404_for_a_user_and_playlist_that_does_not_exist(
            self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f"{user}/{playlist}/"
        resp = self.get_without_auth_header(sut)
        self.assertEqual(404, resp.status_code)

    def test_should_get_a_404_for_a_playlist_that_does_not_exist(self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f"/{user}/{playlist}/"
        resp = self.get_without_auth_header(sut)
        self.assertEqual(404, resp.status_code)

    def test_should_get_user_lists_when_randomizing(self):
        sut = self.randomizer_url + "/v1/randomize"
        body = self.test_randomize_body
        for _ in range(3):
            self.post_without_auth_header(sut, body)
        resp = self.get_without_auth_header(self.highscore_url)
        self.assertEqual(200, resp.status_code)
        self.assertIsNotNone(resp)

    def test_should_get_global_lists_when_randomizing(self):
        sut = self.randomizer_url + "/v1/randomize"
        body = self.test_randomize_body
        for _ in range(5):
            self.post_without_auth_header(sut, body)
        not_yet_resolved = True
        sut = (
            self.highscore_url +
            f'/{self.test_randomize_body["user"]}/{self.test_randomize_body["list"]}/'
        )
        while not_yet_resolved:
            resp = self.get_without_auth_header(sut)
            if resp.status_code == 200:
                not_yet_resolved = False
        self.assertEqual(200, resp.status_code)
