from api.services.map_json_to_post_object import ObjectMapper
from api.error_handler.error_model import InvalidUsage
import api
from api.db.users_mongo import UsersDb


class ListsService:

    def get_specific_user_list(self, user_name, list_name):
        mongo_users = UsersDb(api.mongo.db)
        mongo_users.check_if_user_exists(user_name)
        mongo_users.check_if_userlist_can_be_found(user_name, list_name)
        return mongo_users.get_specific_list(user_name, list_name)

    def delete_user_list(self, user_name, list_name):
        mongo_users = UsersDb(api.mongo.db)
        user_name = user_name.lower()
        list_name = list_name.lower()
        mongo_users.check_if_user_exists(user_name)
        mongo_users.check_if_userlist_can_be_found(user_name, list_name)
        mongo_users.delete_specific_list(user_name, list_name)
        return

    def delete_all_lists_for_a_user(self, user_name):
        mongo_users = UsersDb(api.mongo.db)
        mongo_users.check_if_user_exists(user_name.lower())
        mongo_users.delete_all_user_lists(user_name.lower())
        return

    def post_new_list(self, posted_user, user_name):
        mongo_users = UsersDb(api.mongo.db)
        mapper = ObjectMapper()
        mongo_object = mapper.map_json_to_object(posted_user)
        self.validate_user_is_not_frontpage(mongo_object.user)
        mongo_users.check_if_userlist_exists(mongo_object.user, mongo_object.list)
        mongo_users.insert_new_list(mongo_object, user_name)
        return


    def update_list(self, user_name, list_name, json_body):
        mongo_users = UsersDb(api.mongo.db)
        mongo_users.check_if_user_exists(user_name.lower())
        mongo_users.check_if_userlist_can_be_found(user_name.lower(), list_name.lower())
        mapper = ObjectMapper()
        mongo_object = mapper.map_json_to_object(json_body)
        self.validate_user_is_not_frontpage(mongo_object.user)
        if mongo_object.user != user_name:
            raise InvalidUsage('You can only update your own lists', status_code=400)
        mongo_users.update_specific_list(mongo_object, user_name, list_name)
        return


    def validate_user_is_not_frontpage(self, user_name):
        if user_name.lower() == 'frontpage':            
            raise InvalidUsage('Frontpage is a reserved user cannot post', status_code=403)
        return
