from api.services.map_json_to_post_object import ObjectMapper
from api.error_handler.error_model import InvalidUsage
from api.services import data_validator
import api
from api.db.users_mongo import UsersDb


class ListsService:

    def get_specific_user_list(self, user_name, list_name):
        mongo_users = UsersDb(api.mongo.db)
        return mongo_users.get_specific_list(user_name.lower(), list_name.lower())

    def delete_user_list(self, user_name, list_name):
        mongo_users = UsersDb(api.mongo.db)
        user_name = user_name.lower()
        list_name = list_name.lower()
        self.validate_user_is_not_reserved_keywords(user_name)
        mongo_users.check_if_user_exists(user_name)
        mongo_users.check_if_userlist_can_be_found(user_name, list_name)
        mongo_users.delete_specific_list(user_name, list_name)
        return

    def delete_all_lists_for_a_user(self, user_name):
        mongo_users = UsersDb(api.mongo.db)
        mongo_users.check_if_user_exists(user_name.lower())
        mongo_users.delete_all_user_lists(user_name.lower())
        return

    def post_new_list(self, posted_user, user_name, playlist_name):
        self.validate_misc_fields_in_json(posted_user)
        mongo_users = UsersDb(api.mongo.db)
        mapper = ObjectMapper()
        mongo_object = mapper.map_json_to_object(posted_user, user_name, playlist_name)
        self.validate_user_is_not_reserved_keywords(mongo_object.user)
        mongo_users.check_if_userlist_exists(mongo_object.user, mongo_object.list)
        mongo_users.insert_new_list(mongo_object, user_name)
        return

    def update_list(self, user_name, list_name, json_body):
        self.validate_misc_fields_in_json(json_body)
        mongo_users = UsersDb(api.mongo.db)
        mongo_users.check_if_userlist_can_be_found(user_name.lower(), list_name.lower())
        mapper = ObjectMapper()
        mongo_object = mapper.map_json_to_object(json_body, user_name, list_name)
        self.validate_user_is_not_reserved_keywords(mongo_object.user)
        if mongo_object.user != user_name:
            raise InvalidUsage('You can only update your own lists', status_code=400)
        mongo_users.update_specific_list(mongo_object, user_name, list_name)
        return

    def validate_user_is_not_reserved_keywords(self, user_name):
        reserved_keywords = ['global', 'frontpage', 'bevrand', 'bevragerandomizer']
        if user_name.lower() in reserved_keywords:
            raise InvalidUsage(user_name + ' is a reserved username and cannot be used for creation or deletion', status_code=403)
        return

    def validate_misc_fields_in_json(self, json_body):
        data_validator.validate_beverages(json_body['beverages'])
        data_validator.validate_display_name(json_body['displayName'])
        if 'imageUrl' in json_body:
            data_validator.validate_image_url(json_body['imageUrl'])
        if 'list' in json_body:
            data_validator.validate_play_list(json_body['list'])
