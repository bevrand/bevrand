from tests import test_setup_fixture
from helpers.random_name_generator import HelperClass
from helpers.models import PlaylistModel


class PlaylistApiPublicTests(test_setup_fixture.TestFixture):

    def test_ping_returns_200(self):
        sut = self.playlist_url + '/public/ping'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)

    def test_tgif_should_always_exist(self):
        sut = self.playlist_url + '/public/tgif'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['result']['beverages'])

    def test_should_be_able_to_retrieve_public_playlists(self):
        sut = self.playlist_url + '/public'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['result'])

    def test_should_be_able_to_get_more_details_on_all_returned_lists(self):
        sut = self.playlist_url + '/public'
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
        sut = f'{self.playlist_url}/public/{random_playlist}'
        response = self.get_without_auth_header(sut)
        error_message = response.json()['Error']
        self.assertEqual(404, response.status_code)
        self.assertIsNotNone(error_message)
        self.assertTrue(self.validate_string_contains(error_message, "List could not be found"))


class PlayListApiPrivateTests(test_setup_fixture.TestFixture):

    def test_should_be_able_to_create_new_playlist_and_user(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    def test_should_be_able_to_create_playlist_names_should_be_lowercase(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

        sut = f'{self.playlist_url}/private/{new_user}'
        resp = self.get_without_auth_header(sut)
        self.assertEqual(200, resp.status_code)
        for x in resp.json()['result']:
            self.assertTrue(x['list'].islower())

    def test_should_be_able_to_create_playlists_for_existing_users(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    def test_should_not_be_able_to_create_a_playlist_twice(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        resp = self.post_without_auth_header(sut, body)
        self.assertEqual(400, resp.status_code)
        error_message = resp.json()['Error']
        self.assertIsNotNone(error_message)
        self.assertTrue(self.validate_string_contains(error_message, "already exists"))


    def test_should_not_be_able_to_post_a_playlist_with_one_drink(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        body['beverages'] = ['beer']
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertIsNotNone(error_message)
        self.assertEqual(meta_message['beverages'][0], "min length is 2")

    def test_should_be_able_to_create_same_playlist_for_two_users(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)
        new_user = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(201, response.status_code)

    '''This relies on the dataseeder to seed a standard user'''
    def test_should_be_able_to_retrieve_from_a_standard_private_list(self):
        standard_user = 'marvin'
        sut = f'{self.playlist_url}/private/{standard_user}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())

    '''This relies on the dataseeder to seed a standard user'''
    def test_should_be_able_to_retrieve_from_a_standard_private_list_specific_playlist(self):
        standard_user = 'marvin'
        playlist = 'paranoid'
        sut = f'{self.playlist_url}/private/{standard_user}/{playlist}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())

    def test_should_get_a_200_for_getting_all_playlists_for_a_user_that_does_not(self):
        user = HelperClass.random_word_letters_only(25)
        sut = f'{self.playlist_url}/private/{user}'
        response = self.get_without_auth_header(sut)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())

    def test_should_be_able_to_create_new_playlist_and_retrieve_it(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        self.post_without_auth_header(sut, body)
        resp = self.get_without_auth_header(sut)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json()['result']['user'], new_user.lower())

    def test_should_be_able_to_delete_a_created_playlist(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        self.post_without_auth_header(sut, body)
        resp = self.delete_without_auth_header(sut)
        self.assertEqual(204, resp.status_code)

    def test_should_be_able_to_delete_a_created_user(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        self.post_without_auth_header(sut, body)
        sut = f'{self.playlist_url}/private/{new_user}'
        resp = self.delete_without_auth_header(sut)
        self.assertEqual(204, resp.status_code)

    def test_should_not_be_able_to_delete_invalid_users(self):
        new_users = ['%20', 'o']
        for new_user in new_users:
            sut = f'{self.playlist_url}/private/{new_user}'
            response = self.delete_without_auth_header(sut)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_delete_invalid_playlists(self):
        new_playlists = ['%20', 'o']
        for playlist in new_playlists:
            sut = f'{self.playlist_url}/private/username/{playlist}'
            response = self.delete_without_auth_header(sut)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['playlist'][0], "min length is 2")

    def test_should_not_be_able_to_delete_playlist_that_do_not_exist(self):
        playlist = HelperClass.random_word_letters_only(40)
        sut = f'{self.playlist_url}/private/marvin/{playlist}'
        response = self.delete_without_auth_header(sut)
        self.assertEqual(404, response.status_code)
        error_message = response.json()['Error']
        self.assertEqual(error_message, "List could not be found")

    def test_should_not_be_able_to_delete_user_that_do_not_exist(self):
        user = HelperClass.random_word_letters_only(40)
        sut = f'{self.playlist_url}/private/{user}/somerandomlist'
        response = self.delete_without_auth_header(sut)
        self.assertEqual(404, response.status_code)
        error_message = response.json()['Error']
        self.assertEqual(error_message, "User could not be found")

    def test_should_be_able_to_put_a_created_user(self):
        new_user = HelperClass.random_word_letters_only(25)
        new_playlist = HelperClass.random_word_letters_only(25)
        body = PlaylistModel.create_random_playlist()
        sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
        self.post_without_auth_header(sut, body)
        body['beverages'] = ['beer', 'beer', 'beer']
        new_display_name = 'newDisplayName'
        body['displayName'] = new_display_name
        resp = self.put_without_auth_header(sut, body)
        self.assertEqual(204, resp.status_code)
        response = self.get_without_auth_header(sut)
        json_body = response.json()['result']
        self.assertEqual(200, response.status_code)
        self.assertEqual(new_display_name, json_body['displayName'])
        self.assertEqual('beer', json_body['beverages'][0])

    def test_should_not_be_able_to_update_list_that_do_not_exist(self):
        user = HelperClass.random_word_letters_only(40)
        sut = f'{self.playlist_url}/private/{user}/somerandomlist'
        body = PlaylistModel.create_random_playlist()
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(404, response.status_code)
        error_message = response.json()['Error']
        self.assertEqual(error_message, "List could not be found")


class PlayListApiValidationTests(test_setup_fixture.TestFixture):

    def test_should_not_be_able_to_create_playlists_with_reserved_users(self):
        for keyword in self.reserved_keywords:
            sut = self.playlist_url + f'/private/{keyword}/test'
            body = self.test_playlist_body
            response = self.post_without_auth_header(sut, body)
            error_message = response.json()['Error']
            self.assertEqual(403, response.status_code)
            self.assertTrue(self.validate_string_contains(error_message, self.reserved_user_error))
            self.assertTrue(self.validate_string_contains(error_message, keyword))

    def test_should_not_be_able_to_post_to_an_invalid_username(self):
        new_users = ['%20', 'o']
        for new_user in new_users:
            new_playlist = HelperClass.random_word_letters_only(25)
            body = PlaylistModel.create_random_playlist()
            sut = f'{self.playlist_url}/private/{new_user}/{new_playlist}'
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_get_an_invalid_username(self):
        new_users = ['%20', 'o']
        for new_user in new_users:
            sut = f'{self.playlist_url}/private/{new_user}'
            response = self.get_without_auth_header(sut)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_post_invalid_data_user(self):
        new_users = ['%20', 'o']
        for new_user in new_users:
            playlist = 'listname'
            sut = f'{self.playlist_url}/private/{new_user}/{playlist}'
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
            sut = f'{self.playlist_url}/private/{username}/{playlist}'
            body = PlaylistModel.create_random_playlist()
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['playlist'][0], "min length is 2")

    def test_should_not_be_able_to_post_invalid_data_displayname(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        displaynames = ['i', ' ']
        for displayname in displaynames:
            body['displayName'] = displayname
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['displayName'][0], "min length is 3")

    def test_should_not_be_able_to_post_invalid_data_imageurl(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        images = ['i', ' ']
        for image in images:
            body['imageUrl'] = image
            response = self.post_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['imageUrl'][0], "min length is 3")

    def test_should_not_be_able_to_post_invalid_data_beverages(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        body['beverages'] = ['b', ' ']
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertIsNotNone(error_message)
        self.assertEqual(meta_message['beverages'][0]['0'][0], "min length is 2")

    def test_should_not_be_able_to_post_invalid_data_beverage_list(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        body['beverages'] = ['beer']
        response = self.post_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertIsNotNone(error_message)
        self.assertEqual(meta_message['beverages'][0], "min length is 2")

    def test_should_not_be_able_to_put_invalid_data_user(self):
        new_users = ['%20', 'o']
        for new_user in new_users:
            playlist = 'listname'
            sut = f'{self.playlist_url}/private/{new_user}/{playlist}'
            body = PlaylistModel.create_random_playlist()
            response = self.put_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['user_name'][0], "min length is 3")

    def test_should_not_be_able_to_put_invalid_data_playlist(self):
        playlists = ['%20', 'o']
        for playlist in playlists:
            username = 'listname'
            sut = f'{self.playlist_url}/private/{username}/{playlist}'
            body = PlaylistModel.create_random_playlist()
            response = self.put_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['playlist'][0], "min length is 2")

    def test_should_not_be_able_to_put_invalid_data_displayname(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        displaynames = ['i', ' ']
        for displayname in displaynames:
            body['displayName'] = displayname
            response = self.put_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['displayName'][0], "min length is 3")

    def test_should_not_be_able_to_put_invalid_data_imageurl(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        images = ['i', ' ']
        for image in images:
            body['imageUrl'] = image
            response = self.put_without_auth_header(sut, body)
            self.assertEqual(400, response.status_code)
            error_message = response.json()['Error']
            meta_message = response.json()['Meta']
            self.assertIsNotNone(error_message)
            self.assertEqual(meta_message['imageUrl'][0], "min length is 3")

    def test_should_not_be_able_to_put_invalid_data_beverages(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        body['beverages'] = ['b', ' ']
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertIsNotNone(error_message)
        self.assertEqual(meta_message['beverages'][0]['0'][0], "min length is 2")

    def test_should_not_be_able_to_put_invalid_data_beverage_list(self):
        username = 'listname'
        playlist = 'playlistname'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        body['beverages'] = ['beer']
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(400, response.status_code)
        error_message = response.json()['Error']
        meta_message = response.json()['Meta']
        self.assertIsNotNone(error_message)
        self.assertEqual(meta_message['beverages'][0], "min length is 2")

    def test_should_not_be_able_to_update_frontpage_lists(self):
        username = 'frontpage'
        playlist = 'tgif'
        sut = f'{self.playlist_url}/public/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(404, response.status_code)

    def test_should_not_be_able_to_update_frontpage_lists_private(self):
        username = 'frontpage'
        playlist = 'tgif'
        sut = f'{self.playlist_url}/private/{username}/{playlist}'
        body = PlaylistModel.create_random_playlist()
        response = self.put_without_auth_header(sut, body)
        self.assertEqual(404, response.status_code)

