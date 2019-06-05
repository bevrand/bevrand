from tests import test_setup_fixture
from helpers.random_name_generator import HelperClass


class HighScoreApiTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        split_url = "/".join(self.highscore_url.split("/", 3)[:3])
        sut = split_url + '/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_post_a_sample_drink(self):
        sut = self.highscore_url + 'test/test/'
        body = {"drink" : "beer"}
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    def test_should_be_able_to_post_a_sample_drink_and_retrieve_it(self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'{user}/{playlist}/'
        body = {"drink" : "beer"}
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        resp = self.get_without_auth_header(sut)
        self.assertEqual(200, resp.status_code)
        json_body = resp.json()
        self.assertTrue(len(json_body) >= 1)

    def test_should_get_a_404_for_a_user_and_playlist_that_does_not_exist(self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'{user}/{playlist}/'
        resp = self.get_without_auth_header(sut)
        self.assertEqual(404, resp.status_code)

    def test_should_get_a_404_for_a_playlist_that_does_not_exist(self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'{user}/{playlist}/'
        body = {"drink" : "beer"}
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        playlist = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'/{user}/{playlist}/'
        resp = self.get_without_auth_header(sut)
        self.assertEqual(404, resp.status_code)

    def test_should_not_be_able_to_post_an_empty_list(self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'{user}/{playlist}/'
        body = {}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['errorMessage']
        meta_message = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "You have to provide a body"))

    def test_should_not_be_able_to_post_with_user_global(self):
        playlist = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'global/{playlist}'
        body = {"drink" : "beer"}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['errorMessage']
        meta_message = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertIsNotNone(meta_message)
        self.assertTrue(self.validate_string_contains(error_message, "Global is a restricted user"))

    def test_should_be_able_to_post_a_sample_drink_and_retrieve_it_from_global(self):
        playlist = HelperClass.random_word_letters_only(25)
        user = HelperClass.random_word_letters_only(25)
        sut = self.highscore_url + f'{user}/{playlist}/'
        body = {"drink": "beer"}
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        resp = self.get_without_auth_header(self.highscore_url)
        self.assertIsNotNone(resp)

