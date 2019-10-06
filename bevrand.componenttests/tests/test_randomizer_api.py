from tests import test_setup_fixture


class RandomizerApiTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        sut = self.randomizer_url + '/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    #this test is to check for backwards compatibility
    def test_should_be_able_to_randomize_a_simple_list_old_enpoint(self):
        sut = self.randomizer_url + '/randomize'
        body = self.test_randomize_body
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)

    def test_should_be_able_to_randomize_a_simple_list(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = self.test_randomize_body
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)


class RandomizerValidationChecks(test_setup_fixture.TestFixture):

    def test_should_not_be_able_to_make_empty_calls(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = {}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 3)

    def test_should_not_be_able_to_make_call_without_beverages(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = {"list": "tgif", "user": "frontpage"}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 1)
        for key, value in error_message[0].items():
            if key == "validationField":
                self.assertTrue(self.validate_string_contains(value, "beverages"))
            else:
                self.assertTrue(self.validate_string_contains(value, "beveragelist"))

    def test_should_not_be_able_to_make_call_without_user(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = { "beverages": [
                            "beer",
                            "wine",
                            "whiskey"
                          ],"list": "frontpage"}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 1)
        for key, value in error_message[0].items():
            if key == "validationField":
                self.assertTrue(self.validate_string_contains(value, "user"))
            else:
                self.assertTrue(self.validate_string_contains(value, "short"))

    def test_should_not_be_able_to_make_call_without_playlist(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = { "beverages": [
                            "beer",
                            "wine",
                            "whiskey"
                          ],"user": "frontpage"}
        response = self.post_without_auth_header(sut, body)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 1)
        for key, value in error_message[0].items():
            if key == "validationField":
                self.assertTrue(self.validate_string_contains(value, "playlist"))
            else:
                self.assertTrue(self.validate_string_contains(value, "short"))

    def test_should_be_able_to_include_extra_json_fields(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = {
            "beverages": [
                "beer",
                "wine",
                "whiskey"
            ],
            "list": "tgif",
            "user": "frontpage",
            "anextrafield": "just an extra field"
        }
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(200, response.status_code)

    '''playlists should be at least two chars long'''
    def test_should_not_be_able_to_randomize_with_invalid_playlist(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = {
            "beverages": [
                "beer",
                "wine",
                "whiskey"
            ],
            "list": "t",
            "user": "frontpage",
        }
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 1)
        for key, value in error_message[0].items():
            if key == "validationField":
                self.assertTrue(self.validate_string_contains(value, "playlist"))
            else:
                self.assertTrue(self.validate_string_contains(value, "short"))

    '''users should be at least two chars long'''
    def test_should_not_be_able_to_randomize_with_invalid_user(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = {
            "beverages": [
                "beer",
                "wine",
                "whiskey"
            ],
            "list": "tgif",
            "user": "f",
        }
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 1)
        for key, value in error_message[0].items():
            if key == "validationField":
                self.assertTrue(self.validate_string_contains(value, "user"))
            else:
                self.assertTrue(self.validate_string_contains(value, "short"))

    '''beverages list should be at least two beverages long'''
    def test_should_not_be_able_to_randomize_with_invalid_beverage_list(self):
        sut = self.randomizer_url + '/v1/randomize'
        body = {
            "beverages": [
                "beer"
            ],
            "list": "tgif",
            "user": "frontpage",
        }
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['errorModel']
        code = response.json()['uniqueCode']
        self.assertEqual(400, response.status_code)
        self.assertIsNotNone(code)
        self.assertTrue(len(error_message) == 1)
        for key, value in error_message[0].items():
            if key == "validationField":
                self.assertTrue(self.validate_string_contains(value, "beverages"))
            else:
                self.assertTrue(self.validate_string_contains(value, "beveragelist"))
